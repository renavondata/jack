#!/usr/bin/env python3
"""Regenerate spec/vectors: canonical-JSON vectors and signed logs with the verdict each must produce.

Keys are throwaway and discarded; only their public halves survive, embedded in
each log's genesis. Verdicts come from the Python kernel, which implements
SPEC.md; a second checker must reproduce them. Not kernel."""
import glob
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from harness import build, keys  # noqa: E402
from harness.build import proposal  # noqa: E402
from kernel import check, log, sig  # noqa: E402

OUT = os.path.join(ROOT, "spec", "vectors")


def canonical_vectors():
    cases = [{"b": 1, "a": "x"}, {"z": [1, {"y": None, "x": True}]}, {"s": "é\n\x01/\"\\\U0001F600\u007f"},
             {"n": [0, -1, 9007199254740991]}, {"empty": {}, "list": []}, {"kéy": "v"}]
    lines = [log.canonical(c) for c in cases]
    bad = {'{"a": 1}': "not_canonical", '{"b":1,"a":2}': "not_canonical", '{"a":1.0}': "not_canonical",
           '{"a":-0}': "not_canonical", '{"a":1e2}': "not_canonical", '{"a":9007199254740992}': "not_canonical",
           '{"a":1,"a":2}': "not_canonical", '{"a":"\\ud800"}': "malformed_json", '{"a":"é"}': "not_canonical",
           "[1]": "malformed_json", "{": "malformed_json", '{"a":1.5,"b":"\\ud800"}': "malformed_json"}
    return {"canonical": [{"value": c, "canonical": l, "sha256": log.line_hash(l)} for c, l in zip(cases, lines)],
            "refused_lines": [{"line": l, "reason": r} for l, r in bad.items()],
            "genesis_parent": log.GENESIS_PARENT}


def logs(w):
    weak = dict(keys.weak_keys())
    bob = w.stranger
    out = {}
    lg = w.log(); out["00_genesis_only"] = lg.lines
    lg = w.log()
    lg.add("proposal", "ann", proposal("alpha"), w.ann)
    lg.add("key", "guy", build.decl("bob-1", "bob", bob, ["proposal"]), w.guy)
    lg.add("proposal", "bob", proposal("beta"), bob)
    lg.add("merge", "guy", build.merge(1, build.HEX64), w.guy)
    lg.add("key", "guy", build.decl("bob-1", "bob", bob, []), w.guy)
    lg.add("proposal", "ann", proposal("gamma", note={"nested": [1, {"k": True}], "a.b": None}), w.ann)
    out["01_every_type_grant_revoke"] = list(lg.lines)
    lg.add("proposal", "bob", proposal("x"), bob); out["02_revoked_key_no_power"] = list(lg.lines); lg.lines.pop()
    lg.add("key", "guy", build.decl("ann-1", "ann", w.ann, ["proposal", "merge"]), w.guy)
    lg.add("merge", "ann", build.merge(1), w.ann); out["03_redeclared_powers"] = list(lg.lines)
    lg = w.log(); lg.add("key", "guy", build.decl("ann-2", "ann", w.ann, ["proposal"]), w.guy); out["04_duplicate_pubkey_bad_key"] = lg.lines
    lg = w.log(); lg.add("key", "guy", build.decl("eve-1", "eve", keys.fake_key(weak["order 8 (a)"]), ["proposal"]), w.guy)
    out["05_small_order_key_bad_key"] = lg.lines
    lg = w.log(); lg.add("key", "guy", build.decl("eve-1", "eve", keys.fake_key(weak["y = p + 1"]), ["proposal"]), w.guy)
    out["06_noncanonical_key_bad_key"] = lg.lines
    lg = build.Log(); lg.add("genesis", "guy", build.genesis_body(w.decls + [build.decl("eve-1", "eve", keys.fake_key(weak["identity (order 1)"]), [])]), w.guy)
    out["07_genesis_weak_key_bad_key"] = lg.lines
    lg = w.log(); lg.add("key", "ann", build.decl("x", "ann", bob, ["proposal"]), w.ann); out["08_no_power"] = lg.lines
    lg = w.log(); lg.add("proposal", "ann", proposal(), bob); out["09_unknown_key"] = lg.lines
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.ann); out["10_proposer_mismatch"] = lg.lines
    lg = w.log(); lg.add("proposal", "", proposal(), w.ann); out["11_no_proposer"] = lg.lines
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.ann)
    e = log.parse_line(lg.lines[1]); e["body"]["title"] = "tampered"; out["12_bad_signature_tampered"] = [lg.lines[0], log.canonical(e)]
    e = log.parse_line(lg.lines[1]); _, s64 = sig.parse_sshsig(e["sig"])
    e["sig"] = keys.rewrap(e["sig"], sig64=s64[:32] + (int.from_bytes(s64[32:], "little") + sig.L).to_bytes(32, "little"))
    out["13_bad_signature_s_plus_L"] = [lg.lines[0], log.canonical(e)]
    e = log.parse_line(lg.lines[1]); e["sig"] = keys.rewrap(e["sig"], namespace="file"); out["14_bad_signature_namespace"] = [lg.lines[0], log.canonical(e)]
    e = log.parse_line(lg.lines[1]); e["sig"] = keys.rewrap(e["sig"], reserved=b"\x00"); out["15_bad_signature_reserved"] = [lg.lines[0], log.canonical(e)]
    lg.lines.append(build.make_entry(3, lg.head, "proposal", "ann", proposal(), w.ann)); out["16_bad_seq"] = list(lg.lines); lg.lines.pop()
    lg.lines.append(build.make_entry(2, log.GENESIS_PARENT, "proposal", "ann", proposal(), w.ann)); out["17_parent_mismatch_fork"] = list(lg.lines); lg.lines.pop()
    lg.add("genesis", "guy", build.genesis_body(w.decls), w.guy); out["18_genesis_misplaced"] = list(lg.lines); lg.lines.pop()
    lg.add("proposal", "ann", {"title": "no commit"}, w.ann); out["19_schema"] = list(lg.lines); lg.lines.pop()
    lg.add("rule", "guy", {"rule_id": "r1"}, w.guy); out["20_schema_rule_type_gone"] = list(lg.lines); lg.lines.pop()
    out["21_not_canonical"] = [lg.lines[0], lg.lines[1].replace(',"ts"', ', "ts"', 1)]
    out["22_malformed_json"] = [lg.lines[0], lg.lines[1][:-2]]
    out["23_empty"] = []
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.ann, ts="\uff12\uff10\uff12\uff16-10-14T00:00:00Z"); out["24_ts_unicode_digits"] = lg.lines
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.ann, ts="2026-02-29T00:00:00Z"); out["25_ts_impossible_date"] = lg.lines
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.ann, ts="2028-02-29T23:59:59Z"); out["26_ts_leap_day_ok"] = lg.lines
    out["27_nesting_33_deep"] = ['{"a":' * 33 + "1" + "}" * 33]
    out["28_long_integer"] = ['{"a":' + "9" * 5000 + "}"]
    lg = w.log(); lg.add("key", "guy", build.decl("ann-1", "ann", bob, ["proposal"]), w.guy)
    lg.add("key", "guy", build.decl("eve-1", "eve", w.ann, ["proposal"]), w.guy); out["29_pubkey_reused_after_rotation"] = lg.lines
    lg = w.log(); lg.add("key", "guy", dict(build.decl("eve-1", "eve", bob, ["proposal"]), note="x"), w.guy); out["30_key_decl_extra_member"] = lg.lines
    lg = build.Log(); lg.add("genesis", "guy", build.genesis_body([dict(w.decls[0], note="x")] + w.decls[1:]), w.guy)
    out["31_genesis_key_extra_member"] = lg.lines
    return out


def main():
    os.makedirs(os.path.join(OUT, "logs"), exist_ok=True)
    for old in glob.glob(os.path.join(OUT, "logs", "*.jsonl")):
        os.remove(old)
    with tempfile.TemporaryDirectory() as tmp:
        w = build.World(tmp)
        verdicts = {}
        for name, lines in logs(w).items():
            with open(os.path.join(OUT, "logs", name + ".jsonl"), "w") as f:
                f.write("".join(l + "\n" for l in lines))
            v = check.check(lines)
            verdicts[name + ".jsonl"] = {k: x for k, x in v.items() if k != "detail"}
    with open(os.path.join(OUT, "canonical.json"), "w") as f:
        json.dump(canonical_vectors(), f, indent=1, ensure_ascii=False)
    with open(os.path.join(OUT, "verdicts.json"), "w") as f:
        json.dump({"about": "verdict each log in logs/ must produce (SPEC.md §10), detail omitted", "verdicts": verdicts}, f, indent=1)
    print(f"{len(verdicts)} logs, {len(canonical_vectors()['canonical'])} canonical vectors → {OUT}")


if __name__ == "__main__":
    main()
