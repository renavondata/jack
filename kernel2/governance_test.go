package main

import (
	"crypto/ed25519"
	"crypto/sha256"
	"fmt"
	"reflect"
	"strings"
	"testing"
)

func governanceBody(typ string) object {
	switch typ {
	case "amend":
		return object{"id": "A2", "charter": strings.Repeat("a", 64), "activate_at": jsonInteger(10)}
	case "push":
		return object{"digest": strings.Repeat("b", 64), "review": strings.Repeat("0", 64)}
	case "decision":
		return object{"kind": "transmute", "subject": "A2"}
	case "spec_conflict":
		return object{"section": "7", "text": "unresolved text"}
	}
	panic("unknown test type")
}

func nextTestEntry(state law, seq int64, typ string, body object, signer ed25519.PrivateKey) object {
	m := testEntry(typ, body)
	m["seq"], m["parent"] = jsonInteger(seq), state.head
	testSign(m, signer)
	return m
}

func foundingLaw(t *testing.T, private ed25519.PrivateKey) law {
	t.Helper()
	state := newLaw()
	if v := checkEntry(canonical(testGenesis(private)), 0, &state); v != nil {
		t.Fatal(v)
	}
	return state
}

func TestGovernanceSchemas(t *testing.T) {
	private := testPrivate("governance schemas")
	for _, typ := range []string{"amend", "push", "decision", "spec_conflict"} {
		t.Run(typ, func(t *testing.T) {
			state := foundingLaw(t, private)
			check := func(body object, reason string) {
				t.Helper()
				m := nextTestEntry(state, 1, typ, body, private)
				if reason != "" {
					m["sig"] = "AA==" // Body schema must precede container parsing.
				}
				v := checkEntry(canonical(m), 1, &state)
				if reason == "" && v != nil || reason != "" && v["reason"] != reason {
					t.Fatalf("body=%v: got %v, want %q", body, v, reason)
				}
			}
			for field := range governanceBody(typ) {
				body := governanceBody(typ)
				delete(body, field)
				check(body, "schema")
				for _, wrong := range []any{nil, true, object{}, []any{}} {
					body := governanceBody(typ)
					body[field] = wrong
					check(body, "schema")
				}
			}
			body := governanceBody(typ)
			body["extra.with.dot"] = object{"nested": []any{nil, true, jsonInteger(-1)}}
			check(body, "")
		})
	}
	for _, id := range []string{"A0", "B01", "Z999"} {
		body := governanceBody("amend")
		body["id"] = id
		if _, ok := bodyShape("amend", body); !ok {
			t.Fatalf("specified id pattern refused %q", id)
		}
	}
	for _, c := range []struct {
		typ, field string
		value      any
	}{
		{"amend", "id", "A"}, {"amend", "id", "A1234"}, {"amend", "id", "a2"},
		{"amend", "id", "A٢"}, {"amend", "id", "A2\n"}, {"amend", "id", "AA2"},
		{"amend", "activate_at", "10"}, {"amend", "charter", strings.Repeat("A", 64)},
		{"push", "digest", strings.Repeat("a", 63)}, {"push", "review", strings.Repeat("g", 64)},
		{"decision", "kind", "unknown"}, {"decision", "kind", "Transmute"}, {"decision", "subject", ""},
		{"spec_conflict", "section", ""}, {"spec_conflict", "text", ""},
	} {
		body := governanceBody(c.typ)
		body[c.field] = c.value
		if _, ok := bodyShape(c.typ, body); ok {
			t.Errorf("invalid %s.%s=%v accepted", c.typ, c.field, c.value)
		}
	}
}

func TestGovernanceSignaturePrecedence(t *testing.T) {
	private := testPrivate("governance signatures")
	for _, typ := range []string{"amend", "push", "decision", "spec_conflict"} {
		for _, reason := range []string{"bad_signature", "unknown_key", "proposer_mismatch", "no_power"} {
			t.Run(typ+"/"+reason, func(t *testing.T) {
				state := foundingLaw(t, private)
				m := nextTestEntry(state, 1, typ, governanceBody(typ), private)
				switch reason {
				case "bad_signature":
					m["ts"] = "2026-10-15T00:00:00Z"
				case "unknown_key":
					testSign(m, testPrivate("undeclared"))
				case "proposer_mismatch":
					m["proposer"] = "someone else"
				case "no_power":
					d := state.keys["root"]
					d.powers = []string{"genesis"}
					state.keys["root"] = d
					m["ts"] = "2026-10-15T00:00:00Z"
				}
				head := state.head
				if v := checkEntry(canonical(m), 1, &state); v["reason"] != reason {
					t.Fatalf("got %v, want %s", v, reason)
				}
				if state.head != head || len(state.amendments) != 0 || len(state.amendIDs) != 0 || len(state.transmuted) != 0 || state.promulgatedCharter != state.genesisCharter || state.trustedBase != strings.Repeat("0", 64) {
					t.Fatal("refused entry changed governance state")
				}
			})
		}
	}
}

func TestAmendmentConstraints(t *testing.T) {
	private := testPrivate("amendment constraints")
	state := foundingLaw(t, private)
	for _, height := range []jsonInteger{-1, 0, 1} {
		body := governanceBody("amend")
		body["activate_at"] = height
		m := nextTestEntry(state, 1, "amend", body, private)
		m["sig"] = "AA=="
		if v := checkEntry(canonical(m), 1, &state); v["reason"] != "schema" {
			t.Fatalf("activate_at=%d: %v", height, v)
		}
	}
	body := governanceBody("amend")
	body["activate_at"] = jsonInteger(2)
	if v := checkEntry(canonical(nextTestEntry(state, 1, "amend", body, private)), 1, &state); v != nil {
		t.Fatal(v)
	}
	for _, height := range []jsonInteger{3, 9007199254740991} {
		body := governanceBody("amend")
		body["activate_at"] = height
		m := nextTestEntry(state, 2, "amend", body, private)
		m["sig"] = "AA=="
		if v := checkEntry(canonical(m), 2, &state); v["reason"] != "schema" {
			t.Fatalf("duplicate id must fail before signature: %v", v)
		}
	}
	body = governanceBody("amend")
	body["id"], body["activate_at"] = "Z999", jsonInteger(9007199254740991)
	if v := checkEntry(canonical(nextTestEntry(state, 2, "amend", body, private)), 2, &state); v != nil {
		t.Fatal(v)
	}
}

func TestLawInForce(t *testing.T) {
	private := testPrivate("law in force")
	state := foundingLaw(t, private)
	zero := strings.Repeat("0", 64)
	if state.genesisCharter != zero || state.promulgatedCharter != zero || state.charterAt(1) != zero || state.trustedBase != zero {
		t.Fatal("genesis did not establish charter and trusted base")
	}
	seq := int64(1)
	accept := func(typ string, body object, signer ed25519.PrivateKey) {
		t.Helper()
		line := canonical(nextTestEntry(state, seq, typ, body, signer))
		if v := checkEntry(line, seq, &state); v != nil {
			t.Fatal(v)
		}
		if state.head != fmt.Sprintf("%x", sha256.Sum256(line)) {
			t.Fatal("head did not advance")
		}
		seq++
	}
	// A decision may use any currently empowered key, including a later key.
	delegate := testPrivate("later decision signer")
	accept("key", testDeclaration("delegate", delegate, "decision", "decision"), private)
	accept("decision", governanceBody("decision"), delegate)
	accept("decision", governanceBody("decision"), private)
	accept("decision", object{"kind": "transmute", "subject": "not an amendment id"}, private)
	if !reflect.DeepEqual(state.transmuted, map[string]bool{"A2": true, "not an amendment id": true}) {
		t.Fatalf("transmute set: %v", state.transmuted)
	}
	// No transmutation requirement or amendment freeze is imposed by the kernel.
	accept("amend", object{"id": "B1", "charter": strings.Repeat("1", 64), "activate_at": jsonInteger(12)}, private) // seq 5
	accept("amend", object{"id": "B2", "charter": strings.Repeat("2", 64), "activate_at": jsonInteger(9)}, private)  // seq 6
	accept("amend", object{"id": "B3", "charter": strings.Repeat("3", 64), "activate_at": jsonInteger(14)}, private) // seq 7
	if state.promulgatedCharter != strings.Repeat("3", 64) || state.charterAt(8) != zero {
		t.Fatal("promulgation and activation were conflated")
	}
	accept("push", governanceBody("push"), private) // seq 8, within pending amendments
	if state.trustedBase != strings.Repeat("b", 64) {
		t.Fatal("push did not update trusted base")
	}
	for _, c := range []struct {
		position int64
		charter  string
	}{{6, zero}, {8, zero}, {9, strings.Repeat("2", 64)}, {12, strings.Repeat("2", 64)}, {13, strings.Repeat("2", 64)}, {14, strings.Repeat("3", 64)}} {
		if got := state.charterAt(c.position); got != c.charter {
			t.Errorf("charter at %d: %s, want %s", c.position, got, c.charter)
		}
	}
	// Grant is a recorded decision, not a key declaration. All five other
	// decision kinds, proposals, merges and conflicts only advance the head.
	for _, kind := range []string{"veto", "promote", "budget", "grant", "fix"} {
		accept("decision", object{"kind": kind, "subject": " ", "powers": []any{"push"}}, private)
	}
	accept("proposal", object{"title": "", "commit": strings.Repeat("0", 40)}, private)
	accept("merge", object{"proposal": jsonInteger(9007199254740991), "commit": strings.Repeat("0", 40), "checker": strings.Repeat("f", 64)}, private)
	accept("spec_conflict", object{"section": " ", "text": " ", "digest": strings.Repeat("f", 64)}, private)
	if len(state.keys) != 2 || len(state.amendments) != 3 || len(state.amendIDs) != 3 || len(state.transmuted) != 2 || state.promulgatedCharter != strings.Repeat("3", 64) || state.trustedBase != strings.Repeat("b", 64) {
		t.Fatal("inert entry changed governance state")
	}
	accept("push", object{"digest": strings.Repeat("c", 64), "review": strings.Repeat("d", 64)}, private)
	if state.trustedBase != strings.Repeat("c", 64) {
		t.Fatal("latest push did not supersede trusted base")
	}
}
