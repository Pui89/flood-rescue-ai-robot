"""Write a deterministic synthetic reconnaissance map as JSON."""
import argparse
import json
from pathlib import Path
from .grid import EvidenceGrid

def build_demo_map():
    grid = EvidenceGrid(10.0, 8.0, 1.0)
    samples = [
        (1.2, 1.3, "clear", 0.95, "synthetic_rgb"),
        (2.1, 1.4, "person", 0.82, "synthetic_rgb"),
        (3.3, 1.5, "debris", 0.91, "synthetic_depth"),
        (4.1, 1.4, "water", 0.88, "synthetic_depth"),
        (4.4, 1.7, "water", 0.78, "synthetic_depth"),
        (6.2, 2.1, "vehicle", 0.90, "synthetic_rgb"),
        (7.2, 4.1, "building", 0.96, "synthetic_rgb"),
        (8.2, 5.1, "unknown", 0.35, "synthetic_rgb"),
    ]
    for sample in samples:
        grid.add_observation(*sample)
    return grid

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", default="rescue-map-demo.json")
    args = parser.parse_args()
    payload = build_demo_map().to_dict()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print("Wrote synthetic map:", output)
    print("Grid: {}x{}; observed={}; unknown={}".format(
        payload["cols"], payload["rows"], payload["observed_cells"], payload["unknown_cells"]))
    print("Synthetic evidence aggregation only; not a validated flood map.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
