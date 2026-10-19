"""Temporary git repositories for judge tests and pins. Not kernel."""
import hashlib
import os
import shutil
import subprocess
import tempfile
from collections import namedtuple

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Fixture = namedtuple("Fixture", "repo log main")
CHARTER_TEXT = "# charter\n"
CHARTER_SHA256 = hashlib.sha256(CHARTER_TEXT.encode()).hexdigest()


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True).stdout.strip()


def write(repo, rel, data):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb" if isinstance(data, bytes) else "w") as f:
        f.write(data)


def link(repo, rel, target):
    """A symbolic link at `rel` pointing to `target`, which git stores as mode 120000."""
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    os.symlink(target, path)


def move(repo, old, new):
    """git mv, creating the destination directory (git mv will not)."""
    os.makedirs(os.path.dirname(os.path.join(repo, new)) or repo, exist_ok=True)
    git(repo, "mv", old, new)


def commit_all(repo, msg):
    git(repo, "add", "-A")
    git(repo, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-q", "--allow-empty", "-m", msg)
    return git(repo, "rev-parse", "HEAD")


def make_repo(world, with_log=True, root=ROOT, tmpdir=None):
    """main: pristine kernel/ and judge/ from `root`, a workflow, SPEC.md, CHARTER.md, README and a
    genesis log bound to that CHARTER.md, declaring the world's keys and its parties' keys; the branch `pr`
    is checked out, ready for the proposal's commits."""
    repo = tempfile.mkdtemp(dir=tmpdir, prefix="repo-")
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "diff.renames", "true")  # git's default since 2.9, pinned so rename fixtures behave alike everywhere
    for d in ("kernel", "judge"):
        shutil.copytree(os.path.join(root, d), os.path.join(repo, d), ignore=shutil.ignore_patterns("__pycache__"))
    write(repo, ".github/workflows/judge.yml", "name: judge\n")
    write(repo, "SPEC.md", "spec\n")
    write(repo, "CHARTER.md", CHARTER_TEXT)
    write(repo, "README.md", "readme\n")
    lg = world.log(world.decls + world.party_decls, charter=CHARTER_SHA256)
    if with_log:
        write(repo, "log.jsonl", lg.text())
    main = commit_all(repo, "trunk")
    git(repo, "checkout", "-q", "-b", "pr")
    return Fixture(repo, lg, main)
