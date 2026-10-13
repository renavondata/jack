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
from harness.build import forbid_title, proposal, rule_body, witness  # noqa: E402
from kernel import check, log, sig  # noqa: E402

OUT = os.path.join(ROOT, "spec", "vectors")


def W(t):
    return witness("proposal", "p", proposal(t))


def R(rid, forbid, viol, sat, **kw):
    return rule_body(rid, forbid_title(rid, *forbid), [W(t) for t in viol], [W(t) for t in sat], **kw)


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
    out = {}
    lg = w.log(); out["00_genesis_only"] = lg.lines
    lg = w.log()
    lg.add("proposal", "ann", proposal("alpha"), w.ann)
    lg.add("key", "guy", build.decl("bob-1", "bob", w.stranger, ["proposal"]), w.guy)
    lg.add("proposal", "bob", proposal("beta"), w.stranger)
    lg.add("rule", "guy", R("r1", ["gamma"], ["gamma"], ["ok"]), w.guy)
    lg.add("rule", "guy", R("r2", ["gamma", "delta"], ["delta"], ["ok"]), w.guy)
    lg.add("merge", "guy", build.merge(1, build.HEX64), w.guy)
    lg.add("repeal", "guy", {"rule_id": "r2"}, w.guy)
    lg.add("key", "guy", build.decl("bob-1", "bob", w.stranger, []), w.guy)
    out["01_every_type_and_lapse"] = list(lg.lines)
    lg.add("proposal", "bob", proposal("x"), w.stranger); out["02_revoked_key_no_power"] = list(lg.lines); lg.lines.pop()
    lg.add("proposal", "ann", proposal("gamma"), w.ann); out["03_violation"] = list(lg.lines); lg.lines.pop()
    lg = w.log()
    lg.add("rule", "guy", R("r1", ["x"], ["x"], ["y"]), w.guy)
    lg.add("rule", "guy", R("r2", ["y"], ["y"], ["z"], replacements={"r1": [W("z")]}), w.guy)
    out["04_replacements"] = list(lg.lines)
    lg.lines.pop(); lg.add("rule", "guy", R("r2", ["y"], ["y"], ["z"]), w.guy); out["05_orphans_rule"] = list(lg.lines)
    rules = {"06_vacuous_rule": R("r1", ["x"], ["z"], ["y"]), "07_impossible_rule": R("r1", ["x"], ["x"], ["x"]),
             "08_rule_malformed": rule_body("r1", [{"head": ["violation", "?S", "zz"], "body": []}], [W("x")], [W("y")]),
             "09_unstratifiable": rule_body("r1", [{"head": ["r1.a", "?S"], "body": [["candidate", "?S"], ["not", ["r1.b", "?S"]]]},
                                                   {"head": ["r1.b", "?S"], "body": [["candidate", "?S"], ["not", ["r1.a", "?S"]]]},
                                                   {"head": ["violation", "?S", "r1"], "body": [["r1.a", "?S"]]}], [W("x")], [W("y")])}
    for name, body in rules.items():
        lg = w.log(); lg.add("rule", "guy", body, w.guy); out[name] = lg.lines
    lg = w.log(); lg.add("rule", "guy", R("r1", ["x"], ["x"], ["y"]), w.guy); lg.add("rule", "guy", R("r1", ["w"], ["w"], ["y"]), w.guy)
    out["10_duplicate_rule"] = lg.lines
    lg = w.log(); lg.add("repeal", "guy", {"rule_id": "none"}, w.guy); out["11_unknown_rule"] = lg.lines
    lg = w.log(); lg.add("rule", "ann", R("r1", ["x"], ["x"], ["y"]), w.ann); out["12_no_power"] = lg.lines
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.stranger); out["13_unknown_key"] = lg.lines
    lg = w.log(); lg.add("proposal", "guy", proposal(), w.ann); out["14_proposer_mismatch"] = lg.lines
    lg = w.log(); lg.add("proposal", "", proposal(), w.ann); out["15_no_proposer"] = lg.lines
    lg = w.log(); lg.add("proposal", "ann", proposal(), w.ann)
    e = log.parse_line(lg.lines[1]); e["body"]["title"] = "tampered"; out["16_bad_signature_tampered"] = [lg.lines[0], log.canonical(e)]
    e = log.parse_line(lg.lines[1]); _, s64 = sig.parse_sshsig(e["sig"])
    e["sig"] = keys.rewrap(e["sig"], sig64=s64[:32] + (int.from_bytes(s64[32:], "little") + sig.L).to_bytes(32, "little"))
    out["17_bad_signature_s_plus_L"] = [lg.lines[0], log.canonical(e)]
    e = log.parse_line(lg.lines[1]); e["sig"] = keys.rewrap(e["sig"], namespace="file"); out["18_bad_signature_namespace"] = [lg.lines[0], log.canonical(e)]
    lg.lines.append(build.make_entry(3, lg.head, "proposal", "ann", proposal(), w.ann)); out["19_bad_seq"] = list(lg.lines); lg.lines.pop()
    lg.lines.append(build.make_entry(2, log.GENESIS_PARENT, "proposal", "ann", proposal(), w.ann)); out["20_parent_mismatch_fork"] = list(lg.lines); lg.lines.pop()
    lg.add("genesis", "guy", build.genesis_body(w.decls), w.guy); out["21_genesis_misplaced"] = list(lg.lines); lg.lines.pop()
    lg.add("proposal", "ann", {"title": "no commit"}, w.ann); out["22_schema"] = list(lg.lines); lg.lines.pop()
    out["23_not_canonical"] = [lg.lines[0], lg.lines[1].replace(',"ts"', ', "ts"', 1)]
    out["24_malformed_json"] = [lg.lines[0], lg.lines[1][:-2]]
    out["25_empty"] = []
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
        json.dump({"about": "verdict each log in logs/ must produce (SPEC.md §13), detail omitted", "verdicts": verdicts}, f, indent=1)
    print(f"{len(verdicts)} logs, {len(canonical_vectors()['canonical'])} canonical vectors → {OUT}")


if __name__ == "__main__":
    main()
