# Brite Spark 2026 — No Wrong Door

## Problem 3 — No Wrong Door

### Unified Resident View API

A lightweight integration service that combines resident information from two independent legacy systems behind a single API.

The goal is to provide staff with one unified API instead of requiring them to manually check multiple systems.

---

## Problem Overview

This challenge provides two mock legacy services:

### 1. Resident Index

- REST API
- Paginated responses
- 620 resident records
- May return duplicate records across pages

### 2. Benefits Register

- XML API
- 540 benefit records
- Slow responses
- May intermittently return HTTP 500 errors
- Configured with a 40% failure rate for the Day 2 challenge

Our solution provides one API that integrates both services.

---

## Architecture

```text
                          CLIENT / JUDGE
                               |
                               | GET /unified
                               v
                     +------------------+
                     |   Unified API    |
                     |    main.py       |
                     |    Port 8080     |
                     +--------+---------+
                              |
                   +----------+----------+
                   |                     |
                   v                     v
          +-----------------+   +------------------+
          | Resident        |   | Benefits         |
          | Adapter         |   | Adapter          |
          +--------+--------+   +---------+--------+
                   |                      |
                   v                      v
          REST Service :8081      XML Service :8082
                   |                      |
                   v                      v
             620 residents          540 benefits
                   |                      |
                   +----------+-----------+
                              |
                              v
                         aggregator.py
                              |
                              v
                       Unified Response




BRITE SPARK HACK/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── aggregator.py
│   ├── benefits_adapter.py
│   └── resident_adapter.py
│
├── services/
│   ├── rest_service.py
│   ├── xml_service.py
│   ├── _rest_data.json
│   ├── _xml_data.json
│   └── run_both.sh
│
├── tests/
│   ├── __init__.py
│   └── test_api.py
│
├── README.md
├── DECISIONS.md
└── AI-USAGE.md



                         CLIENT / JUDGE
                              |
                              |
                              | GET /unified
                              v
                    +--------------------+
                    |    Unified API     |
                    |      :8080         |
                    +---------+----------+
                              |
                    +---------+---------+
                    |                   |
                    v                   v
          +------------------+  +-------------------+
          | Resident Adapter |  | Benefits Adapter  |
          +--------+---------+  +---------+---------+
                   |                      |
                   v                      v
          Resident Index          Benefits Register
             REST :8081               XML :8082
                   |                      |
                   v                      v
             620 residents          540 benefits
                   |                      |
                   +----------+-----------+
                              |
                              v
                        Aggregator
                              |
                              v
                     Unified Response

                     