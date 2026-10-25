package main

import (
	"bytes"
	"crypto/ed25519"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
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
	case "forecast":
		return object{"claim": "F1", "p": jsonInteger(500), "resolves_by": "2026-10-16T00:00:00Z"}
	case "resolution":
		return object{"forecast": jsonInteger(1), "outcome": jsonInteger(1), "evidence": "verified"}
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
	other := testPrivate("governance schemas other")
	for _, typ := range []string{"amend", "push", "decision", "spec_conflict", "forecast", "resolution"} {
		t.Run(typ, func(t *testing.T) {
			baseState := foundingLaw(t, private)
			seq := int64(1)
			if typ == "resolution" {
				// Seed an unresolved forecast at seq 1 by another principal so valid resolutions pass.
				d, ok := keyShape(testDeclaration("other", other, "forecast"))
				if !ok {
					t.Fatal("bad test key")
				}
				d.principal = "other"
				if detail := baseState.declare(d, true); detail != "" {
					t.Fatal(detail)
				}
				f := nextTestEntry(baseState, 1, "forecast", governanceBody("forecast"), other)
				f["proposer"] = "other"
				testSign(f, other)
				if v := checkEntry(canonical(f), 1, &baseState); v != nil {
					t.Fatal(v)
				}
				seq = 2
			}
			check := func(body object, reason string) {
				t.Helper()
				state := baseState
				state.forecasts = map[int64]string{}
				for k, v := range baseState.forecasts {
					state.forecasts[k] = v
				}
				state.resolved = map[int64]bool{}
				for k, v := range baseState.resolved {
					state.resolved[k] = v
				}
				m := nextTestEntry(state, seq, typ, body, private)
				if reason != "" {
					m["sig"] = "AA==" // Body schema must precede container parsing.
				}
				v := checkEntry(canonical(m), seq, &state)
				if reason == "" && v != nil || reason != "" && v["reason"] != reason {
					t.Fatalf("body=%v: got %v, want %q", body, v, reason)
				}
			}
			for field := range governanceBody(typ) {
				body := governanceBody(typ)
				delete(body, field)
				check(body, "schema")
				for _, wrong := range []any{nil, true, false, object{}, []any{}} {
					body := governanceBody(typ)
					body[field] = wrong
					check(body, "schema")
				}
			}
			body := governanceBody(typ)
			body["extra.with.dot"] = object{"nested": []any{nil, true, jsonInteger(-1)}}
			if typ == "forecast" {
				body["type"] = "world.screen"
				body["args"] = object{"window": jsonInteger(7)}
			}
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
	for _, p := range []jsonInteger{1, 500, 999} {
		body := governanceBody("forecast")
		body["p"] = p
		if _, ok := bodyShape("forecast", body); !ok {
			t.Fatalf("valid forecast p=%d refused", p)
		}
	}
	for _, outcome := range []jsonInteger{0, 1} {
		body := governanceBody("resolution")
		body["outcome"] = outcome
		if _, ok := bodyShape("resolution", body); !ok {
			t.Fatalf("valid resolution outcome=%d refused", outcome)
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
		{"forecast", "claim", ""}, {"forecast", "p", jsonInteger(0)}, {"forecast", "p", jsonInteger(1000)},
		{"forecast", "p", jsonInteger(-1)}, {"forecast", "p", true}, {"forecast", "p", false},
		{"forecast", "p", "500"}, {"forecast", "resolves_by", "2026-02-30T00:00:00Z"},
		{"forecast", "resolves_by", "not-a-timestamp"},
		{"resolution", "forecast", jsonInteger(-1)}, {"resolution", "forecast", true}, {"resolution", "forecast", "1"},
		{"resolution", "outcome", jsonInteger(-1)}, {"resolution", "outcome", jsonInteger(2)},
		{"resolution", "outcome", true}, {"resolution", "outcome", false}, {"resolution", "outcome", "1"},
		{"resolution", "evidence", ""},
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
	other := testPrivate("governance signatures other")
	for _, typ := range []string{"amend", "push", "decision", "spec_conflict", "forecast", "resolution"} {
		for _, reason := range []string{"bad_signature", "unknown_key", "proposer_mismatch", "no_power"} {
			t.Run(typ+"/"+reason, func(t *testing.T) {
				state := foundingLaw(t, private)
				seq := int64(1)
				if typ == "resolution" {
					d, ok := keyShape(testDeclaration("other", other, "forecast"))
					if !ok {
						t.Fatal("bad test key")
					}
					d.principal = "other"
					if detail := state.declare(d, true); detail != "" {
						t.Fatal(detail)
					}
					f := nextTestEntry(state, 1, "forecast", governanceBody("forecast"), other)
					f["proposer"] = "other"
					testSign(f, other)
					if v := checkEntry(canonical(f), 1, &state); v != nil {
						t.Fatal(v)
					}
					seq = 2
				}
				m := nextTestEntry(state, seq, typ, governanceBody(typ), private)
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
				head, prevTS := state.head, state.prevTS
				if v := checkEntry(canonical(m), seq, &state); v["reason"] != reason {
					t.Fatalf("got %v, want %s", v, reason)
				}
				if state.head != head || state.prevTS != prevTS || len(state.amendments) != 0 || len(state.amendIDs) != 0 || len(state.transmuted) != 0 || len(state.resolved) != 0 || (typ != "resolution" && len(state.forecasts) != 0) || state.promulgatedCharter != state.genesisCharter || state.trustedBase != strings.Repeat("0", 64) {
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

func TestC1aSignedLogs(t *testing.T) {
	alice1 := testPrivate("c1a alice 1")
	alice2 := testPrivate("c1a alice 2")
	bob := testPrivate("c1a bob")

	decl := func(id, principal string, priv ed25519.PrivateKey, powers ...string) object {
		ps := make([]any, len(powers))
		for i, p := range powers {
			ps[i] = p
		}
		return object{
			"key_id":    id,
			"principal": principal,
			"powers":    ps,
			"pubkey":    "ssh-ed25519 " + base64.StdEncoding.EncodeToString(testPublicBlob(priv)),
		}
	}

	allPowers := []string{"genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict", "forecast", "resolution"}
	genesisObj := func() object {
		m := object{
			"seq":      jsonInteger(0),
			"parent":   strings.Repeat("0", 64),
			"ts":       "2026-10-25T12:00:00Z",
			"type":     "genesis",
			"proposer": "alice",
			"body": object{
				"charter": strings.Repeat("1", 64),
				"checker": strings.Repeat("2", 64),
				"keys": []any{
					decl("alice-1", "alice", alice1, allPowers...),
					decl("alice-2", "alice", alice2, "forecast", "resolution"),
					decl("bob-1", "bob", bob, "forecast", "resolution", "proposal"),
				},
			},
		}
		testSign(m, alice1)
		return m
	}

	buildLog := func(entries ...object) []byte {
		var lines [][]byte
		for i, m := range entries {
			if i > 0 {
				m["parent"] = fmt.Sprintf("%x", sha256.Sum256(lines[i-1]))
			}
			lines = append(lines, canonical(m))
		}
		return append(bytes.Join(lines, []byte{'\n'}), '\n')
	}

	signedEntry := func(seq int64, ts, typ, proposer string, body object, signer ed25519.PrivateKey, parent []byte) object {
		m := object{
			"seq":      jsonInteger(seq),
			"parent":   fmt.Sprintf("%x", sha256.Sum256(parent)),
			"ts":       ts,
			"type":     typ,
			"proposer": proposer,
			"body":     body,
		}
		testSign(m, signer)
		return m
	}

	g := genesisObj()
	gBytes := canonical(g)

	f1 := signedEntry(1, "2026-10-25T12:01:00Z", "forecast", "alice", object{
		"claim":       "both checkers agree on 10^5 seeded logs",
		"p":           jsonInteger(990),
		"resolves_by": "2026-10-26T00:00:00Z",
		"type":        "world.screen",
		"args":        object{"seeds": jsonInteger(100000)},
	}, alice1, gBytes)
	f1Bytes := canonical(f1)

	r1Valid := signedEntry(2, "2026-10-25T12:02:00Z", "resolution", "bob", object{
		"forecast": jsonInteger(1),
		"outcome":  jsonInteger(1),
		"evidence": "run of record",
	}, bob, f1Bytes)
	r1ValidBytes := canonical(r1Valid)

	r1Self := signedEntry(2, "2026-10-25T12:02:00Z", "resolution", "alice", object{
		"forecast": jsonInteger(1),
		"outcome":  jsonInteger(1),
		"evidence": "self-resolved by same key",
	}, alice1, f1Bytes)

	r1SelfSecondKey := signedEntry(2, "2026-10-25T12:02:00Z", "resolution", "alice", object{
		"forecast": jsonInteger(1),
		"outcome":  jsonInteger(0),
		"evidence": "self-resolved by second key of same principal",
	}, alice2, f1Bytes)

	rDangling := signedEntry(1, "2026-10-25T12:01:00Z", "resolution", "bob", object{
		"forecast": jsonInteger(0),
		"outcome":  jsonInteger(1),
		"evidence": "genesis is not a forecast",
	}, bob, gBytes)

	rDouble := signedEntry(3, "2026-10-25T12:03:00Z", "resolution", "alice", object{
		"forecast": jsonInteger(1),
		"outcome":  jsonInteger(0),
		"evidence": "already resolved (even when self-resolved)",
	}, alice1, r1ValidBytes)

	fPast := signedEntry(1, "2026-10-25T12:01:00Z", "forecast", "alice", object{
		"claim":       "past resolves_by",
		"p":           jsonInteger(500),
		"resolves_by": "2026-10-25T12:00:59Z",
	}, alice1, gBytes)

	fEqualResolvesBy := signedEntry(1, "2026-10-25T12:01:00Z", "forecast", "alice", object{
		"claim":       "equal resolves_by is not earlier than ts",
		"p":           jsonInteger(1),
		"resolves_by": "2026-10-25T12:01:00Z",
	}, alice1, gBytes)

	fPermille0 := signedEntry(1, "2026-10-25T12:01:00Z", "forecast", "alice", object{
		"claim":       "p=0 out of range",
		"p":           jsonInteger(0),
		"resolves_by": "2026-10-25T12:01:00Z",
	}, alice1, gBytes)

	fPermille1000 := signedEntry(1, "2026-10-25T12:01:00Z", "forecast", "alice", object{
		"claim":       "p=1000 out of range",
		"p":           jsonInteger(1000),
		"resolves_by": "2026-10-25T12:01:00Z",
	}, alice1, gBytes)

	fBool := signedEntry(1, "2026-10-25T12:01:00Z", "forecast", "alice", object{
		"claim":       "boolean p is not an integer",
		"p":           true,
		"resolves_by": "2026-10-25T12:01:00Z",
	}, alice1, gBytes)

	rOutcomeBool := signedEntry(2, "2026-10-25T12:02:00Z", "resolution", "bob", object{
		"forecast": jsonInteger(1),
		"outcome":  true,
		"evidence": "boolean outcome is not an integer",
	}, bob, f1Bytes)

	tsDecreased := signedEntry(1, "2026-10-25T11:59:59Z", "forecast", "alice", object{
		"claim":       "ts earlier than previous entry",
		"p":           jsonInteger(500),
		"resolves_by": "2026-10-25T12:00:00Z",
	}, alice1, gBytes)

	tsDecreasedBeforeBadSeq := object{
		"seq":      jsonInteger(99),
		"parent":   strings.Repeat("f", 64),
		"ts":       "2026-10-25T11:59:59Z",
		"type":     "genesis",
		"proposer": "",
		"body":     object{},
		"sig":      "AA==",
	}

	rSelfBadSig := signedEntry(2, "2026-10-25T12:02:00Z", "resolution", "alice", object{
		"forecast": jsonInteger(1),
		"outcome":  jsonInteger(1),
		"evidence": "tampered after signing",
	}, alice1, f1Bytes)
	rSelfBadSig["body"].(object)["evidence"] = "tampered payload"

	cases := []struct {
		name    string
		witness string
		log     []byte
		ok      bool
		entries int64
		seq     int64
		reason  string
	}{
		{
			name:    "40_forecast_valid",
			witness: "SPEC.md §4 (type forecast), §5 (forecast schema + optional type/args), §7 & §8 step 9 (record forecast seq -> proposer)",
			log:     buildLog(g, f1),
			ok:      true,
			entries: 2,
		},
		{
			name:    "40b_forecast_equal_resolves_by_valid",
			witness: "SPEC.md §5 (resolves_by not earlier than entry's own ts; p=1 lower bound) & §7 (equal ts does not decrease)",
			log:     buildLog(g, fEqualResolvesBy),
			ok:      true,
			entries: 2,
		},
		{
			name:    "41_resolution_valid",
			witness: "SPEC.md §4 (type resolution), §5 (resolution schema), §7 & §8 step 9 (mark forecast resolved)",
			log:     buildLog(g, f1, r1Valid),
			ok:      true,
			entries: 3,
		},
		{
			name:    "42_resolution_self_bad",
			witness: "SPEC.md §7 & §8 step 8a: A resolution whose proposer equals the recorded proposer of its forecast is self_judged",
			log:     buildLog(g, f1, r1Self),
			ok:      false,
			seq:     2,
			reason:  "self_judged",
		},
		{
			name:    "42b_resolution_self_second_key_bad",
			witness: "SPEC.md §7: judged by principal so that two keys of one party cannot launder a judgement",
			log:     buildLog(g, f1, r1SelfSecondKey),
			ok:      false,
			seq:     2,
			reason:  "self_judged",
		},
		{
			name:    "43_resolution_dangling_bad",
			witness: "SPEC.md §7 & §8 step 7: A resolution whose forecast is not a recorded forecast seq is schema (before the signature)",
			log:     buildLog(g, rDangling),
			ok:      false,
			seq:     1,
			reason:  "schema",
		},
		{
			name:    "44_resolution_double_bad",
			witness: "SPEC.md §7 & §8 step 7: A resolution whose forecast is already resolved is schema; a self-resolution of an already-resolved forecast is schema",
			log:     buildLog(g, f1, r1Valid, rDouble),
			ok:      false,
			seq:     3,
			reason:  "schema",
		},
		{
			name:    "45_forecast_past_bad",
			witness: "SPEC.md §5 & §8 step 7: For forecast, resolves_by earlier than ts -> schema",
			log:     buildLog(g, fPast),
			ok:      false,
			seq:     1,
			reason:  "schema",
		},
		{
			name:    "46a_forecast_permille_0_bad",
			witness: "SPEC.md §5: forecast.p integer 1-999 (0 refused as schema)",
			log:     buildLog(g, fPermille0),
			ok:      false,
			seq:     1,
			reason:  "schema",
		},
		{
			name:    "46b_forecast_permille_1000_bad",
			witness: "SPEC.md §5: forecast.p integer 1-999 (1000 refused as schema)",
			log:     buildLog(g, fPermille1000),
			ok:      false,
			seq:     1,
			reason:  "schema",
		},
		{
			name:    "47_forecast_boolean_bad",
			witness: "SPEC.md §5: forecast.p integer 1-999 (a boolean is not an integer -> schema)",
			log:     buildLog(g, fBool),
			ok:      false,
			seq:     1,
			reason:  "schema",
		},
		{
			name:    "47b_resolution_outcome_boolean_bad",
			witness: "SPEC.md §5: resolution.outcome integer 0 or 1 (a boolean is not an integer -> schema)",
			log:     buildLog(g, f1, rOutcomeBool),
			ok:      false,
			seq:     2,
			reason:  "schema",
		},
		{
			name:    "48_ts_decreased_bad",
			witness: "SPEC.md §7 & §8 step 2a: entry i's ts is not earlier than entry i-1's -> ts_decreased",
			log:     buildLog(g, tsDecreased),
			ok:      false,
			seq:     1,
			reason:  "ts_decreased",
		},
		{
			name:    "48b_ts_decreased_precedes_bad_seq",
			witness: "SPEC.md §8 step 2a precedes step 3 (bad_seq), step 4 (parent_mismatch), step 5 (genesis_misplaced), step 6 (no_proposer), step 7 (schema), step 8 (bad_signature)",
			log:     append(append([]byte(nil), gBytes...), append([]byte{'\n'}, canonical(tsDecreasedBeforeBadSeq)...)...),
			ok:      false,
			seq:     1,
			reason:  "ts_decreased",
		},
		{
			name:    "49_self_resolution_bad_signature",
			witness: "SPEC.md §7 & §8 steps 8-8a: A self-resolution with a bad signature is bad_signature, not self_judged",
			log:     append(append(append([]byte(nil), gBytes...), '\n'), append(append([]byte(nil), f1Bytes...), append([]byte{'\n'}, canonical(rSelfBadSig)...)...)...),
			ok:      false,
			seq:     2,
			reason:  "bad_signature",
		},
	}

	tmpDir := t.TempDir()
	for _, tc := range cases {
		t.Run(tc.name, func(t *testing.T) {
			t.Logf("witnesses %s", tc.witness)
			got, err := checkLog(bytes.NewReader(tc.log))
			if err != nil {
				t.Fatal(err)
			}
			if tc.ok {
				if got["ok"] != true || got["entries"] != tc.entries {
					t.Fatalf("got %v, want ok=true entries=%d", got, tc.entries)
				}
			} else {
				if got["ok"] != false || got["seq"] != tc.seq || got["reason"] != tc.reason {
					t.Fatalf("got %v, want ok=false seq=%d reason=%s", got, tc.seq, tc.reason)
				}
			}

			// Every proper prefix before a first refusal (or of a valid log) must be valid (§9a.2).
			lines := bytes.Split(bytes.TrimSuffix(tc.log, []byte{'\n'}), []byte{'\n'})
			for n := 0; n < len(lines); n++ {
				prefix := bytes.Join(lines[:n], []byte{'\n'})
				if n > 0 {
					prefix = append(prefix, '\n')
				}
				pv, err := checkLog(bytes.NewReader(prefix))
				if err != nil || pv["ok"] != true || pv["entries"] != int64(n) {
					t.Fatalf("proper prefix %d: got %v (err=%v)", n, pv, err)
				}
			}

			// Also verify through the CLI binary.
			logPath := filepath.Join(tmpDir, tc.name+".jsonl")
			if err := os.WriteFile(logPath, tc.log, 0600); err != nil {
				t.Fatal(err)
			}
			cmd := exec.Command("./check", logPath)
			var stdout, stderr bytes.Buffer
			cmd.Stdout, cmd.Stderr = &stdout, &stderr
			err = cmd.Run()
			code := 0
			if err != nil {
				exit, ok := err.(*exec.ExitError)
				if !ok {
					t.Fatal(err)
				}
				code = exit.ExitCode()
			}
			wantCode := 1
			if tc.ok {
				wantCode = 0
			}
			if code != wantCode {
				t.Fatalf("CLI exit=%d want=%d stderr=%s", code, wantCode, stderr.String())
			}
			var cliVerdict map[string]any
			if err := json.Unmarshal(stdout.Bytes(), &cliVerdict); err != nil {
				t.Fatal(err)
			}
			if tc.ok {
				if cliVerdict["ok"] != true || cliVerdict["entries"] != float64(tc.entries) {
					t.Fatalf("CLI verdict: %v", cliVerdict)
				}
			} else {
				if cliVerdict["ok"] != false || cliVerdict["seq"] != float64(tc.seq) || cliVerdict["reason"] != tc.reason {
					t.Fatalf("CLI verdict: %v", cliVerdict)
				}
			}
		})
	}
}
