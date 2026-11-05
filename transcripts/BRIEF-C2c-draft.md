# BRIEF-C2c (draft, counsel) — Appendix M, the model (5 November 2026)

This file is `transcripts/BRIEF-C2c-draft.md`. The model is written first and in small steps, one rule at a time; the rest of the brief follows. Each rule is marked **New in C2c**, binds C2c only, and has a pin.

C2c's opening is the entry that C2c's brief's opening rule selects.

## M.1 One stated end (New in C2c)

- C2c's promotion forecast is the first `forecast` by counsel whose `args.id` is the id C2c's brief names, and whose `seq` is below C2c's opening.
- `tools/status.py` reads C2c's stated end only from that forecast's `resolves_by` (A5.2: "a brief states no other date").
- With no such forecast, `status.py` prints `promote C2c: refused: C2c has no promotion forecast before its opening`.

**Pin `c2c_one_end`.**

Twins:
1. All of these lie below the opening:
   - first, a counsel forecast with another id, dated *d3*;
   - then a non-counsel forecast with the id, dated *d0*;
   - then counsel's forecast with the id, dated *d1*, later than opening + 14 d;
   - then a second counsel forecast with the id, dated *d2*.

   The four dates differ, and the stated end is *d1*.
2. The only forecast with the id lies above the opening. `status.py` prints the refusal line.

Mutants:
- the stated end read as opening + 14 d (killed by twin 1);
- read as min(*d1*, opening + 14 d), which is how `status.py` reads C2a's end today (twin 1);
- the second counsel forecast taken (twin 1);
- the non-counsel forecast taken (twin 1);
- the forecast above the opening accepted (twin 2);
- the `args.id` test dropped (twin 1).

M.1 decides nothing about C2a's stated end, which is unruled (`transcripts/CASES.md`).

## M.2 Three values for each criterion (New in C2c)

Each criterion of C2c prints one of three values, decided in this order:
1. `unmet`, when the inputs supplied already show it fails;
2. otherwise `unknown (no <input>)`, when an input it reads is not supplied or cannot be read. `<input>` is that input's name, for example `unknown (no run file)`;
3. otherwise `met` or `unmet`, as the inputs say.

Which runs count as supplied is stated with each criterion.

**Pin `c2c_three_values`.** The pin runs on a criterion of C2c that reads the run file and the tree.

The twins:
1. With every input supplied, the line prints `met` or `unmet`, as the inputs say.
2. With no run file, and a tree that shows no failure, the line prints `unknown (no run file)`.
3. With no run file, and a tree that shows a failure, the line prints `unmet`.

The mutants:
- absent input printed as `unmet` (killed by twin 2);
- absent input printed as `met` (twin 2);
- `unknown` printed where the tree already shows a failure (twin 3).
