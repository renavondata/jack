package main

import (
	"bytes"
	"crypto/sha512"
	"encoding/base64"
	"encoding/binary"
	"strings"
)

// Both specified containers have lengths divisible by three: their standard
// base64 encodings have no padding or unused bits.
func decodeBase64(s string, size int) ([]byte, bool) {
	if len(s) != base64.StdEncoding.EncodedLen(size) {
		return nil, false
	}
	for _, c := range s {
		if !(c >= 'A' && c <= 'Z' || c >= 'a' && c <= 'z' || c >= '0' && c <= '9' || c == '+' || c == '/') {
			return nil, false
		}
	}
	b, err := base64.StdEncoding.DecodeString(s)
	return b, err == nil && len(b) == size
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

func parsePublicText(s string) (blob, public []byte, valid bool) {
	fields := strings.Split(s, " ")
	if len(fields) != 2 || fields[0] != "ssh-ed25519" {
		return nil, nil, false
	}
	blob, valid = decodeBase64(fields[1], 51)
	if !valid {
		return nil, nil, false
	}
	public, valid = publicFromBlob(blob)
	return blob, public, valid
}

type signatureContainer struct{ blob, public, signature []byte }

func parseSignature(s string) (signatureContainer, bool) {
	b, ok := decodeBase64(s, 180)
	if !ok {
		return signatureContainer{}, false
	}
	r := wireReader{b: b}
	magic := r.raw(6)
	version := r.uint32()
	blob, namespace, reserved, hash, inner := r.text(), r.text(), r.text(), r.text(), r.text()
	if !r.done() || !bytes.Equal(magic, []byte("SSHSIG")) || version != 1 || string(namespace) != "core-entry" || len(reserved) != 0 || string(hash) != "sha512" {
		return signatureContainer{}, false
	}
	public, ok := publicFromBlob(blob)
	if !ok {
		return signatureContainer{}, false
	}
	ir := wireReader{b: inner}
	typ, signature := ir.text(), ir.text()
	if !ir.done() || string(typ) != "ssh-ed25519" || len(signature) != 64 {
		return signatureContainer{}, false
	}
	return signatureContainer{blob, public, signature}, true
}

func signedData(message []byte) []byte {
	h := sha512.Sum512(message)
	b := []byte("SSHSIG")
	for _, part := range [][]byte{[]byte("core-entry"), {}, []byte("sha512"), h[:]} {
		b = append(b, wireString(part)...)
	}
	return b
}
