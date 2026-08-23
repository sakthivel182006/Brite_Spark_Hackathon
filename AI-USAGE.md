# AI Usage — Brite Spark 2026

## Problem 3 — No Wrong Door

AI assistance was used during development as a development support and reasoning tool.

The final architecture, implementation, integration, testing, debugging, and submission decisions were made and verified by the developer.

AI was not treated as the source of truth. Suggestions were reviewed, adapted where necessary, implemented, and tested against the provided legacy services.

---

## 1. Architecture and Design

AI was used to discuss possible approaches for building the Unified Resident View API.

The main areas discussed were:

- Separating the Resident Index and Benefits Register into independent adapters.

- Using an aggregation layer to combine responses from both legacy systems.

- Keeping legacy-service-specific logic outside the API layer.

- Handling REST/JSON and XML services independently.

- Designing the unified response so that partial source failures do not make the entire API unusable.

The final architecture uses:

```text
Client
  |
  v
Unified API
  |
  +--> Resident Index Adapter --> REST/JSON Service
  |
  +--> Benefits Register Adapter --> XML Service
  |
  v
Aggregator
  |
  v
Unified Resident Response