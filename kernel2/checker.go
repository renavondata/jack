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
	amendID        = regexp.MustCompile(`^[A-Z][0-9]{1,3}$`)
	sigShape       = regexp.MustCompile(`^[A-Za-z0-9+/]+={0,2}$`)
	asciiTimestamp = regexp.MustCompile(`^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$`)
)

func isType(s string) bool {
	switch s {
	case "genesis", "key", "proposal", "merge", "amend", "push", "decision", "spec_conflict":
		return true
	}
	return false
}

func isDecisionKind(v any) bool {
	switch v {
	case "veto", "promote", "budget", "grant", "transmute", "fix":
		return true
	}
	return false
}

func nonempty(v any) bool                   { s, ok := v.(string); return ok && s != "" }
func matches(v any, re *regexp.Regexp) bool { s, ok := v.(string); return ok && re.MatchString(s) }
func nonnegative(v any) bool                { n, ok := v.(jsonInteger); return ok && n >= 0 }

func timestampShape(v any) bool {
	s, ok := v.(string)
	if !ok || !asciiTimestamp.MatchString(s) {
		return false
	}
	num := func(a, b int) int { n, _ := strconv.Atoi(s[a:b]); return n }
	y, m, d := num(0, 4), num(5, 7), num(8, 10)
	days := []int{0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31}
	if y%400 == 0 || y%4 == 0 && y%100 != 0 {
		days[2] = 29
	}
	if y == 0 || m < 1 || m > 12 || d < 1 || d > days[m] || num(11, 13) > 23 || num(14, 16) > 59 || num(17, 19) > 59 {
		return false
	}
	return true
}

func entryShape(m object) bool {
	if len(m) != 7 {
		return false
	}
	for _, k := range []string{"seq", "parent", "ts", "type", "proposer", "body", "sig"} {
		if _, ok := m[k]; !ok {
			return false
		}
	}
	if !nonnegative(m["seq"]) || !matches(m["parent"], hex64) || !matches(m["sig"], sigShape) {
		return false
	}
	typ, ok := m["type"].(string)
	if !ok || !isType(typ) {
		return false
	}
	if _, ok := m["proposer"].(string); !ok {
		return false
	}
	if _, ok := m["body"].(object); !ok {
		return false
	}
	return timestampShape(m["ts"])
}

type declaration struct {
	id, principal string
	blob, public  []byte
	powers        []string
}

func keyShape(v any) (declaration, bool) {
	m, ok := v.(object)
	if !ok || len(m) != 4 {
		return declaration{}, false
	}
	if !matches(m["key_id"], keyID) {
		return declaration{}, false
	}
	principal, ok := m["principal"].(string)
	if !ok || principal == "" {
		return declaration{}, false
	}
	ps, ok := m["powers"].([]any)
	if !ok {
		return declaration{}, false
	}
	powers := make([]string, len(ps))
	for i, v := range ps {
		s, ok := v.(string)
		if !ok || !isType(s) {
			return declaration{}, false
		}
		powers[i] = s
	}
	text, ok := m["pubkey"].(string)
	if !ok {
		return declaration{}, false
	}
	blob, public, ok := parsePublicText(text)
	if !ok {
		return declaration{}, false
	}
	return declaration{m["key_id"].(string), principal, blob, public, powers}, true
}

func bodyShape(typ string, m object) ([]declaration, bool) {
	switch typ {
	case "genesis":
		if !matches(m["charter"], hex64) || !matches(m["checker"], hex64) {
			return nil, false
		}
		ks, ok := m["keys"].([]any)
		if !ok {
			return nil, false
		}
		decls := make([]declaration, len(ks))
		for i, v := range ks {
			d, ok := keyShape(v)
			if !ok {
				return nil, false
			}
			decls[i] = d
		}
		return decls, true
	case "key":
		d, ok := keyShape(m)
		return []declaration{d}, ok
	case "proposal":
		_, ok := m["title"].(string)
		return nil, ok && matches(m["commit"], hex40)
	case "merge":
		return nil, nonnegative(m["proposal"]) && matches(m["commit"], hex40) && matches(m["checker"], hex64)
	case "amend":
		_, integer := m["activate_at"].(jsonInteger)
		return nil, matches(m["id"], amendID) && matches(m["charter"], hex64) && integer
	case "push":
		return nil, matches(m["digest"], hex64) && matches(m["review"], hex64)
	case "decision":
		return nil, isDecisionKind(m["kind"]) && nonempty(m["subject"])
	case "spec_conflict":
		return nil, nonempty(m["section"]) && nonempty(m["text"])
	}
	panic("entry shape admitted unknown type")
}

type amendment struct {
	seq, activateAt int64
	charter         string
}

type law struct {
	head               string
	keys               map[string]declaration
	byBlob             map[string]string // Lifetime ownership; includes rotated-out blobs.
	genesisCharter     string
	promulgatedCharter string
	trustedBase        string
	amendments         []amendment // Log order, not activation-height order.
	amendIDs           map[string]bool
	transmuted         map[string]bool
}

func newLaw() law {
	return law{
		head: strings.Repeat("0", 64), keys: map[string]declaration{},
		byBlob: map[string]string{}, amendIDs: map[string]bool{}, transmuted: map[string]bool{},
	}
}

// Only earlier entries establish the law at a position. Among eligible
// amendments, the latest in log order wins, even if heights are out of order.
func (s law) charterAt(position int64) string {
	for i := len(s.amendments) - 1; i >= 0; i-- {
		a := s.amendments[i]
		if a.seq < position && a.activateAt <= position {
			return a.charter
		}
	}
	return s.genesisCharter
}

func (s *law) declare(d declaration) string {
	if weakKey(d.public) {
		return "weak public key"
	}
	if id, ok := s.byBlob[string(d.blob)]; ok && id != d.id {
		return "public key already declared under another key_id"
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

func checkEntry(line []byte, seq int64, state *law) map[string]any {
	fail := func(reason, detail string) map[string]any { return refused(seq, reason, detail) }
	m, reason := parseCanonical(line)
	if reason != "" {
		return fail(reason, "line is not a canonical JSON object")
	}
	if !entryShape(m) {
		return fail("schema", "entry shape")
	}
	if int64(m["seq"].(jsonInteger)) != seq {
		return fail("bad_seq", "seq differs from line index")
	}
	if m["parent"].(string) != state.head {
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
	body := m["body"].(object)
	decls, ok := bodyShape(typ, body)
	if !ok {
		return fail("schema", "body shape")
	}
	if typ == "amend" {
		if state.amendIDs[body["id"].(string)] || int64(body["activate_at"].(jsonInteger)) <= seq {
			return fail("schema", "amendment id repeated or activation does not exceed seq")
		}
	}
	if typ == "genesis" {
		for _, d := range decls {
			if detail := state.declare(d); detail != "" {
				return fail("bad_key", detail)
			}
		}
	}
	container, ok := parseSignature(m["sig"].(string))
	if !ok {
		return fail("bad_signature", "invalid SSHSIG container")
	}
	id, known := state.byBlob[string(container.blob)]
	if !known || !bytes.Equal(state.keys[id].blob, container.blob) {
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
	switch typ {
	case "genesis":
		state.genesisCharter = body["charter"].(string)
		state.promulgatedCharter = state.genesisCharter
		state.trustedBase = body["checker"].(string)
	case "key":
		if detail := state.declare(decls[0]); detail != "" {
			return fail("bad_key", detail)
		}
	case "amend":
		state.promulgatedCharter = body["charter"].(string)
		state.amendments = append(state.amendments, amendment{seq, int64(body["activate_at"].(jsonInteger)), state.promulgatedCharter})
		state.amendIDs[body["id"].(string)] = true
	case "push":
		state.trustedBase = body["digest"].(string)
	case "decision":
		if body["kind"] == "transmute" {
			state.transmuted[body["subject"].(string)] = true
		}
	}
	state.head = fmt.Sprintf("%x", sha256.Sum256(line))
	return nil
}

func checkLog(input io.Reader) (map[string]any, error) {
	r := bufio.NewReader(input)
	state := newLaw()
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
		verdict := checkEntry(line, seq, &state)
		if verdict != nil {
			return verdict, nil
		}
		seq++
	}
}
