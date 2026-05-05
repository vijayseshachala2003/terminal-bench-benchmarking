import json
import os
import shutil
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent

TIMESTAMP_DIRS = [
    "2026-04-30__11-18-27",
    "2026-05-05__07-57-55",
]


def sanitize_model(model_name: str) -> str:
    return model_name.replace("/", "_")


def reorganize(timestamp_dir: Path) -> None:
    summary = defaultdict(lambda: defaultdict(list))
    run_dirs = []

    for entry in timestamp_dir.iterdir():
        if not entry.is_dir():
            continue
        if "__" not in entry.name:
            continue
        config_path = entry / "config.json"
        if not config_path.exists():
            continue
        run_dirs.append(entry)

    for run_dir in run_dirs:
        with open(run_dir / "config.json") as f:
            cfg = json.load(f)

        model_name = cfg["agent"]["model_name"]
        task_name = run_dir.name.rsplit("__", 1)[0]
        sanitized = sanitize_model(model_name)

        target_dir = timestamp_dir / "grouped" / task_name / sanitized
        os.makedirs(target_dir, exist_ok=True)

        dest = target_dir / run_dir.name
        shutil.move(str(run_dir), str(dest))
        summary[task_name][model_name].append(run_dir.name)

    print(f"\n=== {timestamp_dir.name} ===")
    for task in sorted(summary):
        print(f"\ntask: {task}")
        for model in sorted(summary[task]):
            count = len(summary[task][model])
            print(f"  model: {model}  ({count} trajectories)")


for ts in TIMESTAMP_DIRS:
    ts_path = BASE / ts
    if ts_path.exists():
        reorganize(ts_path)
    else:
        print(f"Skipping missing: {ts_path}")

print("\nDone.")
