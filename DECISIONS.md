# Engineering Decisions

## Brite Spark 2026 — No Wrong Door

### Problem 3 — Unified Resident View API

This document records the main engineering decisions made for the Unified Resident View API.

---

## 1. Use a Unified API

The project provides a single API endpoint:

```text
GET /unified
```

The purpose is to hide the complexity of multiple legacy systems from the client.

Instead of calling two separate services, the client calls the Unified API.

---

## 2. Use Adapter Pattern

Each legacy service uses a separate adapter.

### Resident Adapter

```text
app/resident_adapter.py
```

Responsible for communicating with the Resident Index REST API.

### Benefits Adapter

```text
app/benefits_adapter.py
```

Responsible for communicating with the Benefits Register XML API.

This keeps the legacy service-specific logic separated from the main application.

---

## 3. Use Aggregator Pattern

The aggregator combines the results from both adapters.

```text
app/aggregator.py
```

The flow is:

```text
Resident Adapter
       |
       +------+
              |
              v
          Aggregator
              ^
              |
       +------+
       |
Benefits Adapter
```

The aggregator creates the final Unified API response.

---

## 4. Handle Pagination

The Resident Index provides paginated data.

The Resident Adapter retrieves all available pages instead of reading only the first page.

This ensures that the Unified API can process the complete Resident Index dataset.

---

## 5. Remove Duplicate Residents

The Resident Index may return duplicate residents across pages.

The application uses the resident identifier as the deduplication key.

The same resident should not appear multiple times in the final resident collection.

---

## 6. Handle XML Data

The Benefits Register provides XML instead of JSON.

The Benefits Adapter parses the XML response and converts it into application data before passing it to the aggregator.

This keeps XML-specific processing inside the Benefits Adapter.

---

## 7. Graceful Degradation

The Benefits Register may return HTTP 500 errors.

A failure in the Benefits Register should not cause the entire Unified API to fail.

When Benefits Register is unavailable:

```text
Status: partial
```

Resident information is still returned.

The unavailable Benefits data is not fabricated.

---

## 8. Explicit Error Reporting

When an upstream service fails, the Unified API records the failure information.

For example:

```text
Benefits available: False
Benefits error: Benefits Register returned HTTP 500
```

This allows the client to understand that the response is partial.

---

## 9. No Cross-System Identity Matching

The two legacy systems do not provide a common identifier.

Therefore, the project does not automatically claim that a Benefits record belongs to a particular Resident record.

Identity resolution is outside the core integration scope.

---

## 10. Read-Only Integration

The Unified API reads information from the legacy systems.

The project does not modify the underlying Resident Index or Benefits Register data.

---

## 11. Simple Architecture

The project uses a lightweight Python architecture:

```text
Client
  |
  v
Unified API
  |
  +---- Resident Adapter ---- REST Service
  |
  +---- Benefits Adapter ---- XML Service
  |
  v
Aggregator
  |
  v
Unified Response
```

The design keeps the solution simple and focused on integration reliability.

---

## Summary

The main engineering decisions are:

- Unified API
- Adapter Pattern
- Aggregator Pattern
- Pagination handling
- Duplicate removal
- XML parsing
- Graceful degradation
- Explicit error reporting
- Read-only integration
- Separation of concerns
