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
	"path/filepath"
	"strings"
	"testing"
	"time"
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
	for _, depth := range []int{31, 32, 33, 100001} {
		for _, container := range []struct{ open, close string }{{"[", "]"}, {`{"a":`, "}"}} {
			line := `{"a":` + strings.Repeat(container.open, depth-1) + "0" + strings.Repeat(container.close, depth-1) + "}"
			want := ""
			if depth > 32 {
				want = "malformed_json"
			}
			if _, reason := parseCanonical([]byte(line)); reason != want {
				t.Fatalf("depth %d: got %s want %s", depth, reason, want)
			}
		}
	}
	long := strings.Repeat("9", 100000)
	for _, c := range []struct{ line, reason string }{
		{`{"a":` + long + `}`, "not_canonical"},
		{`{"a":-` + long + `}`, "not_canonical"},
		{`{"a":` + long + `,"b":"\ud800"}`, "malformed_json"},
		{`{"a":` + long + `,"b":` + strings.Repeat("[", 32) + `0` + strings.Repeat("]", 32) + `}`, "malformed_json"},
		{`{"a":` + long + `e}`, "malformed_json"},
	} {
		if _, reason := parseCanonical([]byte(c.line)); reason != c.reason {
			t.Fatalf("long-number precedence: got %s want %s", reason, c.reason)
		}
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
	m := testEntry("genesis", object{"charter": strings.Repeat("0", 64), "checker": strings.Repeat("0", 64), "keys": []any{testDeclaration("root", private, "genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict", "forecast", "resolution")}})
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
	// Ownership survives rotation, but the same identity may restore its key.
	reused := appendEntry(rotated, 2, "key", testDeclaration("old_id", old, "proposal"), replacement)
	testReason(t, reused, "bad_key", 2)
	lostOnRestore := appendEntry(rotated, 2, "key", testDeclaration("root", old, "proposal"), replacement)
	testReason(t, lostOnRestore, "bad_key", 2)
	restored := appendEntry(rotated, 2, "key", testDeclaration("root", old, "key", "proposal"), replacement)
	testReason(t, appendEntry(restored, 3, "proposal", proposal, old), "", 0)
	// Losing the last key power is refused for key entries, while dropping other powers is allowed.
	testReason(t, appendEntry(rotated, 2, "key", testDeclaration("root", replacement), replacement), "bad_key", 2)
	testReason(t, appendEntry(rotated, 2, "key", testDeclaration("root", replacement, "proposal"), replacement), "bad_key", 2)
	narrowed := appendEntry(rotated, 2, "key", testDeclaration("root", replacement, "key"), replacement)
	testReason(t, narrowed, "", 0)
	testReason(t, appendEntry(narrowed, 3, "proposal", proposal, replacement), "no_power", 3)
	testReason(t, appendEntry(narrowed, 3, "proposal", proposal, old), "unknown_key", 3)
	// Full self-revocation is allowed once another declared key holds key power.
	backup := testPrivate("backup")
	withBackup := appendEntry(rotated, 2, "key", testDeclaration("backup", backup, "key"), replacement)
	revoked := appendEntry(withBackup, 3, "key", testDeclaration("root", replacement), replacement)
	testReason(t, revoked, "", 0)
	testReason(t, appendEntry(revoked, 4, "key", testDeclaration("root", replacement, "key"), replacement), "no_power", 4)
	testReason(t, appendEntry(revoked, 4, "key", testDeclaration("backup", backup), backup), "bad_key", 4)
	// Genesis is never refused for declaring no key with the key power.
	noKeyPowerGenesis := testEntry("genesis", object{"charter": strings.Repeat("0", 64), "checker": strings.Repeat("0", 64), "keys": []any{testDeclaration("root", old, "genesis")}})
	testSign(noKeyPowerGenesis, old)
	testReason(t, canonical(noKeyPowerGenesis), "", 0)
	// Within §7 / §8 step 9, weakness is tested first, then ownership, then last key power;
	// refusing a key entry leaves keys and byBlob unchanged.
	state := foundingLaw(t, old)
	weakDecl := declaration{id: "root", principal: "tester", blob: append(wireString([]byte("ssh-ed25519")), wireString(encodePoint(identity()))...), public: encodePoint(identity()), powers: nil}
	if got := state.declare(weakDecl, true); got != "weak public key" {
		t.Fatalf("weakness precedence: got %q", got)
	}
	otherDecl, ok := keyShape(testDeclaration("other", replacement, "key"))
	if !ok || state.declare(otherDecl, true) != "" {
		t.Fatal("failed to register second key")
	}
	dupAndLose := declaration{id: "other", principal: "tester", blob: state.keys["root"].blob, public: state.keys["root"].public, powers: nil}
	if got := state.declare(dupAndLose, true); got != "public key already declared under another key_id" {
		t.Fatalf("ownership precedence: got %q", got)
	}
	unowned := testPrivate("unowned")
	unownedDecl, ok := keyShape(testDeclaration("other", unowned))
	if !ok || state.declare(unownedDecl, true) != "" {
		t.Fatal("failed to drop key power from second key while root still holds key")
	}
	fresh := testPrivate("fresh")
	loseLast, ok := keyShape(testDeclaration("root", fresh))
	if !ok {
		t.Fatal("bad test declaration")
	}
	if got := state.declare(loseLast, true); got != "no declared key would hold key power" {
		t.Fatalf("last key power check: got %q", got)
	}
	if _, owned := state.byBlob[string(loseLast.blob)]; owned || !bytes.Equal(state.keys["root"].blob, testPublicBlob(old)) {
		t.Fatal("refused declaration mutated key state")
	}
}

func TestContainerBoundaries(t *testing.T) {
	m := testGenesis(testPrivate("containers"))
	b, err := base64.StdEncoding.DecodeString(m["sig"].(string))
	if err != nil {
		t.Fatal(err)
	}
	for i := 0; i < len(b); i++ {
		if _, ok := parseSignature(base64.StdEncoding.EncodeToString(b[:i])); ok {
			t.Fatalf("truncation %d accepted", i)
		}
	}
	bad := append(append([]byte(nil), b...), 0)
	if _, ok := parseSignature(base64.StdEncoding.EncodeToString(bad)); ok {
		t.Fatal("trailing byte accepted")
	}
	bad = append([]byte(nil), b...)
	binary.BigEndian.PutUint32(bad[10:14], ^uint32(0))
	if _, ok := parseSignature(base64.StdEncoding.EncodeToString(bad)); ok {
		t.Fatal("oversized wire length accepted")
	}
	for _, text := range []string{"A", "AAA", "AA=", "AA===", "AA==\n", "AA==\r", "AA-A", "AA_A", "AA==AA==", "AB==", strings.Repeat("A", 238) + "=="} {
		if _, ok := parseSignature(text); ok {
			t.Fatalf("bad base64 %q accepted", text)
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

func TestTimestamps(t *testing.T) {
	private := testPrivate("timestamps")
	for _, timestamp := range []string{"2026-02-30T00:00:00Z", "1900-02-29T00:00:00Z", "2026-12-31T23:59:60Z", "0000-01-01T00:00:00Z", "٢٠٢٦-10-14T00:00:00Z", "2026-00-01T00:00:00Z", "2026-13-01T00:00:00Z", "2026-01-00T00:00:00Z", "2026-01-01T24:00:00Z", "2026-01-01T00:60:00Z"} {
		m := testGenesis(private)
		m["ts"] = timestamp
		testReason(t, canonical(m), "schema", 0)
	}
	for _, timestamp := range []string{"0001-01-01T00:00:00Z", "9999-12-31T23:59:59Z", "2000-02-29T00:00:00Z", "2024-02-29T00:00:00Z"} {
		m := testGenesis(private)
		m["ts"] = timestamp
		testSign(m, private)
		testReason(t, canonical(m), "", 0)
	}
}

func TestKeyDeclarationText(t *testing.T) {
	private := testPrivate("public text")
	valid := testDeclaration("root", private)["pubkey"].(string)
	for _, text := range []string{
		" " + valid, valid + " ", strings.Replace(valid, " ", "  ", 1),
		strings.Replace(valid, " ", "\t", 1), strings.Replace(valid, " ", "\u00a0", 1),
		valid + "\n", valid + "=", "ssh-ed25519 AB==",
		valid[:len(valid)-2] + "==", valid + "AAAA",
	} {
		m := testGenesis(private)
		m["body"].(object)["keys"].([]any)[0].(object)["pubkey"] = text
		testReason(t, canonical(m), "schema", 0)
	}
	for _, text := range []string{"AB==", "AA==", strings.Repeat("A", 238) + "=="} {
		m := testGenesis(private)
		m["sig"] = text
		testReason(t, canonical(m), "bad_signature", 0)
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
	info, err := os.Stat(".cache/check")
	if err != nil {
		t.Fatal(err)
	}
	newer := info.ModTime().Add(time.Second)
	if err := os.Chtimes(path, newer, newer); err != nil {
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

func TestLauncherBuildFreshness(t *testing.T) {
	dir := t.TempDir()
	sources := []string{"check", "build.sh", "main.go", "canonical.go", "ed25519.go", "signature.go", "checker.go"}
	for _, name := range sources {
		b, err := os.ReadFile(name)
		if err != nil {
			t.Fatal(err)
		}
		if err := os.WriteFile(filepath.Join(dir, name), b, 0700); err != nil {
			t.Fatal(err)
		}
	}
	log := filepath.Join(dir, "empty.jsonl")
	if err := os.WriteFile(log, nil, 0600); err != nil {
		t.Fatal(err)
	}
	launch := func() {
		t.Helper()
		b, err := exec.Command(filepath.Join(dir, "check"), log).CombinedOutput()
		if err != nil || string(b) != "{\"entries\":0,\"ok\":true}\n" {
			t.Fatalf("launcher: %v %s", err, b)
		}
	}
	binary := filepath.Join(dir, ".cache/check")
	mtime := func() time.Time {
		t.Helper()
		info, err := os.Stat(binary)
		if err != nil {
			t.Fatal(err)
		}
		return info.ModTime()
	}
	launch() // Missing binary must build.
	built := mtime()
	launch()
	if !mtime().Equal(built) {
		t.Fatal("unchanged sources rebuilt")
	}
	// Equal timestamps are not newer. A test file is not a binary source.
	for _, name := range sources {
		if err := os.Chtimes(filepath.Join(dir, name), built, built); err != nil {
			t.Fatal(err)
		}
	}
	if err := os.WriteFile(filepath.Join(dir, "ignored_test.go"), []byte("package main\n"), 0600); err != nil {
		t.Fatal(err)
	}
	launch()
	if !mtime().Equal(built) {
		t.Fatal("equal timestamps or unrelated test file triggered rebuild")
	}
	// Keep all sources older than the binary except one, in turn.
	for _, changed := range sources {
		for _, name := range sources {
			old := built.Add(-2 * time.Hour)
			if err := os.Chtimes(filepath.Join(dir, name), old, old); err != nil {
				t.Fatal(err)
			}
		}
		stale := built.Add(-time.Hour)
		if err := os.Chtimes(binary, stale, stale); err != nil {
			t.Fatal(err)
		}
		if err := os.Chtimes(filepath.Join(dir, changed), built, built); err != nil {
			t.Fatal(err)
		}
		launch()
		if mtime().Equal(stale) {
			t.Fatalf("newer %s did not trigger rebuild", changed)
		}
	}
}

var _ io.Reader = (*failAfterLine)(nil)
