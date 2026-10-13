"""Every path:function citation in LAW.md must name a real file and a real definition."""
import os
import re
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Citations(unittest.TestCase):
    def test_every_citation_resolves(self):
        with open(os.path.join(ROOT, "LAW.md")) as f:
            text = f.read()
        cites = set(re.findall(r"`((?:kernel|judge|harness|tools)/[a-z_]+\.py):([A-Za-z_]+)`", text))
        self.assertGreater(len(cites), 25)
        for path, name in sorted(cites):
            full = os.path.join(ROOT, path)
            self.assertTrue(os.path.exists(full), path)
            with open(full) as f:
                src = f.read()
            self.assertTrue(re.search(rf"^(def {name}\(|{name} = )", src, re.M), f"{path}:{name} not defined")
        files = set(re.findall(r"`((?:kernel|judge|harness|tools)/[a-z_]+\.py)`", text))
        for path in files:
            self.assertTrue(os.path.exists(os.path.join(ROOT, path)), path)
        for path in ("genesis.template.json", ".github/workflows/judge.yml", "kernel2/README.md"):
            self.assertIn(path, text)
            self.assertTrue(os.path.exists(os.path.join(ROOT, path)))


if __name__ == "__main__":
    unittest.main()
