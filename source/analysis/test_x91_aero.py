import unittest

from analysis.x91_aero import analyze, load_config


class X91BaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result = analyze(load_config())

    def test_positive_static_margin(self):
        self.assertGreaterEqual(self.result["static_margin_fraction_mac"], 0.05)
        self.assertLessEqual(self.result["static_margin_fraction_mac"], 0.12)

    def test_usable_thrust_exceeds_weight(self):
        self.assertGreater(self.result["thrust_to_weight_usable"], 1.0)

    def test_approach_speed_has_margin(self):
        self.assertAlmostEqual(
            self.result["recommended_approach_speed_m_s"],
            1.3 * self.result["stall_speed_m_s"],
        )

    def test_endurance_is_plausible_for_initial_sorties(self):
        self.assertGreater(self.result["estimated_endurance_min"], 5.0)
        self.assertLess(self.result["estimated_endurance_min"], 15.0)


if __name__ == "__main__":
    unittest.main()
