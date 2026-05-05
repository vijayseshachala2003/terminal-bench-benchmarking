# Terminal-Bench Evaluation Results

## What We Did

We ran **terminal-bench** — a benchmark that tests AI coding agents on real terminal-based engineering tasks — across 4 models and 11 tasks, collecting 10 independent runs per model per task (110 runs per model, 440 total).

Each run placed the agent inside a Docker container with a broken or incomplete system. The agent had to diagnose and fix it using only the terminal. An automated test suite then verified the result and produced a binary pass/fail score.

---

## Tasks Evaluated

All 11 tasks are included directly in this repository. No external dependencies or additional repos are required — everything needed to browse results is self-contained here. Each task has its own detailed README in the subdirectories below.

| Task | Taxonomy |
|------|----------|
| [dns-resolution-chain-debugging](./dns-resolution-chain-debugging/README.md) | Service Failure |
| [edge-ai-iot-system_v1](./edge-ai-iot-system_v1/README.md) | Runtime Errors |
| [epoch-fence-repair-canonical-v2](./epoch-fence-repair-canonical-v2/README.md) | Service Failure |
| [fs-relative-path](./fs-relative-path/README.md) | Runtime Errors |
| [iot-sensor-processor](./iot-sensor-processor/README.md) | Runtime Errors |
| [lockfree-queue-race-debug](./lockfree-queue-race-debug/README.md) | Runtime Errors |
| [multi-file-reasoning](./multi-file-reasoning/README.md) | Runtime Errors |
| [mysql-query-optimise](./mysql-query-optimise/README.md) | Runtime Errors |
| [set-intersection-timeout](./set-intersection-timeout/README.md) | Test Failures |
| [sqlite-fs-indexer-lockswap](./sqlite-fs-indexer-lockswap/README.md) | Version Conflict |
| [stack-vm](./stack-vm/README.md) | Runtime Errors |

---

## Models Evaluated

Four models were evaluated. Due to two separate job runs, Claude and Gemini results come from a later, cleaner run.

| Model | Provider | Job Run | Folder |
|-------|----------|---------|--------|
| Claude Opus 4.6 | Anthropic | 2026-05-05 | `claude-opus-4-6` |
| GPT 5.2 | OpenAI | 2026-04-30 | `openai_gpt-5.2` |
| Grok-code-fast-1 | xAI | 2026-04-30 | `xai_grok-code-fast-1` |
| Gemini 3-pro-preview | Google | 2026-05-05 | `gemini_gemini-3-pro-preview` |

> The April 30 run included all 4 models but its Claude and Gemini results were superseded by the cleaner May 5 re-run. GPT and Grok have no May 5 data, so their April 30 results are used as-is.

---

## How Results Were Computed

Each run folder contains a `result.json`. Every run is classified into one of three outcomes:

| Outcome | Condition |
|---------|-----------|
| **Passed** | `verifier_result.rewards.reward == 1.0` — all tests passed |
| **Failed** | `verifier_result.rewards.reward == 0.0` — ran to completion but tests failed |
| **Error** | `exception_info != null` — the run crashed before the verifier could run |

**Pass Rate = Passed / 10** — errors count against the denominator (a crashed run is not a free pass).

---

## Overall Results (110 runs per model)

| Model | Passed | Failed | Errors | Overall Pass Rate |
|-------|--------|--------|--------|-------------------|
| Claude Opus 4.6 | 58 | 26 | 26 | **52.7%** |
| GPT 5.2 | 42 | 52 | 16 | **38.2%** |
| Gemini 3-pro-preview | 32 | 77 | 1 | **29.1%** |
| Grok-code-fast-1 | 25 | 72 | 13 | **22.7%** |

---

## Per-Task Summary

| Task | Claude Opus 4.6 | GPT 5.2 | Grok-code-fast-1 | Gemini 3-pro-preview |
|------|-----------------|---------|------------------|----------------------|
| dns-resolution-chain-debugging | 70% | 90% | 30% | 50% |
| edge-ai-iot-system_v1 | 100% | 0% | 0% | 0% |
| epoch-fence-repair-canonical-v2 | 0% | 0% | 10% | 0% |
| fs-relative-path | 80% | 100% | 80% | 100% |
| iot-sensor-processor | 100% | 0% | 20% | 0% |
| lockfree-queue-race-debug | 50% | 10% | 10% | 20% |
| multi-file-reasoning | 0% | 0% | 0% | 0% |
| mysql-query-optimise | 0% | 70% | 0% | 0% |
| set-intersection-timeout | 100% | 100% | 100% | 100% |
| sqlite-fs-indexer-lockswap | 80% | 30% | 0% | 50% |
| stack-vm | 0% | 20% | 0% | 0% |

---

## Post-sanity results (`post_sanity_results/`)

The [`post_sanity_results/`](./post_sanity_results/) directory holds **one JSON file per evaluated task** (11 files, same task names as in [Tasks Evaluated](#tasks-evaluated)). Each file is a **post-run sanity summary**: how failures distribute across trials, whether the task looks sound versus underspecified, and structured evidence from runs.

Typical fields in each `{task_name}.json`:

| Field | Meaning |
|-------|---------|
| `task` | Task id (matches directory name) |
| `total_trials` | Number of runs summarized |
| `total_failed` | Count of failed trials |
| `pass_rate` | Aggregate pass rate string |
| `outcome` | High-level sanity outcome (e.g. whether the task passes sanity checks) |
| `explanation` | Short narrative on failure patterns and task quality |
| `consistent_failures` | Failures that show up across trials |
| `trials_evidence` | Per-trial rows: model, paths to trajectories, failed/passed tests, messages |

Use these files to review **whether failures look like legitimate task difficulty versus specification or harness issues**, without opening every `result.json` by hand.

---

## Folder Structure

```
jobs_new/
├── README.md                         ← this file (repo root)
├── post_sanity_results/              ← per-task post-sanity summaries (JSON)
│   └── {task_name}.json
├── results/
│   └── {task_name}/README.md         ← per-task breakdown (11 files)
├── 2026-04-30__11-18-27/
│   ├── config.json                   ← job configuration
│   ├── result.json                   ← aggregated job results
│   ├── job.log
│   └── grouped/
│       └── {task}/{model}/{run_id}/  ← individual run data
└── 2026-05-05__07-57-55/
    ├── config.json
    ├── result.json
    ├── job.log
    └── grouped/
        └── {task}/{model}/{run_id}/
```

Each `run_id` folder contains:
- `result.json` — full run metadata, token usage, reward
- `agent/trajectory.json` — complete step-by-step agent interaction
- `agent/recording.cast` — asciinema terminal recording
- `verifier/reward.txt` — raw score (`0` or `1`)
- `verifier/ctrf.json` — individual test-level pass/fail results
