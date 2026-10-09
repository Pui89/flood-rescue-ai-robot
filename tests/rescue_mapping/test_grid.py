import unittest
from simulation.rescue_mapping.demo import build_demo_map
from simulation.rescue_mapping.grid import EvidenceGrid

class EvidenceGridTests(unittest.TestCase):
    def test_dimensions_and_unknown_count(self):
        grid = EvidenceGrid(4.0, 3.0, 1.0)
        self.assertEqual((grid.cols, grid.rows), (4, 3))
        self.assertEqual(grid.to_dict()["unknown_cells"], 12)

    def test_observations_aggregate(self):
        grid = EvidenceGrid(4.0, 4.0, 1.0)
        grid.add_observation(0.2, 0.3, "water", 0.8, "depth")
        grid.add_observation(0.7, 0.8, "water", 1.0, "thermal")
        cell = grid.cells[(0, 0)]
        self.assertEqual(cell.observations, 2)
        self.assertEqual(cell.hazard_observations, 2)
        self.assertAlmostEqual(cell.mean_confidence, 0.9)
        self.assertEqual(cell.sources, {"depth", "thermal"})

    def test_unknown_is_not_clear(self):
        grid = EvidenceGrid(2.0, 2.0, 1.0)
        grid.add_observation(0.5, 0.5, "unknown", 0.2)
        self.assertEqual(grid.cells[(0, 0)].dominant_label, "unknown")
        self.assertEqual(grid.to_dict()["unknown_cells"], 3)

    def test_out_of_bounds_rejected(self):
        grid = EvidenceGrid(2.0, 2.0, 1.0)
        for point in [(-0.1, 0.0), (2.0, 0.0), (0.0, 2.0)]:
            with self.subTest(point=point), self.assertRaises(ValueError):
                grid.add_observation(*point, "water")

    def test_invalid_values_rejected(self):
        grid = EvidenceGrid(2.0, 2.0, 1.0)
        with self.assertRaises(ValueError):
            grid.add_observation(0.2, 0.2, "water", 1.1)
        with self.assertRaises(ValueError):
            grid.add_observation(0.2, 0.2, "unsupported")
        with self.assertRaises(ValueError):
            EvidenceGrid(2.1, 2.0, 1.0)

    def test_demo_summary(self):
        payload = build_demo_map().to_dict()
        self.assertEqual(payload["observed_cells"], 7)
        self.assertEqual(payload["unknown_cells"], 73)
        self.assertEqual(payload, build_demo_map().to_dict())

if __name__ == "__main__":
    unittest.main()
