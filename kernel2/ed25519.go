package main

import (
	"bytes"
	"crypto/sha512"
	"math/big"
)

// All field helpers allocate their result: points and constants are immutable.
// This verifier handles public data only; it is not a signing implementation.
func decimal(s string) *big.Int {
	n, ok := new(big.Int).SetString(s, 10)
	if !ok {
		panic("bad constant")
	}
	return n
}

var (
	fieldP       = new(big.Int).Sub(new(big.Int).Lsh(big.NewInt(1), 255), big.NewInt(19))
	orderL       = new(big.Int).Add(new(big.Int).Lsh(big.NewInt(1), 252), decimal("27742317777372353535851937790883648493"))
	curveD       = mul(big.NewInt(-121665), new(big.Int).ModInverse(big.NewInt(121666), fieldP))
	sqrtMinusOne = new(big.Int).Exp(big.NewInt(2), new(big.Int).Rsh(new(big.Int).Sub(fieldP, big.NewInt(1)), 2), fieldP)
	sqrtExponent = new(big.Int).Rsh(new(big.Int).Sub(fieldP, big.NewInt(5)), 3)
	basePoint    = affine(decimal("15112221349535400772501151409588531511454012693041857206046113283949847762202"), decimal("46316835694926478169428394003475163141307993866256225615783033603165251855960"))
)

func add(a, b *big.Int) *big.Int { return new(big.Int).Mod(new(big.Int).Add(a, b), fieldP) }
func sub(a, b *big.Int) *big.Int { return new(big.Int).Mod(new(big.Int).Sub(a, b), fieldP) }
func mul(a, b *big.Int) *big.Int { return new(big.Int).Mod(new(big.Int).Mul(a, b), fieldP) }

func littleInteger(b []byte) *big.Int {
	r := make([]byte, len(b))
	for i := range b {
		r[len(b)-1-i] = b[i]
	}
	return new(big.Int).SetBytes(r)
}

// Extended Edwards coordinates: x=X/Z, y=Y/Z, XY=ZT.
type point struct{ x, y, z, t *big.Int }

func affine(x, y *big.Int) point { return point{x, y, big.NewInt(1), mul(x, y)} }
func identity() point            { return affine(big.NewInt(0), big.NewInt(1)) }

// Complete addition for a=-1: equivalent to the Edwards affine group law,
// without a field inversion at each addition/doubling.
func pointAdd(p, q point) point {
	a := mul(sub(p.y, p.x), sub(q.y, q.x))
	b := mul(add(p.y, p.x), add(q.y, q.x))
	c := mul(big.NewInt(2), mul(curveD, mul(p.t, q.t)))
	d := mul(big.NewInt(2), mul(p.z, q.z))
	e, f, g, h := sub(b, a), sub(d, c), add(d, c), add(b, a)
	return point{mul(e, f), mul(g, h), mul(f, g), mul(e, h)}
}

func scalarMultiply(p point, n *big.Int) point {
	r := identity()
	for i := n.BitLen() - 1; i >= 0; i-- {
		r = pointAdd(r, r)
		if n.Bit(i) != 0 {
			r = pointAdd(r, p)
		}
	}
	return r
}

func encodePoint(p point) []byte {
	zi := new(big.Int).ModInverse(p.z, fieldP)
	x, y := mul(p.x, zi), mul(p.y, zi)
	b := make([]byte, 32)
	yb := y.Bytes()
	for i := range yb {
		b[i] = yb[len(yb)-1-i]
	}
	b[31] |= byte(x.Bit(0)) << 7
	return b
}

func decodePoint(b []byte) (point, bool) {
	if len(b) != 32 {
		return point{}, false
	}
	yb := append([]byte(nil), b...)
	sign := uint(yb[31] >> 7)
	yb[31] &= 0x7f
	y := littleInteger(yb)
	if y.Cmp(fieldP) >= 0 {
		return point{}, false
	}
	y2 := mul(y, y)
	u, v := sub(y2, big.NewInt(1)), add(mul(curveD, y2), big.NewInt(1))
	v2 := mul(v, v)
	v3 := mul(v2, v)
	v7 := mul(mul(v3, v3), v)
	x := mul(mul(u, v3), new(big.Int).Exp(mul(u, v7), sqrtExponent, fieldP))
	vx2 := mul(v, mul(x, x))
	if vx2.Cmp(u) != 0 {
		if vx2.Cmp(sub(big.NewInt(0), u)) != 0 {
			return point{}, false
		}
		x = mul(x, sqrtMinusOne)
	}
	if x.Sign() == 0 && sign == 1 {
		return point{}, false
	}
	if x.Bit(0) != sign {
		x = sub(big.NewInt(0), x)
	}
	return affine(x, y), true
}

func weakKey(public []byte) bool {
	p, ok := decodePoint(public)
	if !ok {
		return true
	}
	return bytes.Equal(encodePoint(scalarMultiply(p, big.NewInt(8))), encodePoint(identity()))
}

func verifyEd25519(public, message, signature []byte) bool {
	if len(signature) != 64 || len(public) != 32 {
		return false
	}
	s := littleInteger(signature[32:])
	if s.Cmp(orderL) >= 0 {
		return false
	}
	a, ok := decodePoint(public)
	if !ok {
		return false
	}
	r, ok := decodePoint(signature[:32])
	if !ok {
		return false
	}
	h := sha512.New()
	h.Write(signature[:32])
	h.Write(public)
	h.Write(message)
	k := new(big.Int).Mod(littleInteger(h.Sum(nil)), orderL)
	return bytes.Equal(encodePoint(scalarMultiply(basePoint, s)), encodePoint(pointAdd(r, scalarMultiply(a, k))))
}
