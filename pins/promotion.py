"""Item 15 pins, run against the disposable copy's judge and signed histories."""
from harness import build, gitfix
from judge import judge
from tests.promotion_fixture import install
from tests.test_promotion_judge import Promotions


class Cases(Promotions):
    def test_preinstallation(self):
        self.log = self.w.log(self.w.decls + self.w.party_decls, charter=gitfix.CHARTER_SHA256,
                              checker=judge.digest(self.repo, "HEAD"))
        self.log.add("decision", "guy", {"kind": "promote", "subject": "C1a"}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        gitfix.commit_all(self.repo, "Historical promotion without attested evidence")
        install(self.repo, self.log, self.w)
        self.check(whole_judge=True)

    def test_ungranted_installation(self):
        self.log = build.Log(self.lg.lines[:5564])
        self.log.add("decision", "guy", {"kind": "grant", "subject": "promote_unmet: SPEC.md " + "0" * 64}, self.w.guy)
        self.log.add("push", "guy", {"digest": judge.digest(self.repo, "HEAD"), "review": "0" * 64}, self.w.guy)
        gitfix.write(self.repo, "log.jsonl", self.log.text())
        gitfix.commit_all(self.repo, "Push whose SPEC no earlier grant names")
        self.check("promote_unmet", whole_judge=True)

    def test_skipped_promotion_on_later_run(self):
        for lawful in (True, False):
            with self.subTest(lawful=lawful):
                gitfix.git(self.repo, "reset", "-q", "--hard", self.installed)
                self.log = build.Log(self.lg.lines)
                self.promote(lawful=lawful)  # its message has [skip ci]; no check here
                gitfix.write(self.repo, "README.md", "next run\n")
                gitfix.commit_all(self.repo, "Next run after the skipped promotion")
                self.check(None if lawful else "promote_unmet", whole_judge=True)
