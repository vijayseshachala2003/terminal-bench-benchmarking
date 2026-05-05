import json
import os
from pathlib import Path

BASE = Path(__file__).parent

TAXONOMY = {
    "dns-resolution-chain-debugging": "Service Failure",
    "edge-ai-iot-system_v1": "Runtime Errors",
    "epoch-fence-repair-canonical-v2": "Service Failure",
    "fs-relative-path": "Runtime Errors",
    "iot-sensor-processor": "Runtime Errors",
    "lockfree-queue-race-debug": "Runtime Errors",
    "multi-file-reasoning": "Runtime Errors",
    "mysql-query-optimise": "Runtime Errors",
    "set-intersection-timeout": "Test Failures",
    "sqlite-fs-indexer-lockswap": "Version Conflict",
    "stack-vm": "Runtime Errors",
}

# model display name → (timestamp_dir, model_folder_name)
MODELS = [
    ("Claude Opus 4.6",       "2026-05-05__07-57-55", "claude-opus-4-6"),
    ("GPT 5.2",               "2026-04-30__11-18-27", "openai_gpt-5.2"),
    ("Grok-code-fast-1",      "2026-04-30__11-18-27", "xai_grok-code-fast-1"),
    ("Gemini 3-pro-preview",  "2026-05-05__07-57-55", "gemini_gemini-3-pro-preview"),
]


def count_results(model_dir: Path) -> dict:
    passed = failed = errors = 0
    if not model_dir.exists():
        return {"passed": 0, "failed": 0, "errors": 10, "total": 10}

    for run_dir in model_dir.iterdir():
        if not run_dir.is_dir():
            continue
        result_path = run_dir / "result.json"
        if not result_path.exists():
            errors += 1
            continue
        with open(result_path) as f:
            result = json.load(f)

        if result.get("exception_info") is not None:
            errors += 1
        elif (
            result.get("verifier_result") is None
            or result["verifier_result"].get("rewards", {}).get("reward", 0.0) != 1.0
        ):
            failed += 1
        else:
            passed += 1

    total = passed + failed + errors
    return {"passed": passed, "failed": failed, "errors": errors, "total": total}


def pass_rate(stats: dict) -> str:
    total = stats["total"]
    if total == 0:
        return "N/A"
    pct = int(round(stats["passed"] / total * 100))
    return f"{pct}% ({stats['passed']}/{total})"


def generate_readme(task: str) -> str:
    taxonomy = TAXONOMY.get(task, "Unknown")
    rows = []
    for display_name, ts_dir, model_folder in MODELS:
        model_dir = BASE / ts_dir / "grouped" / task / model_folder
        stats = count_results(model_dir)
        rows.append((display_name, stats))

    col1 = max(len(r[0]) for r in rows)
    col1 = max(col1, len("Model"))

    header = (
        f"## {task}\n\n"
        f"- **Task Taxonomy:** {taxonomy}\n\n"
        f"| {'Model':<{col1}} | Passed | Failed | Errors | Pass Rate       |\n"
        f"|{'-' * (col1 + 2)}|--------|--------|--------|-----------------|\n"
    )

    body = ""
    for display_name, stats in rows:
        body += (
            f"| {display_name:<{col1}} "
            f"| {stats['passed']:<6} "
            f"| {stats['failed']:<6} "
            f"| {stats['errors']:<6} "
            f"| {pass_rate(stats):<15} |\n"
        )

    return header + body


out_base = BASE / "results"

for task in TAXONOMY:
    out_dir = out_base / task
    os.makedirs(out_dir, exist_ok=True)
    content = generate_readme(task)
    readme_path = out_dir / "README.md"
    with open(readme_path, "w") as f:
        f.write(content)
    print(f"Written: {readme_path.relative_to(BASE)}")

print(f"\nAll READMEs written to {out_base}/")
