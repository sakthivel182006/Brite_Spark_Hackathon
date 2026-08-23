# Brite Spark 2026 — No Wrong Door

## Problem 3 — Unified Resident View API

A lightweight Python API that combines data from two legacy systems:

- **Resident Index** — REST/JSON, 620 residents, paginated
- **Benefits Register** — XML, 540 benefits, slow and may return HTTP 500

## Architecture

```text
                    Client
                      |
                      v
              Unified API :8080
                      |
              +-------+-------+
              |               |
              v               v
       Resident Adapter   Benefits Adapter
              |               |
              v               v
        REST :8081          XML :8082
              |               |
              +-------+-------+
                      |
                      v
                 Aggregator
                      |
                      v
              Unified Response
Technology Stack
Python 3
REST API
JSON
XML
HTTP
Python Standard Library
Project Structure
BRITE SPARK HACK/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── resident_adapter.py
│   ├── benefits_adapter.py
│   ├── aggregator.py
│   └── models.py
├── services/
│   ├── rest_service.py
│   ├── xml_service.py
│   ├── _rest_data.json
│   ├── _xml_data.json
│   └── run_both.sh
├── tests/
│   ├── __init__.py
│   └── test_api.py
├── README.md
├── DECISIONS.md
└── AI-USAGE.md
How to Run

Open 4 terminals in the project folder.

Terminal 1 — Resident Index
python services\rest_service.py --port 8081
Terminal 2 — Benefits Register
python services\xml_service.py --port 8082 --failure-rate 0.40
Terminal 3 — Unified API
python -m app.main

Unified API:

http://127.0.0.1:8080
Terminal 4 — Test
python -m tests.test_api
Main API
GET http://127.0.0.1:8080/unified

Test:

curl http://127.0.0.1:8080/unified
Expected Complete Response
Status: complete
Residents: 620
Benefits: 540
Benefits available: True
Benefits error: None
Graceful Degradation

The Benefits Register intentionally has a 40% failure rate.

If it returns HTTP 500:

Status: partial
Residents: 620
Benefits: 0
Benefits available: False
Benefits error: Benefits Register returned HTTP 500

The Resident data is still returned instead of failing the entire Unified API.

Key Features
REST integration
XML integration
Pagination
Duplicate resident removal
Graceful degradation
HTTP 500 handling
Unified API
Integration testing
Documentation
DECISIONS.md — Engineering decisions and degradation policy
AI-USAGE.md — AI assistance and verification