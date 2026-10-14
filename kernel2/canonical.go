package main

import (
	"bytes"
	"fmt"
	"sort"
	"strconv"
	"strings"
	"unicode/utf16"
	"unicode/utf8"
)

// jsonInteger is distinct from strings and booleans. Invalid canonical numbers
// are still parsed completely, so later syntax/surrogate errors take precedence.
type jsonInteger int64
type object map[string]any

type jsonParser struct {
	b            []byte
	i            int
	depth        int
	noncanonical bool
}

func (p *jsonParser) space() {
	for p.i < len(p.b) && strings.ContainsRune(" \t\r\n", rune(p.b[p.i])) {
		p.i++
	}
}

func (p *jsonParser) take(c byte) bool {
	if p.i < len(p.b) && p.b[p.i] == c {
		p.i++
		return true
	}
	return false
}

func (p *jsonParser) hex4() (rune, error) {
	if len(p.b)-p.i < 4 {
		return 0, fmt.Errorf("short Unicode escape")
	}
	for _, c := range p.b[p.i : p.i+4] {
		if !(digit(c) || c >= 'a' && c <= 'f' || c >= 'A' && c <= 'F') {
			return 0, fmt.Errorf("invalid Unicode escape")
		}
	}
	n, err := strconv.ParseUint(string(p.b[p.i:p.i+4]), 16, 16)
	if err != nil {
		return 0, err
	}
	p.i += 4
	return rune(n), nil
}

func (p *jsonParser) text() (string, error) {
	if !p.take('"') {
		return "", fmt.Errorf("expected string")
	}
	var s strings.Builder
	for p.i < len(p.b) {
		c := p.b[p.i]
		p.i++
		if c == '"' {
			return s.String(), nil
		}
		if c < 0x20 {
			return "", fmt.Errorf("unescaped control")
		}
		if c != '\\' {
			s.WriteByte(c)
			continue
		}
		if p.i == len(p.b) {
			break
		}
		c = p.b[p.i]
		p.i++
		switch c {
		case '"', '\\', '/':
			s.WriteByte(c)
		case 'b':
			s.WriteByte('\b')
		case 'f':
			s.WriteByte('\f')
		case 'n':
			s.WriteByte('\n')
		case 'r':
			s.WriteByte('\r')
		case 't':
			s.WriteByte('\t')
		case 'u':
			r, err := p.hex4()
			if err != nil {
				return "", err
			}
			if r >= 0xd800 && r <= 0xdbff {
				if !p.take('\\') || !p.take('u') {
					return "", fmt.Errorf("lone high surrogate")
				}
				lo, err := p.hex4()
				if err != nil || lo < 0xdc00 || lo > 0xdfff {
					return "", fmt.Errorf("invalid surrogate pair")
				}
				r = utf16.DecodeRune(r, lo)
			} else if r >= 0xdc00 && r <= 0xdfff {
				return "", fmt.Errorf("lone low surrogate")
			}
			s.WriteRune(r)
		default:
			return "", fmt.Errorf("invalid escape")
		}
	}
	return "", fmt.Errorf("unterminated string")
}

func digit(c byte) bool { return c >= '0' && c <= '9' }

func (p *jsonParser) number() (any, error) {
	start := p.i
	p.take('-')
	if !p.take('0') {
		if p.i == len(p.b) || p.b[p.i] < '1' || p.b[p.i] > '9' {
			return nil, fmt.Errorf("expected number")
		}
		for p.i < len(p.b) && digit(p.b[p.i]) {
			p.i++
		}
	}
	integer := true
	if p.take('.') {
		integer = false
		at := p.i
		for p.i < len(p.b) && digit(p.b[p.i]) {
			p.i++
		}
		if at == p.i {
			return nil, fmt.Errorf("empty fraction")
		}
	}
	if p.take('e') || p.take('E') {
		integer = false
		if !p.take('+') {
			p.take('-')
		}
		at := p.i
		for p.i < len(p.b) && digit(p.b[p.i]) {
			p.i++
		}
		if at == p.i {
			return nil, fmt.Errorf("empty exponent")
		}
	}
	// Scan the whole token for JSON syntax, but never convert long numbers.
	if !integer || p.i-start > 20 {
		p.noncanonical = true
		return jsonInteger(0), nil
	}
	s := string(p.b[start:p.i])
	n, err := strconv.ParseInt(s, 10, 64)
	if err != nil || n < -9007199254740991 || n > 9007199254740991 || s == "-0" {
		p.noncanonical = true
		return jsonInteger(0), nil
	}
	return jsonInteger(n), nil
}

func (p *jsonParser) value() (any, error) {
	p.space()
	if p.i == len(p.b) {
		return nil, fmt.Errorf("missing value")
	}
	if p.b[p.i] == '{' || p.b[p.i] == '[' {
		if p.depth == 32 {
			return nil, fmt.Errorf("nesting exceeds 32")
		}
		p.depth++
		defer func() { p.depth-- }()
	}
	switch p.b[p.i] {
	case '"':
		return p.text()
	case '{':
		p.i++
		p.space()
		m := object{}
		if p.take('}') {
			return m, nil
		}
		for {
			p.space()
			key, err := p.text()
			if err != nil {
				return nil, err
			}
			p.space()
			if !p.take(':') {
				return nil, fmt.Errorf("missing colon")
			}
			v, err := p.value()
			if err != nil {
				return nil, err
			}
			if _, exists := m[key]; exists {
				p.noncanonical = true
			}
			m[key] = v
			p.space()
			if p.take('}') {
				return m, nil
			}
			if !p.take(',') {
				return nil, fmt.Errorf("missing object separator")
			}
		}
	case '[':
		p.i++
		p.space()
		a := []any{}
		if p.take(']') {
			return a, nil
		}
		for {
			v, err := p.value()
			if err != nil {
				return nil, err
			}
			a = append(a, v)
			p.space()
			if p.take(']') {
				return a, nil
			}
			if !p.take(',') {
				return nil, fmt.Errorf("missing array separator")
			}
		}
	case 't', 'f', 'n':
		for _, literal := range []struct {
			text  string
			value any
		}{{"true", true}, {"false", false}, {"null", nil}} {
			if bytes.HasPrefix(p.b[p.i:], []byte(literal.text)) {
				p.i += len(literal.text)
				return literal.value, nil
			}
		}
		return nil, fmt.Errorf("invalid literal")
	default:
		return p.number()
	}
}

func parseCanonical(line []byte) (object, string) {
	if !utf8.Valid(line) {
		return nil, "malformed_json"
	}
	p := jsonParser{b: line}
	v, err := p.value()
	p.space()
	m, ok := v.(object)
	if err != nil || p.i != len(line) || !ok {
		return nil, "malformed_json"
	}
	if p.noncanonical || !bytes.Equal(canonical(m), line) {
		return nil, "not_canonical"
	}
	return m, ""
}

func appendText(b []byte, s string) []byte {
	b = append(b, '"')
	const hex = "0123456789abcdef"
	unit := func(r rune) { b = append(b, '\\', 'u', hex[(r>>12)&15], hex[(r>>8)&15], hex[(r>>4)&15], hex[r&15]) }
	for _, r := range s {
		switch r {
		case '"', '\\':
			b = append(b, '\\', byte(r))
		case '\b':
			b = append(b, '\\', 'b')
		case '\f':
			b = append(b, '\\', 'f')
		case '\n':
			b = append(b, '\\', 'n')
		case '\r':
			b = append(b, '\\', 'r')
		case '\t':
			b = append(b, '\\', 't')
		default:
			if r >= 0x20 && r <= 0x7e {
				b = append(b, byte(r))
			} else if r <= 0xffff {
				unit(r)
			} else {
				hi, lo := utf16.EncodeRune(r)
				unit(hi)
				unit(lo)
			}
		}
	}
	return append(b, '"')
}

func appendCanonical(b []byte, v any) []byte {
	switch v := v.(type) {
	case object:
		keys := make([]string, 0, len(v))
		for k := range v {
			keys = append(keys, k)
		}
		// UTF-8 lexicographic order equals code-point order for valid strings.
		sort.Strings(keys)
		b = append(b, '{')
		for i, k := range keys {
			if i > 0 {
				b = append(b, ',')
			}
			b = appendText(b, k)
			b = append(b, ':')
			b = appendCanonical(b, v[k])
		}
		return append(b, '}')
	case []any:
		b = append(b, '[')
		for i, x := range v {
			if i > 0 {
				b = append(b, ',')
			}
			b = appendCanonical(b, x)
		}
		return append(b, ']')
	case string:
		return appendText(b, v)
	case jsonInteger:
		return strconv.AppendInt(b, int64(v), 10)
	case bool:
		return strconv.AppendBool(b, v)
	case nil:
		return append(b, "null"...)
	default:
		panic("non-JSON internal value")
	}
}

func canonical(v any) []byte { return appendCanonical(nil, v) }
