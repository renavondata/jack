"""BRIEF-C2b's election: exact downstream arithmetic and signed-prefix replay."""
from fractions import Fraction
import math
import unittest

from sim import election as el


class ElectionMathTest(unittest.TestCase):
    def test_draw_hashes_raw_signature_bytes_as_a_big_endian_integer(self):
        draw = el.draw((Fraction(0),) * 3, bytes(64))
        self.assertEqual(draw["u"], int("f5a5fd42d16a20302798ef6ed309979b43003d2320d9f0e8ea9831a92759fb4b", 16))
        self.assertEqual(draw["arm"], 2)
        self.assertEqual(draw["propensity"], Fraction(draw["cuts"][3] - draw["cuts"][2], 2 ** 256))
        for sigma in (b"a" * 63, b"a" * 65, "a" * 64):
            with self.subTest(sigma=sigma), self.assertRaises(ValueError):
                el.draw((Fraction(0),) * 3, sigma)

    def test_invite_p_is_half_up_laplace_success_rate_not_propensity(self):
        self.assertEqual(el.success_rate([]), 500)
        self.assertEqual(el.success_rate([1]), 667)
        self.assertEqual(el.success_rate([0]), 333)
        self.assertEqual(el.success_rate([0] * 14), 63)  # 62.5 rounds up
        self.assertEqual(el.success_rate([0] * 2000), 1)
        self.assertEqual(el.success_rate([1] * 2000), 999)
        with self.assertRaises(ValueError):
            el.success_rate([True])

    def test_importance_weight_uses_saved_grid_mass_and_exact_identity(self):
        gains = (Fraction(0),) * 3
        old = el.draw(gains, b"a" * 64)
        g = el.gain([2] * 6)
        after = el.update(gains, old["arm"], g, old["propensity"])
        self.assertEqual(after[old["arm"]], g / old["propensity"])
        self.assertEqual(el.draw(after, b"a" * 64), el.draw(after, b"a" * 64))
        self.assertNotEqual(el.cuts(after), old["cuts"])
        updated = el.update(after, old["arm"], g, old["propensity"])
        self.assertEqual(updated[old["arm"]], 2 * g / old["propensity"])
        # Integrate over the three grid intervals, not an approximate float pi.
        for k in range(3):
            boundaries = el.cuts(after)
            identity = sum(Fraction(boundaries[a + 1] - boundaries[a], el.GRID) *
                           (g / Fraction(boundaries[a + 1] - boundaries[a], el.GRID) if a == k else 0) for a in range(3))
            self.assertEqual(identity, g)

    def test_theorem_constants_and_grid_boundaries(self):
        self.assertEqual((el.K, el.HORIZON, el.D), (3, 84, 3))
        self.assertEqual(el.GAMMA, math.sqrt(3 * math.log(3) / ((math.e - 1) * 84)))
        self.assertEqual(el.ETA, el.GAMMA / 3)
        boundaries = el.cuts((Fraction(0),) * 3)
        self.assertEqual(boundaries, (0, math.floor((1 / 3) * 2 ** 256), math.floor((2 / 3) * 2 ** 256), 2 ** 256))
        for k in range(3):
            mass = Fraction(boundaries[k + 1] - boundaries[k], 2 ** 256)
            self.assertEqual(el.select(boundaries, boundaries[k]), (k, mass))
            self.assertEqual(el.select(boundaries, boundaries[k + 1] - 1), (k, mass))
        self.assertEqual(el.select(boundaries, 2 ** 256 - 1)[0], 2)

    def test_gain_endpoints_representation_and_bad_round_kept(self):
        self.assertEqual(el.gain([1] * 6), 0)
        self.assertEqual(el.gain([999] * 6), 1)
        self.assertEqual(el.gain([2] * 6), Fraction(math.fsum(math.log(2) for _ in range(6)) / 6 / math.log(999)))
        self.assertAlmostEqual(float(el.gain([999] * 5 + [1])), 5 / 6)
        for ns in ([999] * 5, [999] * 7, [0] * 6, [1000] * 6, [True] * 6):
            with self.subTest(ns=ns), self.assertRaises(ValueError):
                el.gain(ns)
