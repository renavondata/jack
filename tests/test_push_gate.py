"""Opening reads: signed provenance and current bytes, in real local git histories."""
import os, runpy, subprocess, tempfile, unittest
from pathlib import Path
from harness import build

JACK = runpy.run_path(str(Path(__file__).resolve().parents[1] / "tools/jack"))
BRIEF, REVIEW = "transcripts/BRIEF-C2b-draft.md", "transcripts/REVIEW-C2b-v1.md"

class PushGate(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.repo = Path(self.tmp.name) / "repo"; self.repo.mkdir()
        self.world = build.World(self.tmp.name)
        self.git("init", "-q"); self.trunk = self.git("symbolic-ref", "--short", "HEAD")
        self.write(BRIEF, "current\n"); self.write("judge/scope.json", '{"layer":"C1","cap":7800}\n')
        self.base = self.commit()
        self.git("checkout", "-qb", "opening")
        self.write("judge/scope.json", '{"layer":"C1","cap":9000}\n'); self.commit()
        self.git("checkout", "-q", self.trunk); self.main()
    def git(self, *args):
        return subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "-c", "commit.gpgsign=false",
                               *args], cwd=self.repo, env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM="1"),
                              capture_output=True, text=True, check=True).stdout.strip()
    def write(self, name, text):
        path = self.repo / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_text(text)
    def commit(self):
        self.git("add", "."); self.git("commit", "-qm", "work\n\nProposer: reviewer reviewer-2")
        return self.git("rev-parse", "HEAD")
    def main(self): self.git("update-ref", "refs/remotes/origin/main", "HEAD")
    def accepted(self, ref=None): return f"VERDICT: ACCEPT WITH OBLIGATIONS\nReviewed tree: `{ref or self.base}`\n"
    def publish(self, text, party="reviewer", extra=False, rename=None):
        self.git("checkout", "-q", self.trunk); self.git("reset", "--hard", self.base)
        self.git("checkout", "-qB", "review"); self.write(REVIEW, text); head = self.commit()
        if extra: self.write("transcripts/note", "extra"); head = self.commit()
        lg = self.world.log(decls=self.world.decls + self.world.party_decls)
        lg.add("proposal", party, build.proposal(commit=head), self.world.parties[party])
        if rename: lg.add("key", "guy", build.decl(party + "-1", rename, self.world.parties[party], ["proposal"]), self.world.guy)
        self.write("log.jsonl", lg.text()); self.commit()
        self.git("checkout", "-q", self.trunk); self.git("merge", "--no-ff", "-qm", "merge review", "review"); self.main()
    def gate(self, layer="C2b", branch="opening"): return JACK["push_read_gate"](branch, layer, str(self.repo))
    def rejected(self, reason, **kw):
        with self.assertRaisesRegex(JACK["Refused"], reason): self.gate(**kw)
    def test_push_without_read_refused(self):
        self.rejected("REVIEW-C2b-.*missing review")
        for text, reason in (("VERDICT: BLOCK\n", "verdict"), ("VERDICT: ACCEPT\n", "Reviewed tree"),
                             (self.accepted(self.git("rev-parse", "opening")), "not a commit on origin/main")):
            with self.subTest(text=text): self.publish(text); self.rejected("REVIEW-C2b-v1.md:.*" + reason)
        self.publish(self.accepted(), extra=True); self.gate()
    def test_read_of_this_text(self):
        self.publish(self.accepted(self.base[:12]))
        self.write(BRIEF, "changed\n"); self.commit(); self.main()
        self.rejected("REVIEW-C2b-v1.md:.*different bytes.*BRIEF-C2b")
        self.write(BRIEF, "current\n"); self.commit(); self.main(); self.gate()
    def test_read_not_counsels(self):
        self.publish(self.accepted(), "counsel"); self.rejected("REVIEW-C2b-v1.md:.*non-counsel")
        lg = build.Log((self.repo / "log.jsonl").read_text().splitlines())
        lg.add("proposal", "reviewer", build.proposal(commit=self.git("rev-parse", "HEAD")), self.world.parties["reviewer"])
        self.write("log.jsonl", lg.text()); self.commit(); self.main(); self.rejected("REVIEW-C2b-v1.md:.*non-counsel")
        self.publish(self.accepted(), "counsel", rename="reviewer"); self.rejected("REVIEW-C2b-v1.md:.*non-counsel")
        self.publish(self.accepted(), rename="counsel"); self.gate()
        self.publish(self.accepted()); self.gate()
        self.write(REVIEW, self.accepted(self.base[:12]).replace(" WITH OBLIGATIONS", ""))
        self.commit(); self.main(); self.rejected("REVIEW-C2b-v1.md:.*identical review blob")
    def test_read_empty_file_refused(self):
        self.publish(""); self.rejected("REVIEW-C2b-v1.md:.*missing.*verdict")
        self.publish(self.accepted().replace(" WITH OBLIGATIONS", "")); self.gate()
    def test_opens_required_when_scope_changes(self):
        self.rejected("judge/scope.json:.*require --opens", layer=None)
        self.publish(self.accepted()); self.gate()
        self.rejected("judge/scope.json:.*meaningless", branch="origin/main")
        self.gate(layer=None, branch="origin/main")
    def test_window_file_requires_numbers_readers_reviews_covering_both_files(self):
        wfile = "transcripts/windows/C2b.json"
        self.git("checkout", "-q", self.trunk); self.git("reset", "--hard", self.base)
        self.write(wfile, '{"numbers":{"readers":2}}\n'); self.base = self.commit(); self.main()
        self.publish(self.accepted(self.base))
        self.rejected("1 of 2 required reviews accepted")
        self.git("checkout", "-qB", "review2", self.trunk)
        self.write("transcripts/REVIEW-C2b-v2.md", self.accepted(self.base)); head2 = self.commit()
        lg = build.Log((self.repo / "log.jsonl").read_text().splitlines())
        lg.add("proposal", "builder", build.proposal(commit=head2), self.world.parties["builder"])
        self.write("log.jsonl", lg.text()); self.commit()
        self.git("checkout", "-q", self.trunk); self.git("merge", "--no-ff", "-qm", "merge review2", "review2"); self.main()
        self.gate()
        self.write(wfile, '{"numbers":{"readers":2},"edited":true}\n'); self.commit(); self.main()
        self.rejected("different bytes.*C2b.json")
