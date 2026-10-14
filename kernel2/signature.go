package main

import (
	"bytes"
	"crypto/sha512"
	"encoding/base64"
	"encoding/binary"
	"fmt"
	"strings"
)

func question(id, detail string) error {
	return fmt.Errorf("unresolved SPEC question %s: %s (see kernel2/QUESTIONS.md)", id, detail)
}

// Alphabet, padding count/position and length are checked independently of
// unused pad bits. The latter are deliberately undecided pending Q2.
func decodeBase64(s string) ([]byte, bool, error) {
	for _, c := range s {
		if !(c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z' || c >= '0' && c <= '9' || c == '+' || c == '/' || c == '=') {
			return nil, false, nil
		}
	}
	b, err := base64.StdEncoding.DecodeString(s)
	if err != nil {
		return nil, false, nil
	}
	if base64.StdEncoding.EncodeToString(b) != s {
		return nil, false, question("Q2", "nonzero unused base64 padding bits")
	}
	return b, true, nil
}

type wireReader struct {
	b      []byte
	i      int
	failed bool
}

func (r *wireReader) raw(n int) []byte {
	if r.failed || n < 0 || n > len(r.b)-r.i {
		r.failed = true
		return nil
	}
	b := r.b[r.i : r.i+n]
	r.i += n
	return b
}

func (r *wireReader) uint32() uint32 {
	b := r.raw(4)
	if r.failed {
		return 0
	}
	return binary.BigEndian.Uint32(b)
}

func (r *wireReader) text() []byte {
	n := uint64(r.uint32())
	if r.failed || n > uint64(len(r.b)-r.i) {
		r.failed = true
		return nil
	}
	return r.raw(int(n))
}

func (r *wireReader) done() bool { return !r.failed && r.i == len(r.b) }

func wireString(b []byte) []byte {
	out := make([]byte, 4, 4+len(b))
	binary.BigEndian.PutUint32(out, uint32(len(b)))
	return append(out, b...)
}

func publicFromBlob(blob []byte) ([]byte, bool) {
	r := wireReader{b: blob}
	typ, public := r.text(), r.text()
	return public, r.done() && string(typ) == "ssh-ed25519" && len(public) == 32
}

func parsePublicText(s string) (blob, public []byte, valid bool, err error) {
	fields := strings.Split(s, " ")
	if len(fields) != 2 || fields[0] != "ssh-ed25519" {
		return nil, nil, false, nil
	}
	blob, valid, err = decodeBase64(fields[1])
	if err != nil || !valid {
		return nil, nil, false, err
	}
	public, valid = publicFromBlob(blob)
	return blob, public, valid, nil
}

type signatureContainer struct{ blob, public, signature []byte }

func parseSignature(s string) (signatureContainer, bool, error) {
	b, ok, err := decodeBase64(s)
	if err != nil || !ok {
		return signatureContainer{}, false, err
	}
	r := wireReader{b: b}
	magic := r.raw(6)
	version := r.uint32()
	blob, namespace, reserved, hash, inner := r.text(), r.text(), r.text(), r.text(), r.text()
	if !r.done() || !bytes.Equal(magic, []byte("SSHSIG")) || version != 1 || string(namespace) != "core-entry" || len(reserved) != 0 || string(hash) != "sha512" {
		return signatureContainer{}, false, nil
	}
	public, ok := publicFromBlob(blob)
	if !ok {
		return signatureContainer{}, false, nil
	}
	ir := wireReader{b: inner}
	typ, signature := ir.text(), ir.text()
	if !ir.done() || string(typ) != "ssh-ed25519" || len(signature) != 64 {
		return signatureContainer{}, false, nil
	}
	return signatureContainer{blob, public, signature}, true, nil
}

func signedData(message []byte) []byte {
	h := sha512.Sum512(message)
	b := []byte("SSHSIG")
	for _, part := range [][]byte{[]byte("core-entry"), {}, []byte("sha512"), h[:]} {
		b = append(b, wireString(part)...)
	}
	return b
}
