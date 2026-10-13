"""Temporary git repositories for judge tests and pins. Not kernel."""
import os
import shutil
import subprocess
import tempfile
from collections import namedtuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Fixture = namedtuple("Fixture", "repo log main")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout.strip()


def write(repo, rel, data):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data)


def commit_all(repo, msg):
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", msg)
    return git(repo, "rev-parse", "HEAD")


def make_repo(world, with_log=True, root=ROOT, tmpdir=None):
    """main: pristine kernel/ and judge/ from `root`, a workflow, SPEC.md, CHARTER.md, README and a
    genesis log; the branch `pr` is checked out, ready for the proposal's commits."""
    repo = tempfile.mkdtemp(dir=tmpdir, prefix="repo-")
    git(repo, "init", "-q", "-b", "main")
    for d in ("kernel", "judge"):
        shutil.copytree(os.path.join(root, d), os.path.join(repo, d), ignore=shutil.ignore_patterns("__pycache__"))
    write(repo, ".github/workflows/judge.yml", "name: judge\n")
    write(repo, "SPEC.md", "spec\n")
    write(repo, "CHARTER.md", "charter\n")
    write(repo, "README.md", "readme\n")
    lg = world.log()
    if with_log:
        write(repo, "log.jsonl", lg.text())
    main = commit_all(repo, "trunk")
    git(repo, "checkout", "-q", "-b", "pr")
    return Fixture(repo, lg, main)
