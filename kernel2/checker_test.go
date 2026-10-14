package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/base64"
	"encoding/binary"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"os/exec"
	"strings"
	"testing"
)

func TestCanonicalBoundaries(t *testing.T) {
	cases := []struct{ line, reason string }{
		{`{"a":01}`, "malformed_json"},
		{`{"a":+1}`, "malformed_json"},
		{`{"a":1.}`, "malformed_json"},
		{`{"a":1e}`, "malformed_json"},
		{`{"a":NaN}`, "malformed_json"},
		{`{"a":"\u+001"}`, "malformed_json"},
		{`{"a":"\ud800\ud800"}`, "malformed_json"},
		{`{"a":"\udfff"}`, "malformed_json"},
		{`{"a":"\ud800","a":0}`, "malformed_json"},
		{`{"a":1.5,"a":0,"x":"\ud800"}`, "malformed_json"},
		{`{"a":-9007199254740992}`, "not_canonical"},
		{`{"a":1e99999999999999999999}`, "not_canonical"},
		{`{"a":"\u000A"}`, "not_canonical"},
		{`{"a":"\/"}`, "not_canonical"},
		{`{"a":1,"\u0061":2}`, "not_canonical"},
		{`{"a":{"b":0,"b":1}}`, "not_canonical"},
		{`{"a":"<>&/\ufffd"}`, ""},
		{`{"a":-9007199254740991}`, ""},
		{`{"\ue000":1,"\ud800\udc00":2}`, ""},
		{`{"\ud800\udc00":2,"\ue000":1}`, "not_canonical"},
		{"{\"a\":\"\xff\"}", "malformed_json"},
		{"{}\r", "not_canonical"},
		{"{} {}", "malformed_json"},
	}
	for _, c := range cases {
		if _, got := parseCanonical([]byte(c.line)); got != c.reason {
			t.Errorf("%q: got %q want %q", c.line, got, c.reason)
		}
	}
	deep := `{"a":` + strings.Repeat("[", 10001) + "0" + strings.Repeat("]", 10001) + "}"
	if _, reason := parseCanonical([]byte(deep)); reason != "" {
		t.Fatalf("unbounded body depth: %s", reason)
	}
}

func testPrivate(label string) ed25519.PrivateKey {
	seed := sha256.Sum256([]byte("kernel2 tests: " + label))
	return ed25519.NewKeyFromSeed(seed[:])
}

func testPublicBlob(private ed25519.PrivateKey) []byte {
	return append(wireString([]byte("ssh-ed25519")), wireString(private.Public().(ed25519.PublicKey))...)
}

func testDeclaration(id string, private ed25519.PrivateKey, powers ...string) object {
	ps := make([]any, len(powers))
	for i, p := range powers {
		ps[i] = p
	}
	return object{"key_id": id, "principal": "tester", "powers": ps, "pubkey": "ssh-ed25519 " + base64.StdEncoding.EncodeToString(testPublicBlob(private))}
}

func testSign(m object, private ed25519.PrivateKey) {
	delete(m, "sig")
	sig := ed25519.Sign(private, signedData(canonical(m)))
	inner := append(wireString([]byte("ssh-ed25519")), wireString(sig)...)
	b := append([]byte("SSHSIG"), 0, 0, 0, 1)
	for _, part := range [][]byte{testPublicBlob(private), []byte("core-entry"), {}, []byte("sha512"), inner} {
		b = append(b, wireString(part)...)
	}
	m["sig"] = base64.StdEncoding.EncodeToString(b)
}

func testEntry(typ string, body object) object {
	return object{"seq": jsonInteger(0), "parent": strings.Repeat("0", 64), "ts": "2026-10-14T00:00:00Z", "type": typ, "proposer": "tester", "body": body}
}

func testGenesis(private ed25519.PrivateKey) object {
	m := testEntry("genesis", object{"charter": strings.Repeat("0", 64), "checker": strings.Repeat("0", 64), "keys": []any{testDeclaration("root", private, "genesis", "key", "proposal", "merge")}})
	testSign(m, private)
	return m
}

func testReason(t *testing.T, b []byte, reason string, seq int64) {
	t.Helper()
	v, err := checkLog(bytes.NewReader(b))
	if err != nil {
		t.Fatal(err)
	}
	if reason == "" {
		if v["ok"] != true {
			t.Fatalf("expected valid: %v", v)
		}
		return
	}
	if v["reason"] != reason || v["seq"] != seq || v["ok"] != false {
		t.Fatalf("got %v, want %s at %d", v, reason, seq)
	}
}

func TestFailurePrecedence(t *testing.T) {
	private := testPrivate("precedence")
	for _, c := range []struct {
		name, reason string
		edit         func(object)
	}{
		{"shape before sequence", "schema", func(m object) { m["seq"] = jsonInteger(3); m["extra"] = nil }},
		{"sequence before parent", "bad_seq", func(m object) { m["seq"] = jsonInteger(3); m["parent"] = strings.Repeat("1", 64) }},
		{"parent before placement", "parent_mismatch", func(m object) { m["parent"] = strings.Repeat("1", 64); m["type"] = "proposal" }},
		{"placement before proposer", "genesis_misplaced", func(m object) { m["type"] = "proposal"; m["proposer"] = "" }},
		{"proposer before body", "no_proposer", func(m object) { m["proposer"] = ""; m["body"] = object{} }},
		{"body before signature", "schema", func(m object) { m["body"] = object{}; m["sig"] = "AA==" }},
		{"key declaration before signature", "bad_key", func(m object) {
			d := testDeclaration("weak", private)
			d["pubkey"] = "ssh-ed25519 " + base64.StdEncoding.EncodeToString(append(wireString([]byte("ssh-ed25519")), wireString(encodePoint(identity()))...))
			m["body"].(object)["keys"] = []any{d}
			m["sig"] = "AA=="
		}},
		{"all key schemas before declaration", "schema", func(m object) {
			d := testDeclaration("weak", private)
			d["pubkey"] = "ssh-ed25519 " + base64.StdEncoding.EncodeToString(append(wireString([]byte("ssh-ed25519")), wireString(encodePoint(identity()))...))
			m["body"].(object)["keys"] = []any{d, object{}}
		}},
		{"unknown key before Ed25519", "unknown_key", func(m object) { m["body"].(object)["keys"] = []any{} }},
		{"principal before Ed25519", "proposer_mismatch", func(m object) { m["proposer"] = "someone else" }},
		{"power before Ed25519", "no_power", func(m object) { m["body"].(object)["keys"].([]any)[0].(object)["powers"] = []any{} }},
	} {
		t.Run(c.name, func(t *testing.T) { m := testGenesis(private); c.edit(m); testReason(t, canonical(m), c.reason, 0) })
	}
}

func TestKeyRotationAndFutureEffect(t *testing.T) {
	old, replacement := testPrivate("old"), testPrivate("replacement")
	genesis := canonical(testGenesis(old))
	appendEntry := func(log []byte, seq int64, typ string, body object, signer ed25519.PrivateKey) []byte {
		lines := bytes.Split(log, []byte{'\n'})
		m := testEntry(typ, body)
		m["seq"] = jsonInteger(seq)
		m["parent"] = fmt.Sprintf("%x", sha256.Sum256(lines[len(lines)-1]))
		testSign(m, signer)
		return append(append(append([]byte(nil), log...), '\n'), canonical(m)...)
	}
	// A replacement cannot sign its own admission; the old key can.
	body := testDeclaration("root", replacement, "genesis", "key", "proposal")
	testReason(t, appendEntry(genesis, 1, "key", body, replacement), "unknown_key", 1)
	rotated := appendEntry(genesis, 1, "key", body, old)
	testReason(t, rotated, "", 0)
	proposal := object{"title": "rotation", "commit": strings.Repeat("0", 40)}
	testReason(t, appendEntry(rotated, 2, "proposal", proposal, old), "unknown_key", 2)
	testReason(t, appendEntry(rotated, 2, "proposal", proposal, replacement), "", 0)
	// The replaced blob is no longer assigned in the current key map.
	reused := appendEntry(rotated, 2, "key", testDeclaration("old_id", old, "proposal"), replacement)
	testReason(t, appendEntry(reused, 3, "proposal", proposal, old), "", 0)
	// Removing one's own powers is allowed under the previous state.
	revoked := appendEntry(rotated, 2, "key", testDeclaration("root", replacement), replacement)
	testReason(t, revoked, "", 0)
	testReason(t, appendEntry(revoked, 3, "proposal", proposal, replacement), "no_power", 3)
}

func TestContainerBoundaries(t *testing.T) {
	m := testGenesis(testPrivate("containers"))
	b, err := base64.StdEncoding.DecodeString(m["sig"].(string))
	if err != nil {
		t.Fatal(err)
	}
	for i := 0; i < len(b); i++ {
		if _, ok, err := parseSignature(base64.StdEncoding.EncodeToString(b[:i])); ok || err != nil {
			t.Fatalf("truncation %d: valid=%v err=%v", i, ok, err)
		}
	}
	bad := append(append([]byte(nil), b...), 0)
	if _, ok, _ := parseSignature(base64.StdEncoding.EncodeToString(bad)); ok {
		t.Fatal("trailing byte accepted")
	}
	bad = append([]byte(nil), b...)
	binary.BigEndian.PutUint32(bad[10:14], ^uint32(0))
	if _, ok, _ := parseSignature(base64.StdEncoding.EncodeToString(bad)); ok {
		t.Fatal("oversized wire length accepted")
	}
	for _, text := range []string{"A", "AAA", "AA=", "AA===", "AA==\n", "AA==\r", "AA-A", "AA_A", "AA==AA=="} {
		if _, ok, err := decodeBase64(text); ok || err != nil {
			t.Fatalf("bad base64 %q: valid=%v err=%v", text, ok, err)
		}
	}
}

type failAfterLine struct{ sent bool }

func (r *failAfterLine) Read(b []byte) (int, error) {
	if r.sent {
		return 0, fmt.Errorf("must not read beyond first refused line")
	}
	r.sent = true
	return copy(b, []byte("{\n")), nil
}

func TestLineBoundaries(t *testing.T) {
	g := canonical(testGenesis(testPrivate("lines")))
	testReason(t, nil, "", 0)
	testReason(t, []byte{'\n'}, "malformed_json", 0)
	testReason(t, g, "", 0)
	testReason(t, append(append([]byte(nil), g...), '\n'), "", 0)
	testReason(t, append(append([]byte(nil), g...), '\n', '\n'), "malformed_json", 1)
	testReason(t, append(append([]byte(nil), g...), '\r', '\n'), "not_canonical", 0)
	v, err := checkLog(&failAfterLine{})
	if err != nil || v["reason"] != "malformed_json" {
		t.Fatalf("read after refusal: %v %v", v, err)
	}
	// A signed line over 64 KiB must not hit bufio.Scanner's default limit.
	m := testGenesis(testPrivate("long line"))
	m["body"].(object)["extra.with.dot"] = strings.Repeat("x", 100000)
	testSign(m, testPrivate("long line"))
	testReason(t, canonical(m), "", 0)
}

func TestOpenQuestions(t *testing.T) {
	for _, timestamp := range []string{"2026-02-30T00:00:00Z", "2026-12-31T23:59:60Z", "0000-01-01T00:00:00Z", "٢٠٢٦-10-14T00:00:00Z"} {
		m := testGenesis(testPrivate("questions"))
		m["ts"] = timestamp
		v, err := checkLog(bytes.NewReader(canonical(m)))
		if v != nil || err == nil || !strings.Contains(err.Error(), "Q1") {
			t.Fatalf("Q1 was decided: %v %v", v, err)
		}
	}
	if _, ok, err := decodeBase64("AB=="); ok || err == nil || !strings.Contains(err.Error(), "Q2") {
		t.Fatalf("Q2 was decided: %v %v", ok, err)
	}
}

func TestCLIUsageAndIO(t *testing.T) {
	for _, args := range [][]string{nil, {"a", "b"}, {"./.cache/nonexistent-input.jsonl"}, {"."}} {
		var stdout, stderr bytes.Buffer
		if status := run(args, &stdout, &stderr); status != 2 || stdout.Len() != 0 || stderr.Len() == 0 {
			t.Fatalf("args=%v status=%d stdout=%q stderr=%q", args, status, stdout.String(), stderr.String())
		}
	}
	for _, args := range [][]string{nil, {"a", "b"}, {"./.cache/nonexistent-input.jsonl"}} {
		cmd := exec.Command("./check", args...)
		var stdout, stderr bytes.Buffer
		cmd.Stdout, cmd.Stderr = &stdout, &stderr
		err := cmd.Run()
		exit, ok := err.(*exec.ExitError)
		if !ok || exit.ExitCode() != 2 || stdout.Len() != 0 || stderr.Len() == 0 {
			t.Fatalf("launcher args=%v err=%v stdout=%s stderr=%s", args, err, stdout.String(), stderr.String())
		}
	}
}

func TestLauncherReasonMutation(t *testing.T) {
	// Test the README-required literal mutation on a copy within kernel2.
	// build.sh locates its own output, so the temporary launcher points back
	// to it and to the real binary while only its reason literal is changed.
	launcher, err := os.ReadFile("check")
	if err != nil {
		t.Fatal(err)
	}
	if bytes.Count(launcher, []byte("bad_signature")) != 1 {
		t.Fatal("launcher must have one live bad_signature literal")
	}
	mutated := bytes.Replace(launcher, []byte("bad_signature"), []byte("mutation_detected"), 1)
	abs, err := os.Getwd()
	if err != nil {
		t.Fatal(err)
	}
	mutated = bytes.Replace(mutated, []byte(`dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)`), []byte("dir='"+strings.ReplaceAll(abs, "'", "'\\''")+"'"), 1)
	path := t.TempDir() + "/check"
	if err := os.WriteFile(path, mutated, 0700); err != nil {
		t.Fatal(err)
	}
	t.Cleanup(func() {
		if b, err := exec.Command("./build.sh").CombinedOutput(); err != nil {
			t.Errorf("restore normal binary: %v %s", err, b)
		}
	})
	cmd := exec.Command(path, "../spec/vectors/logs/12_bad_signature_tampered.jsonl")
	b, err := cmd.Output()
	exit, ok := err.(*exec.ExitError)
	if !ok || exit.ExitCode() != 1 {
		t.Fatalf("mutant exit: %v", err)
	}
	var v map[string]any
	if err := json.Unmarshal(b, &v); err != nil {
		t.Fatal(err)
	}
	if v["reason"] != "mutation_detected" {
		t.Fatalf("launcher mutation did not affect verdict: %s", b)
	}
}

var _ io.Reader = (*failAfterLine)(nil)
