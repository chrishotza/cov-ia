"""Regression tests for the synthetic COV-IA policy report.

These tests make no claims about real inference speed or clinical accuracy.
"""
import contextlib
import io
import math
import unittest
from unittest.mock import patch

import cov_ia


class SyntheticPolicyTests(unittest.TestCase):
    def test_all_modes_return_finite_synthetic_metrics(self):
        for mode in cov_ia.COVMode:
            with self.subTest(mode=mode.value):
                runner = cov_ia.InferenceSimulator("test", mode=mode)
                record = runner.step(load=0.7, dist_to_sep=-999)
                self.assertIn(record["model"], runner.get_available_models())
                self.assertIn(record["precision"], runner.get_available_precisions())
                self.assertGreater(record["latency"], 0)
                self.assertTrue(math.isfinite(record["latency"]))
                self.assertGreater(record["accuracy"], 0)
                self.assertLessEqual(record["accuracy"], 1)
                self.assertGreater(record["cost"], 0)

    def test_report_does_not_swap_performance_and_ultra(self):
        # Give each mode a unique, distinguishable synthetic measurement.
        fixture = {
            mode.value: {
                "mode": mode.value,
                "avg_latency": 13.0 + 11.0 * i,
                "avg_accuracy": 0.91 + 0.01 * i,
                "avg_cost": 1.0 + i,
                "models": {"tiny": 1},
                "total_steps": 1,
            }
            for i, mode in enumerate((
                cov_ia.COVMode.PRECISION, cov_ia.COVMode.BALANCED,
                cov_ia.COVMode.PERFORMANCE, cov_ia.COVMode.ULTRA,
            ))
        }

        def fake_mode_run(mode, duration_seconds=60):
            return fixture[mode.value]

        output = io.StringIO()
        with patch.object(cov_ia, "run_mode_simulation", side_effect=fake_mode_run):
            with contextlib.redirect_stdout(output):
                returned = cov_ia.main()
        text = output.getvalue()
        self.assertEqual(len(returned), 4)
        self.assertIn("SIMULACIÓN; NO ES VALIDACIÓN REAL", text)
        for mode in cov_ia.COVMode:
            expected = fixture[mode.value]
            with self.subTest(report_mode=mode.value):
                start = "MODO " + mode.value.upper() + " —"
                self.assertIn(start, text)
                segment = text.split(start, 1)[1].split("MODO ", 1)[0]
                self.assertIn(
                    f"Latencia simulada: {expected['avg_latency']:.0f} ms",
                    segment,
                )
                self.assertIn(
                    f"Accuracy simulada: {expected['avg_accuracy']:.4f}",
                    segment,
                )
                self.assertIn(
                    f"Costo relativo: {expected['avg_cost']:.2f}",
                    segment,
                )


    def test_seeded_simulators_are_reproducible_and_do_not_modify_global_rng(self):
        import random

        random.seed(812)
        expected = [random.random() for _ in range(3)]
        random.seed(812)
        first = random.random()

        a = cov_ia.InferenceSimulator("A", seed=117)
        b = cov_ia.InferenceSimulator("B", seed=117)
        for load in (0.2, 0.7, 1.3):
            self.assertEqual(a.step(load, -999), b.step(load, -999))

        actual = [first, random.random(), random.random()]
        self.assertEqual(actual, expected)

    def test_load_must_be_bounded_before_query_loop(self):
        runner = cov_ia.InferenceSimulator("bounded", seed=9)
        before = (runner.current_model, runner.precision, runner.cooldown, len(runner.history))
        for invalid in (2.01, 1e12, 1e308, True, "untrusted"):
            with self.subTest(load=invalid):
                with self.assertRaises(ValueError):
                    runner.step(invalid, 0.8)
                self.assertEqual(
                    (runner.current_model, runner.precision, runner.cooldown, len(runner.history)),
                    before
                )
        accepted = runner.step(2.0, -999)
        self.assertEqual(accepted["load"], 2.0)
        self.assertEqual(len(runner.history), 1)

    def test_simulation_duration_invalid_values_fail_before_loop(self):
        for invalid in (0, 0.01, -1, 601, float("inf"), float("nan"), True, "60"):
            with self.subTest(duration=invalid):
                with self.assertRaises(ValueError):
                    cov_ia.run_mode_simulation(cov_ia.COVMode.BALANCED, invalid)

    def test_short_synthetic_duration_produces_finite_results(self):
        with contextlib.redirect_stdout(io.StringIO()):
            result = cov_ia.run_mode_simulation(cov_ia.COVMode.BALANCED, 0.2)
        self.assertEqual(result["total_steps"], 2)
        self.assertTrue(math.isfinite(result["avg_latency"]))

    def test_invalid_load_and_separatrix_distance_are_rejected(self):
        runner = cov_ia.InferenceSimulator("input-check")
        for invalid in (-0.1, float("nan"), float("inf"), -float("inf")):
            with self.subTest(load=invalid):
                with self.assertRaisesRegex(ValueError, "load must"):
                    runner.step(invalid, 0)
        for invalid in (float("nan"), float("inf")):
            with self.subTest(distance=invalid):
                with self.assertRaisesRegex(ValueError, "dist_to_sep must"):
                    runner.step(0.5, invalid)


if __name__ == "__main__":
    unittest.main()
