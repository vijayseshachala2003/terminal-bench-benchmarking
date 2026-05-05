import shutil
from pathlib import Path

BASE = Path(__file__).parent
OUT = BASE / "benchmark_data"

# Exact source for each model: (timestamp_dir, model_folder)
MODEL_SOURCES = [
    ("claude-opus-4-6",                  "2026-05-05__07-57-55", "claude-opus-4-6"),
    ("openai_gpt-5.2",                   "2026-04-30__11-18-27", "openai_gpt-5.2"),
    ("xai_grok-code-fast-1",             "2026-04-30__11-18-27", "xai_grok-code-fast-1"),
    ("gemini_gemini-3-pro-preview",      "2026-05-05__07-57-55", "gemini_gemini-3-pro-preview"),
]

TASKS = [
    "dns-resolution-chain-debugging",
    "edge-ai-iot-system_v1",
    "epoch-fence-repair-canonical-v2",
    "fs-relative-path",
    "iot-sensor-processor",
    "lockfree-queue-race-debug",
    "multi-file-reasoning",
    "mysql-query-optimise",
    "set-intersection-timeout",
    "sqlite-fs-indexer-lockswap",
    "stack-vm",
]

total = 0
for task in TASKS:
    for model_folder, ts_dir, src_model_folder in MODEL_SOURCES:
        src = BASE / ts_dir / "grouped" / task / src_model_folder
        dst = OUT / task / model_folder
        if not src.exists():
            print(f"  MISSING: {src.relative_to(BASE)}")
            continue
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
        run_count = sum(1 for p in dst.iterdir() if p.is_dir())
        print(f"  Copied {run_count:2d} runs  {task}/{model_folder}")
        total += run_count

print(f"\nDone. {total} run folders copied → {OUT.relative_to(BASE)}/")
