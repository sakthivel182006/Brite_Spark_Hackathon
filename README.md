# Brite Spark 2026 — No Wrong Door

## Problem 3 — No Wrong Door

### Unified Resident View API

A lightweight integration service that combines resident information from two independent legacy systems behind a single API.

The goal is to provide staff with **one unified API** instead of requiring them to manually check multiple systems.

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
                              │
                              │ GET /unified
                              ▼
                    ┌──────────────────┐
                    │   Unified API    │
                    │    main.py       │
                    │    Port 8080     │
                    └────────┬─────────┘
                             │
                 ┌───────────┴───────────┐
                 │                       │
                 ▼                       ▼
        ┌─────────────────┐    ┌──────────────────┐
        │ Resident        │    │ Benefits         │
        │ Adapter         │    │ Adapter          │
        └────────┬────────┘    └────────┬─────────┘
                 │                      │
                 ▼                      ▼
        REST Service :8081       XML Service :8082
                 │                      │
                 ▼                      ▼
           620 residents          540 benefits
                 │                      │
                 └──────────┬───────────┘
                            ▼
                     aggregator.py
                            │
                            ▼
                     Unified Response
