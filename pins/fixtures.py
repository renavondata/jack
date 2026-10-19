"""Judge fixtures founded against their actual trusted-base content."""
from harness import build, gitfix
from judge import judge


def bind_genesis(repo, lg, world):
    entry = build.log.parse_line(lg.lines[0])
    body = dict(entry["body"], checker=judge.digest(repo, "HEAD"))
    lg.lines[0] = build.make_entry(0, build.log.GENESIS_PARENT, "genesis", "guy", body, world.guy)
    gitfix.write(repo, "log.jsonl", lg.text())
    return gitfix.commit_all(repo, "Found against the trusted base")


def propose(repo, lg, world, party="builder", msg="change", key=None):
    """Commit the working tree as the proposal's work, then a `proposal` entry naming that commit, signed by
    `party`'s genesis key (or `key`), in a commit touching log.jsonl only (SPEC §10.7). Returns the work's sha."""
    work = gitfix.commit_all(repo, msg)
    lg.add("proposal", party, build.proposal(msg, commit=work), key or world.parties[party])
    gitfix.write(repo, "log.jsonl", lg.text())
    gitfix.commit_all(repo, "Record the proposal")
    return work


def make_repo(world, with_log=True, **kwargs):
    fx = gitfix.make_repo(world, with_log=with_log, **kwargs)
    gitfix.git(fx.repo, "checkout", "-q", "main")
    main = bind_genesis(fx.repo, fx.log, world) if with_log else fx.main
    gitfix.git(fx.repo, "checkout", "-q", "pr")
    gitfix.git(fx.repo, "reset", "-q", "--hard", "main")
    return gitfix.Fixture(fx.repo, fx.log, main)
