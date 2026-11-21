"""One promotion assessment, using only the evaluator extracted beside this module."""
import json
import sys
import argparse

from judge import status


def main():
    repo, rev, ts, subject, log_path, run, runs, acts = sys.argv[1:]
    class Parsed(Exception):
        pass
    parse_args = argparse.ArgumentParser.parse_args
    def capture(ap, *args, **kwargs):
        raise Parsed(parse_args(ap, *args, **kwargs))
    # Let this evaluator's own main build and run its parser, stopping before
    # main can call report (which would re-assess earlier promotions).
    argparse.ArgumentParser.parse_args = capture
    try:
        status.main(["--root", repo, "--as-of", ts, "--subject", subject,
                     "--log", log_path, "--run", run, "--runs", runs, "--acts", acts])
    except Parsed as parsed:
        a = parsed.args[0]
    finally:
        argparse.ArgumentParser.parse_args = parse_args
    context = status.inputs(a)
    context["rev"] = rev
    print(json.dumps(status.promotion_line(status.assess(**context, decision=None))))


if __name__ == "__main__":
    main()
