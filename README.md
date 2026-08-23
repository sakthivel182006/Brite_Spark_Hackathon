# Brite Spark 2026 — No Wrong Door

## Problem 3 — No Wrong Door

### Unified Resident View API

A lightweight integration service that combines resident information from two independent legacy systems behind a single API.

The goal is to provide staff with **one unified API** instead of requiring them to manually check multiple systems.

---

## Problem Overview

This challenge provides two mock legacy services.

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
                 |     main.py      |
                 |    Port 8080     |
                 +--------+---------+
                          |
                +---------+---------+
                |                   |
                v                   v
        +---------------+   +----------------+
        | Resident      |   | Benefits       |
        | Adapter       |   | Adapter        |
        +-------+-------+   +--------+-------+
                |                    |
                v                    v
        REST Service :8081    XML Service :8082
                |                    |
                v                    v
        620 residents          540 benefits
                |                    |
                +---------+----------+
                          |
                          v
                    aggregator.py
                          |
                          v
                   Unified Response
VS Code Setup and How to Run
1. Open the Project in VS Code

Open Visual Studio Code and open the project folder:

BRITE SPARK HACK

The project structure should look like:

BRITE SPARK HACK/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── resident_adapter.py
│   ├── benefits_adapter.py
│   └── aggregator.py
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
2. Requirements

Only Python 3 is required.

Check Python:

python --version

Example:

Python 3.13.x

No database, Node.js, or frontend framework is required for the core solution.

3. Open VS Code Terminal

In VS Code:

Terminal → New Terminal

Make sure the terminal is inside the project directory:

D:\chrome download\BRITE SPARK\BRITE SPARK HACK>

If it is not, run:

cd "D:\chrome download\BRITE SPARK\BRITE SPARK HACK"
4. Start the Project

The project uses three running services.

Open three VS Code terminals.

A fourth terminal can be used for testing.

VS Code Terminal 1 — Resident Index

Open Terminal 1 and run:

python services\rest_service.py --port 8081

Expected output:

Resident Index (REST) on http://127.0.0.1:8081
620 records across 27 pages of 25
Important

Keep Terminal 1 running.

Do not close it.

VS Code Terminal 2 — Benefits Register

Open Terminal 2 and run:

python services\xml_service.py --port 8082 --failure-rate 0.40

Expected output:

Benefits Register (XML) on http://127.0.0.1:8082
540 records | failure rate 40% | delay 0.7-2.4s
Important

Keep Terminal 2 running.

The 40% failure rate is intentional and is part of the Day 2 challenge scenario.

Do not change it to 0.

VS Code Terminal 3 — Unified API

Open Terminal 3 and run:

python -m app.main

The Unified API runs on:

http://127.0.0.1:8080
Important

Keep Terminal 3 running.

5. VS Code Terminal 4 — Testing

Open Terminal 4.

Make sure you are in the project directory:

cd "D:\chrome download\BRITE SPARK\BRITE SPARK HACK"

Run:

python -m tests.test_api

A successful run should show:

================================
UNIFIED API TEST
================================
Status: complete
Residents: 620
Benefits: 540
Benefits available: True
Benefits error: None

Because the Benefits Register intentionally has a 40% failure rate, you may also see:

================================
UNIFIED API TEST
================================
Status: partial
Residents: 620
Benefits: 0
Benefits available: False
Benefits error: Benefits Register returned HTTP 500

The partial result is expected.

6. Test the Unified API Directly

With all three services running, use Terminal 4:

curl http://127.0.0.1:8080/unified

This calls the Unified API.

The request flow is:

GET /unified
      |
      v
   main.py
      |
      v
 aggregator.py
      |
      +----------------------+
      |                      |
      v                      v
Resident Adapter       Benefits Adapter
      |                      |
      v                      v
 REST :8081              XML :8082
      |                      |
      +----------+-----------+
                 |
                 v
          Unified Response
7. Health Checks
Resident Index

Run in Terminal 4:

curl http://127.0.0.1:8081/health

Expected:

{
  "status": "ok",
  "service": "resident-index"
}
Benefits Register

Run:

curl http://127.0.0.1:8082/health

Expected:

<?xml version="1.0"?>
<Health>
    <Status>ok</Status>
</Health>
Unified API

Run:

curl http://127.0.0.1:8080/health

Expected:

{
  "status": "ok",
  "service": "unified-api"
}
8. Quick Demo Command

For a clean demonstration of the Unified API:

curl -s http://127.0.0.1:8080/unified | python -c "import sys,json; d=json.load(sys.stdin); print('================================'); print('UNIFIED API TEST'); print('================================'); print('Status:',d['status']); print('Residents:',d['resident_index']['record_count']); print('Benefits:',d['benefits_register']['record_count']); print('Benefits available:',d['benefits_register']['available']); print('Benefits error:',d['benefits_register']['error'])"

Successful output:

================================
UNIFIED API TEST
================================
Status: complete
Residents: 620
Benefits: 540
Benefits available: True
Benefits error: None

If the Benefits Register fails, a partial response is expected because the service is configured with a 40% failure rate.

9. Understanding the Three Terminals
+---------------------------------------------+
| Terminal 1                                  |
| Resident Index                              |
| Port 8081                                   |
|                                             |
| 620 resident records                        |
+----------------------+----------------------+
                       |
                       |
+----------------------v----------------------+
| Terminal 2                                  |
| Benefits Register                           |
| Port 8082                                   |
|                                             |
| 540 benefit records                         |
| 40% intentional failure rate                |
+----------------------+----------------------+
                       |
                       |
+----------------------v----------------------+
| Terminal 3                                  |
| Unified API                                 |
| Port 8080                                   |
|                                             |
| Combines both sources                       |
+---------------------------------------------+
                       ^
                       |
+----------------------+----------------------+
| Terminal 4                                  |
| Tests / curl                                |
|                                             |
| Used to verify the application              |
+---------------------------------------------+
10. Stopping the Project

When finished, stop each running service with:

Ctrl + C

Do this in:

Terminal 1
Terminal 2
Terminal 3

Terminal 4 does not need to remain running.

11. Complete Startup Summary

Every time you want to run the project from scratch:

Terminal 1 — Resident Index
cd "D:\chrome download\BRITE SPARK\BRITE SPARK HACK"
python services\rest_service.py --port 8081
Terminal 2 — Benefits Register
cd "D:\chrome download\BRITE SPARK\BRITE SPARK HACK"
python services\xml_service.py --port 8082 --failure-rate 0.40
Terminal 3 — Unified API
cd "D:\chrome download\BRITE SPARK\BRITE SPARK HACK"
python -m app.main
Terminal 4 — Tests
cd "D:\chrome download\BRITE SPARK\BRITE SPARK HACK"
python -m tests.test_api

Then optionally:

curl http://127.0.0.1:8080/unified
12. Expected Final State
Resident Index
      |
      | :8081
      v
Resident Adapter
      |
      |
      +----------------+
      |                |
      |                v
      |         Benefits Adapter
      |                |
      |                | :8082
      |                v
      |         Benefits Register
      |
      v
  Aggregator
      |
      v
 Unified API
      |
      | :8080
      v
    Client

The main endpoint for the hackathon demonstration is:

GET http://127.0.0.1:8080/unified