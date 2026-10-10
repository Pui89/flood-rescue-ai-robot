import unittest
from apps.pui89_app.main import AnalyzeRequest, Candidate, analyze


class FloodAppTests(unittest.TestCase):
    def test_invalid_lidar_forces_hold(self):
        result = analyze(AnalyzeRequest(rgb_available=True, thermal_available=True,
            lidar_valid=False, timestamp_skew_ms=0, water_depth_m=0,
            current_speed_mps=0, candidates=[]))
        self.assertEqual(result["status"], "SAFE_HOLD")
        self.assertEqual(result["route_status"], "NOT_EVALUATED")

    def test_high_hazard_requires_human_review(self):
        result = analyze(AnalyzeRequest(rgb_available=True, thermal_available=False,
            lidar_valid=True, timestamp_skew_ms=0, water_depth_m=.8,
            current_speed_mps=.1, candidates=[]))
        self.assertEqual(result["route_status"], "HUMAN_REVIEW")
        self.assertFalse(result["actuator_commands_sent"])

    def test_unstable_track_is_insufficient_evidence(self):
        c = Candidate(track_id="t1", visual_confidence=.9, thermal_support=False,
                      track_stability_frames=1, distance_m=4)
        result = analyze(AnalyzeRequest(rgb_available=True, thermal_available=False,
            lidar_valid=True, timestamp_skew_ms=1, water_depth_m=.1,
            current_speed_mps=.1, candidates=[c]))
        self.assertEqual(result["candidate_reviews"][0]["status"], "INSUFFICIENT_EVIDENCE")


if __name__ == "__main__":
    unittest.main()
