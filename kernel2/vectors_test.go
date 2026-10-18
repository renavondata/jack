package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"reflect"
	"strings"
	"testing"
)

func vectorJSON(t *testing.T, path string, dst any) {
	t.Helper()
	b, err := os.ReadFile(path)
	if os.IsNotExist(err) && strings.HasPrefix(path, "../tests/vectors/") {
		t.Skipf("optional referenced vector file is absent from this room: %s", path)
	}
	if err != nil {
		t.Fatal(err)
	}
	if err := json.Unmarshal(b, dst); err != nil {
		t.Fatal(err)
	}
}

func unhex(t *testing.T, s string) []byte {
	t.Helper()
	b, err := hex.DecodeString(s)
	if err != nil {
		t.Fatal(err)
	}
	return b
}

func TestCanonicalVectors(t *testing.T) {
	var vectors struct {
		Canonical []struct {
			Value             json.RawMessage
			Canonical, SHA256 string
		}
		Refused       []struct{ Line, Reason string } `json:"refused_lines"`
		GenesisParent string                          `json:"genesis_parent"`
	}
	vectorJSON(t, "../spec/vectors/canonical.json", &vectors)
	for i, v := range vectors.Canonical {
		t.Run(fmt.Sprintf("canonical_%d", i), func(t *testing.T) {
			p := jsonParser{b: v.Value}
			value, err := p.value()
			p.space()
			if err != nil || p.i != len(v.Value) {
				t.Fatalf("parse value: %v", err)
			}
			encoded := canonical(value)
			if string(encoded) != v.Canonical {
				t.Fatalf("got %s, want %s", encoded, v.Canonical)
			}
			if got := fmt.Sprintf("%x", sha256.Sum256(encoded)); got != v.SHA256 {
				t.Fatalf("hash: %s", got)
			}
			if _, reason := parseCanonical(encoded); reason != "" {
				t.Fatal(reason)
			}
		})
	}
	for i, v := range vectors.Refused {
		t.Run(fmt.Sprintf("refused_%d", i), func(t *testing.T) {
			if _, reason := parseCanonical([]byte(v.Line)); reason != v.Reason {
				t.Fatalf("got %s, want %s", reason, v.Reason)
			}
		})
	}
	if vectors.GenesisParent != strings.Repeat("0", 64) {
		t.Fatal("genesis parent vector differs")
	}
	t.Logf("canonical vectors: %d encodings + hashes, %d refusals, 1 genesis parent", len(vectors.Canonical), len(vectors.Refused))
}

func TestEd25519Vectors(t *testing.T) {
	for _, file := range []string{"rfc8032.json", "speccheck.json"} {
		t.Run(file, func(t *testing.T) {
			var data struct {
				Vectors []struct {
					Name, Message, Signature string
					PublicKey                string `json:"public_key"`
					PubKey                   string `json:"pub_key"`
					Expected                 *bool
				}
			}
			vectorJSON(t, "../tests/vectors/"+file, &data)
			for i, v := range data.Vectors {
				t.Run(fmt.Sprint(i), func(t *testing.T) {
					key := v.PublicKey
					if key == "" {
						key = v.PubKey
					}
					want := true
					if v.Expected != nil {
						want = *v.Expected
					}
					if got := verifyEd25519(unhex(t, key), unhex(t, v.Message), unhex(t, v.Signature)); got != want {
						t.Fatalf("verify=%v, want %v", got, want)
					}
					if file == "rfc8032.json" && weakKey(unhex(t, key)) {
						t.Fatal("RFC public key classified weak")
					}
				})
			}
			t.Logf("%s: %d signature verdicts", file, len(data.Vectors))
		})
	}
}

func TestWeakKeyVectors(t *testing.T) {
	var vectors map[string]json.RawMessage
	vectorJSON(t, "../tests/vectors/weak_keys.json", &vectors)
	count := 0
	for _, group := range []string{"small_order", "non_canonical"} {
		var keys []struct {
			Name      string
			PublicKey string `json:"pub_key"`
		}
		if err := json.Unmarshal(vectors[group], &keys); err != nil {
			t.Fatal(err)
		}
		for _, key := range keys {
			t.Run(key.Name, func(t *testing.T) {
				if !weakKey(unhex(t, key.PublicKey)) {
					t.Fatal("weak key admitted")
				}
			})
		}
		count += len(keys)
	}
	t.Logf("weak keys: %d/%d refused", count, count)
}

func loadVerdicts(t *testing.T, directory string) map[string]map[string]any {
	t.Helper()
	var data struct{ Verdicts map[string]map[string]any }
	vectorJSON(t, filepath.Join(directory, "verdicts.json"), &data)
	return data.Verdicts
}

func normalizeVerdict(t *testing.T, v map[string]any) map[string]any {
	t.Helper()
	b, err := json.Marshal(v)
	if err != nil {
		t.Fatal(err)
	}
	var out map[string]any
	if err := json.Unmarshal(b, &out); err != nil {
		t.Fatal(err)
	}
	delete(out, "detail")
	return out
}

func TestLogVectors(t *testing.T) {
	testLogVectors(t, "../spec/vectors")
}

func testLogVectors(t *testing.T, directory string) {
	t.Helper()
	wants := loadVerdicts(t, directory)
	files, err := filepath.Glob(filepath.Join(directory, "logs", "*"))
	if err != nil {
		t.Fatal(err)
	}
	if len(files) != len(wants) {
		t.Fatalf("%d logs but %d verdicts", len(files), len(wants))
	}
	for _, path := range files {
		t.Run(filepath.Base(path), func(t *testing.T) {
			want, exists := wants[filepath.Base(path)]
			if !exists {
				t.Fatal("log missing expected verdict")
			}
			b, err := os.ReadFile(path)
			if err != nil {
				t.Fatal(err)
			}
			got, err := checkLog(bytes.NewReader(b))
			if err != nil {
				t.Fatal(err)
			}
			if !reflect.DeepEqual(normalizeVerdict(t, got), want) {
				t.Fatalf("got %v, want %v", got, want)
			}
			// Exercise the actual executable, stdout shape, and exit status too.
			cmd := exec.Command("./check", path)
			var stdout, stderr bytes.Buffer
			cmd.Stdout, cmd.Stderr = &stdout, &stderr
			err = cmd.Run()
			code := 0
			if err != nil {
				e, ok := err.(*exec.ExitError)
				if !ok {
					t.Fatal(err)
				}
				code = e.ExitCode()
			}
			wantCode := 1
			if want["ok"] == true {
				wantCode = 0
			}
			if code != wantCode {
				t.Fatalf("exit=%d want=%d stderr=%s", code, wantCode, stderr.String())
			}
			var actual map[string]any
			if err := json.Unmarshal(stdout.Bytes(), &actual); err != nil {
				t.Fatalf("stdout must be exactly one JSON object: %v; %s", err, stdout.String())
			}
			if wantCode == 1 {
				if _, ok := actual["detail"].(string); !ok {
					t.Fatal("missing string detail")
				}
			}
			delete(actual, "detail")
			if !reflect.DeepEqual(actual, want) {
				t.Fatalf("CLI got %v, want %v", actual, want)
			}
			if wantCode == 1 {
				// Refusal must be prefix-stable, even with malformed UTF-8 appended.
				prefix := append(append([]byte(nil), b...), '\n', 0xff)
				got, err := checkLog(bytes.NewReader(prefix))
				if err != nil {
					t.Fatal(err)
				}
				if !reflect.DeepEqual(normalizeVerdict(t, got), want) {
					t.Fatal("appending changed first refusal")
				}
			}
		})
	}
	t.Logf("log verdicts: %d/%d compared, in-process and through kernel2/check", len(files), len(wants))
}

func TestSSHKeygenDifferences(t *testing.T) {
	var data struct {
		Differences []struct{ Name, Kernel string }
	}
	vectorJSON(t, "../tests/vectors/ssh_keygen_differences.json", &data)
	logs := map[string]string{"s_plus_L": "13_bad_signature_s_plus_L.jsonl", "reserved_nonempty": "15_bad_signature_reserved.jsonl"}
	for _, difference := range data.Differences {
		t.Run(difference.Name, func(t *testing.T) {
			file, ok := logs[difference.Name]
			if !ok {
				t.Fatal("unexercised named difference")
			}
			if !strings.Contains(difference.Kernel, "bad_signature") {
				t.Fatal("unrecognized expected outcome")
			}
			b, err := os.ReadFile("../spec/vectors/logs/" + file)
			if err != nil {
				t.Fatal(err)
			}
			v, err := checkLog(bytes.NewReader(b))
			if err != nil {
				t.Fatal(err)
			}
			if v["ok"] != false || v["reason"] != "bad_signature" {
				t.Fatalf("got %v", v)
			}
		})
	}
	t.Logf("ssh-keygen differences: %d/%d exercised via signed log fixtures", len(data.Differences), len(data.Differences))
}

func TestStandardLibraryComparison(t *testing.T) {
	// Deterministic, ordinary prime-order keys only. Edge-case decisions are
	// tested against SPEC vectors, never crypto/ed25519's acceptance behaviour.
	for i := 0; i < 32; i++ {
		seed := sha256.Sum256([]byte(fmt.Sprintf("kernel2 independent comparison %d", i)))
		private := ed25519.NewKeyFromSeed(seed[:])
		public := private.Public().(ed25519.PublicKey)
		message := bytes.Repeat([]byte{byte(i)}, i*17)
		sig := ed25519.Sign(private, message)
		if !ed25519.Verify(public, message, sig) || !verifyEd25519(public, message, sig) || weakKey(public) {
			t.Fatalf("ordinary valid signature %d failed", i)
		}
		sig[i%64] ^= 1
		if ed25519.Verify(public, message, sig) || verifyEd25519(public, message, sig) {
			t.Fatalf("tampered signature %d passed", i)
		}
	}
}
