from tools.validate_benchmark_report import validate_report


def valid_report():
    return {
        "schema_version": "1.0",
        "project": "flood-rescue-ai-robot",
        "run_id": "sim-run-0001",
        "run_date_utc": "2026-10-09T02:00:00Z",
        "dataset": {"name": "flood-sim-scenarios", "version": "v1", "split": "held-out"},
        "model": {"name": "detector-baseline", "version": "commit:abc123"},
        "hardware": {"platform": "CPU simulation runner"},
        "software": {"os": "Ubuntu", "python": "3.12"},
        "config": {"seed": 42},
        "metrics": {
            "victim_detection": {"precision": 0.8, "recall": 0.7},
            "navigation": {"mission_completion_rate": 0.6, "collision_count": 0},
            "systems": {"latency_p95_ms": 120.0},
        },
    }


def test_valid_report_passes():
    assert validate_report(valid_report()) == []


def test_missing_provenance_is_rejected():
    report = valid_report()
    del report["dataset"]["version"]
    assert any("$.dataset.version" in error for error in validate_report(report))


def test_placeholder_metric_is_rejected():
    report = valid_report()
    report["model"]["version"] = "TBD"
    assert any("placeholder" in error for error in validate_report(report))


def test_timestamp_without_timezone_is_rejected():
    report = valid_report()
    report["run_date_utc"] = "2026-10-09T02:00:00"
    assert any("timezone" in error for error in validate_report(report))


def test_empty_metrics_are_rejected():
    report = valid_report()
    report["metrics"] = {}
    assert any("$.metrics" in error for error in validate_report(report))


def test_non_finite_metric_is_rejected():
    report = valid_report()
    report["metrics"]["systems"]["latency_p95_ms"] = float("nan")
    assert any("finite" in error for error in validate_report(report))
