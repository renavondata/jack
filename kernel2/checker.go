package main

import (
	"bufio"
	"bytes"
	"crypto/sha256"
	"fmt"
	"io"
	"regexp"
	"strconv"
	"strings"
)

var (
	hex64          = regexp.MustCompile(`^[0-9a-f]{64}$`)
	hex40          = regexp.MustCompile(`^[0-9a-f]{40}$`)
	keyID          = regexp.MustCompile(`^[a-z0-9_-]{1,64}$`)
	sigShape       = regexp.MustCompile(`^[A-Za-z0-9+/]+={0,2}$`)
	asciiTimestamp = regexp.MustCompile(`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$`)
	digitTimestamp = regexp.MustCompile(`^[\p{Nd}]{4}-[\p{Nd}]{2}-[\p{Nd}]{2}T[\p{Nd}]{2}:[\p{Nd}]{2}:[\p{Nd}]{2}Z$`)
)

func isType(s string) bool                  { return s == "genesis" || s == "key" || s == "proposal" || s == "merge" }
func matches(v any, re *regexp.Regexp) bool { s, ok := v.(string); return ok && re.MatchString(s) }
func nonnegative(v any) bool                { n, ok := v.(jsonInteger); return ok && n >= 0 }

func timestampShape(v any) (bool, error) {
	s, ok := v.(string)
	if !ok || !digitTimestamp.MatchString(s) {
		return false, nil
	}
	if !asciiTimestamp.MatchString(s) {
		return false, question("Q1", "Unicode decimal digits in timestamp")
	}
	num := func(a, b int) int { n, _ := strconv.Atoi(s[a:b]); return n }
	y, m, d := num(0, 4), num(5, 7), num(8, 10)
	days := []int{0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
	if y%400 == 0 || y%4 == 0 && y%100 != 0 {
		days[2] = 29
	}
	if y == 0 || m < 1 || m > 12 || d < 1 || d > days[m] || num(11, 13) > 23 || num(14, 16) > 59 || num(17, 19) > 59 {
		return false, question("Q1", "regex-shaped timestamp outside ordinary Gregorian date/time range")
	}
	return true, nil
}

func entryShape(m object) (bool, error) {
	if len(m) != 7 {
		return false, nil
	}
	for _, k := range []string{"seq", "parent", "ts", "type", "proposer", "body", "sig"} {
		if _, ok := m[k]; !ok {
			return false, nil
		}
	}
	if !nonnegative(m["seq"]) || !matches(m["parent"], hex64) || !matches(m["sig"], sigShape) {
		return false, nil
	}
	typ, ok := m["type"].(string)
	if !ok || !isType(typ) {
		return false, nil
	}
	if _, ok := m["proposer"].(string); !ok {
		return false, nil
	}
	if _, ok := m["body"].(object); !ok {
		return false, nil
	}
	return timestampShape(m["ts"])
}

type declaration struct {
	id, principal string
	blob, public  []byte
	powers        []string
}

func keyShape(v any) (declaration, bool, error) {
	m, ok := v.(object)
	if !ok {
		return declaration{}, false, nil
	}
	if !matches(m["key_id"], keyID) {
		return declaration{}, false, nil
	}
	principal, ok := m["principal"].(string)
	if !ok || principal == "" {
		return declaration{}, false, nil
	}
	ps, ok := m["powers"].([]any)
	if !ok {
		return declaration{}, false, nil
	}
	powers := make([]string, len(ps))
	for i, v := range ps {
		s, ok := v.(string)
		if !ok || !isType(s) {
			return declaration{}, false, nil
		}
		powers[i] = s
	}
	text, ok := m["pubkey"].(string)
	if !ok {
		return declaration{}, false, nil
	}
	blob, public, ok, err := parsePublicText(text)
	if err != nil || !ok {
		return declaration{}, false, err
	}
	return declaration{m["key_id"].(string), principal, blob, public, powers}, true, nil
}

func bodyShape(typ string, m object) ([]declaration, bool, error) {
	switch typ {
	case "genesis":
		if !matches(m["charter"], hex64) || !matches(m["checker"], hex64) {
			return nil, false, nil
		}
		ks, ok := m["keys"].([]any)
		if !ok {
			return nil, false, nil
		}
		decls := make([]declaration, len(ks))
		for i, v := range ks {
			d, ok, err := keyShape(v)
			if err != nil || !ok {
				return nil, false, err
			}
			decls[i] = d
		}
		return decls, true, nil
	case "key":
		d, ok, err := keyShape(m)
		return []declaration{d}, ok, err
	case "proposal":
		_, ok := m["title"].(string)
		return nil, ok && matches(m["commit"], hex40), nil
	case "merge":
		return nil, nonnegative(m["proposal"]) && matches(m["commit"], hex40) && matches(m["checker"], hex64), nil
	}
	panic("entry shape admitted unknown type")
}

type law struct {
	keys   map[string]declaration
	byBlob map[string]string
}

func newLaw() law { return law{map[string]declaration{}, map[string]string{}} }

func (s law) declare(d declaration) string {
	if weakKey(d.public) {
		return "weak public key"
	}
	if id, ok := s.byBlob[string(d.blob)]; ok && id != d.id {
		return "public key already declared under another key_id"
	}
	if previous, ok := s.keys[d.id]; ok {
		delete(s.byBlob, string(previous.blob))
	}
	s.keys[d.id] = d
	s.byBlob[string(d.blob)] = d.id
	return ""
}

// The launcher supplies this linker variable so the README's reason-code
// mutation in kernel2/check changes the actual verdict (not just a comment).
var badSignatureReason = "bad_signature"

func refused(seq int64, reason, detail string) map[string]any {
	if reason == "bad_signature" {
		reason = badSignatureReason
	}
	return map[string]any{"ok": false, "seq": seq, "reason": reason, "detail": detail}
}

func checkEntry(line []byte, seq int64, parent string, state law) (map[string]any, error) {
	fail := func(reason, detail string) (map[string]any, error) { return refused(seq, reason, detail), nil }
	m, reason := parseCanonical(line)
	if reason != "" {
		return fail(reason, "line is not a canonical JSON object")
	}
	ok, err := entryShape(m)
	if err != nil {
		return nil, err
	}
	if !ok {
		return fail("schema", "entry shape")
	}
	if int64(m["seq"].(jsonInteger)) != seq {
		return fail("bad_seq", "seq differs from line index")
	}
	if m["parent"].(string) != parent {
		return fail("parent_mismatch", "parent differs from previous line hash")
	}
	typ := m["type"].(string)
	if (typ == "genesis") != (seq == 0) {
		return fail("genesis_misplaced", "genesis must occur exactly at entry zero")
	}
	proposer := m["proposer"].(string)
	if proposer == "" {
		return fail("no_proposer", "empty proposer")
	}
	decls, ok, err := bodyShape(typ, m["body"].(object))
	if err != nil {
		return nil, err
	}
	if !ok {
		return fail("schema", "body shape")
	}
	if typ == "genesis" {
		for _, d := range decls {
			if detail := state.declare(d); detail != "" {
				return fail("bad_key", detail)
			}
		}
	}
	container, ok, err := parseSignature(m["sig"].(string))
	if err != nil {
		return nil, err
	}
	if !ok {
		return fail("bad_signature", "invalid SSHSIG container")
	}
	id, known := state.byBlob[string(container.blob)]
	if !known {
		return fail("unknown_key", "signature key is not declared")
	}
	key := state.keys[id]
	if key.principal != proposer {
		return fail("proposer_mismatch", "signing key belongs to another principal")
	}
	powered := false
	for _, power := range key.powers {
		if power == typ {
			powered = true
			break
		}
	}
	if !powered {
		return fail("no_power", "signing key lacks entry-type power")
	}
	unsigned := make(object, len(m)-1)
	for k, v := range m {
		if k != "sig" {
			unsigned[k] = v
		}
	}
	if !verifyEd25519(container.public, signedData(canonical(unsigned)), container.signature) {
		return fail("bad_signature", "strict Ed25519 verification failed")
	}
	if typ == "key" {
		if detail := state.declare(decls[0]); detail != "" {
			return fail("bad_key", detail)
		}
	}
	return nil, nil
}

func checkLog(input io.Reader) (map[string]any, error) {
	r := bufio.NewReader(input)
	state, parent := newLaw(), strings.Repeat("0", 64)
	var seq int64
	for {
		line, err := r.ReadBytes('\n')
		if err != nil && err != io.EOF {
			return nil, err
		}
		if err == io.EOF && len(line) == 0 {
			return map[string]any{"ok": true, "entries": seq}, nil
		}
		line = bytes.TrimSuffix(line, []byte{'\n'})
		verdict, checkErr := checkEntry(line, seq, parent, state)
		if checkErr != nil {
			return nil, fmt.Errorf("entry %d: %w", seq, checkErr)
		}
		if verdict != nil {
			return verdict, nil
		}
		parent = fmt.Sprintf("%x", sha256.Sum256(line))
		seq++
	}
}
