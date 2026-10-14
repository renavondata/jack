# Open specification questions

No answer below has been chosen. The checker stops without a validity verdict
when it reaches one of these unresolved cases. The supplied vectors do not
resolve them.

## Q1 — §4, §12.4: timestamp syntax and meaning

Does `\d` mean ASCII `[0-9]` or Unicode decimal digits? Does “a UTC timestamp”
require a real calendar date and bounded time fields, or is the displayed
regular expression the entire requirement? Are year zero and leap seconds
allowed? There is no calendar or leap-second definition in the spec.

Implementation boundary: ordinary ASCII Gregorian timestamps with years
0001–9999 and seconds 00–59 are unambiguous. Regex-shaped timestamps outside
that intersection, including Unicode decimal digits, stop at Q1. Strings
outside both interpretations of the regex fail `schema`.

## Q2 — §5, §6: unused base64 padding bits

Must unused bits in the last base64 sextet be zero? “Standard base64 (strict:
only the alphabet, correct padding)” does not explicitly say whether these
bits are part of “correct padding”. Several alphabet- and padding-shaped
strings can decode to the same bytes if the unused bits are ignored. Should
these produce `schema` (public-key text), `bad_signature` (signature text), or
be accepted? The “exactly one encoding” explanation suggests rejection, but
does not specify this condition.

Implementation boundary: incorrect alphabet, missing/excess/misplaced padding
and impossible lengths are rejected as specified. Nonzero unused padding bits
stop at Q2; canonical base64 proceeds.

## Q3 — §9: reporting an unresolved specification question

What CLI status/output should represent an input whose validity cannot be
decided until a specification question is answered? All twelve refusal codes
are validity decisions, and status 2 is specified only for usage/I/O errors.

Until answered, a Q1/Q2 stop emits a question diagnostic on stderr, no JSON
verdict, and status 2. This is an explicit incomplete portion of the CLI
contract, not an additional refusal reason or an answer to Q1/Q2.
