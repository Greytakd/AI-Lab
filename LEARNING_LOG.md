# Learning Log

A running record of the FDE-prep journey — Python to production, the agent + eval stack, and the road to a Forward Deployed / Applied AI Engineer role. One entry per working session.

---

## Phase 1 — Foundations (Weeks 1–12)

### Week 1 — Set up the war room

**Day 1 — 2026-06-22**
- Locked the daily cadence: weekday **8:00–9:00am** core hour (non-negotiable) + optional **11:30–12:30** lunch block. Starting deliberately below the 15–20 hr target to build the habit before ramping.
- Toolchain completed via `uv add --dev`: **ruff** (lint + format), **pytest** (testing), **ty** (type checking). Python 3.12, numpy, pandas already in place.
- Learned the core `uv` lesson: dev tools install into the project's isolated `.venv`, so they run via `uv run <tool>` (or after `source .venv/bin/activate`) — bare commands hit the system PATH and fail.
- Honest skill audit (1–5 self-rating): comprehensions/idioms **1**, type annotations **1**, error handling **1**, functions-vs-classes **1**, testing **1**, core DS&A **1**. Clean beginner baseline; restarting from scratch after an earlier January attempt.

_Next: Day 2 — Modern Python fundamentals. First fully type-annotated code._
