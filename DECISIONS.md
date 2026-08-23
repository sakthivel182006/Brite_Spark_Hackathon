<<<<<<< HEAD

=======
# Engineering Decisions — Brite Spark 2026

## Problem 3 — No Wrong Door

### 1. Architecture

We use separate adapters for each external source:

- `resident_adapter.py` handles the Resident Index REST service.
- `benefits_adapter.py` handles the Benefits Register XML service.
- `aggregator.py` combines the results.
- `main.py` exposes the unified API.

This keeps each source independent from the aggregation logic.

---

## 2. Degradation Policy

The unified API must return useful information even when one source is unavailable.

We never silently replace unavailable source data with an empty successful result.

The response contains:

- overall status
- source availability
- record count
- available records
- error information when a source fails

---

### Resident Index — Source Failure

If the Resident Index cannot be successfully retrieved:

```text
Resident Index
    ↓
Unavailable
    ↓
Unified API returns partial response
>>>>>>> 45b3cd3 (docs: add VS Code setup and run instructions)
