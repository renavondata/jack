"""Judge fixtures founded against their actual trusted-base content."""
from harness import build, gitfix
from judge import judge


def bind_genesis(repo, lg, world):
    entry = build.log.parse_line(lg.lines[0])
    body = dict(entry["body"], checker=judge.digest(repo, "HEAD"))
    lg.lines[0] = build.make_entry(0, build.log.GENESIS_PARENT, "genesis", "guy", body, world.guy)
    gitfix.write(repo, "log.jsonl", lg.text())
    return gitfix.commit_all(repo, "Found against the trusted base")


def make_repo(world, with_log=True, **kwargs):
    fx = gitfix.make_repo(world, with_log=with_log, **kwargs)
    gitfix.git(fx.repo, "checkout", "-q", "main")
    main = bind_genesis(fx.repo, fx.log, world) if with_log else fx.main
    gitfix.git(fx.repo, "checkout", "-q", "pr")
    gitfix.git(fx.repo, "reset", "-q", "--hard", "main")
    return gitfix.Fixture(fx.repo, fx.log, main)
