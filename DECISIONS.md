# Engineering Decisions

## Brite Spark 2026 — No Wrong Door

### Problem 3 — Unified Resident View API

This document records the main engineering decisions made for the Unified Resident View API, including what was chosen, what was rejected, the degradation policy, and what would be improved next.

---

## 1. Unified API

We chose to expose a single endpoint:

```text
GET /unified
```

The purpose is to hide the complexity of the two legacy systems from the caller.

The caller should not need to know whether the underlying source uses REST/JSON or XML.

---

## 2. Independent Source Adapters

We chose separate adapters for each legacy system.

### Resident Adapter

```text
app/resident_adapter.py
```

Responsible for:

- Calling the Resident Index REST service
- Handling pagination
- Collecting resident records
- Removing duplicate records

### Benefits Adapter

```text
app/benefits_adapter.py
```

Responsible for:

- Calling the Benefits Register XML service
- Parsing XML
- Handling upstream failures
- Returning available Benefits records

Keeping these adapters independent makes the solution easier to change if the behaviour of one source changes on Day 2.

---

## 3. Aggregator

We chose an aggregation layer:

```text
app/aggregator.py
```

The aggregator combines the results from the two independent adapters.

```text
Resident Adapter ----                       >---- Aggregator ----> Unified Response
Benefits Adapter ----/
```

The aggregator does not need to know the details of REST pagination or XML parsing.

---

## 4. Pagination

The Resident Index is paginated.

We chose to retrieve the available pages instead of assuming that the first page contains all residents.

This ensures that the Unified API can process the complete Resident Index dataset.

---

## 5. Duplicate Handling

The Resident Index may return the same source record on more than one page.

We use the Resident Index resident identifier as the deduplication key.

Therefore, repeated records from the same source are not returned multiple times in the final resident collection.

---

# 6. Graceful Degradation Policy

Partial data is preferred over an error page.

The Unified API does not silently pretend that a failed source returned zero records.

The caller receives the available source data together with explicit information about the failed source.

## Failure Policy

| Source condition | Caller receives | How the caller knows |
|---|---|---|
| Resident Index succeeds | Resident records | Resident source is available |
| Resident Index HTTP/network failure | Other available source data plus Resident failure information | Resident source availability/error fields |
| Benefits Register succeeds | Benefits records | Benefits source is available |
| Benefits Register returns HTTP 500 | Resident data when available; no fabricated Benefits records | `benefits_register.available = false` and `benefits_register.error` |
| Benefits Register timeout/network failure | Resident data when available; no fabricated Benefits records | Benefits source availability/error information |
| Both sources succeed | Data from both sources | `status = complete` |
| One source succeeds and one fails | Data from successful source plus explicit failure information | `status = partial` and source error information |
| Both sources fail | No fabricated data; explicit failure information for both sources | Both source statuses/errors |

The important distinction is:

```text
No records found
```

is different from:

```text
Source unavailable
```

An unavailable source is never silently represented as a successful empty dataset.

---

## 7. Benefits Register HTTP 500

The Benefits Register is intentionally unreliable and can return HTTP 500.

When this happens, the Unified API continues to return Resident information when the Resident Index is available.

Example:

```text
Status: partial
Residents: 620
Benefits: 0
Benefits available: False
Benefits error: Benefits Register returned HTTP 500
```

The caller can therefore identify both:

1. Which source failed.
2. Why the source was unavailable.

---

## 8. Complete and Partial Responses

When both sources are available:

```text
status = complete
```

When at least one source is unavailable:

```text
status = partial
```

The response also exposes source-specific availability and error information so the caller can understand the condition instead of receiving a bare server error.

---

## 9. Retry-Safe and Idempotent Behaviour

The Unified API is read-only.

The API does not create, update, or delete records in either legacy system.

Repeating:

```text
GET /unified
```

does not create write-side effects.

Resident records are also deduplicated using the Resident Index identifier, so repeated records from paginated responses do not become duplicate entries in the unified resident collection.

---

## 10. No Fabricated Data

When an upstream source is unavailable, the application does not invent records or claim that the source successfully returned an empty dataset.

Instead, the source is marked unavailable and the error is exposed to the caller.

This prioritizes correctness and transparency over presenting an apparently complete but misleading response.

---

## 11. No Cross-System Identity Matching

The two legacy systems do not provide a shared identifier.

Therefore, we deliberately do not automatically claim that a Benefits record belongs to a particular Resident record.

Incorrectly merging two different people would be worse than declining to merge them.

Identity resolution is therefore outside the core implementation.

It is considered a possible future enhancement only if a conservative confidence threshold and an uncertain-match policy can be established.

---

## 12. Why We Did Not Add a Database

A database was not chosen because persistence is not required for the core integration problem.

Adding a database would introduce additional deployment and failure complexity without being necessary for the required Unified API.

---

## 13. Why We Did Not Add a Frontend

A frontend was not chosen because the problem evaluates the API and command-line demonstration is sufficient.

The solution focuses development effort on integration reliability rather than interface work.

---

## 14. Caching — Deferred

Caching was not included in the core implementation.

The Benefits Register is slow, so caching could improve response time. However, caching also introduces stale-data behaviour.

We would only add caching after defining:

- A defensible expiry time
- What level of staleness is acceptable
- How cache failures are handled
- How fresh data can be requested when necessary

This was deliberately deferred until the required floor was satisfied.

---

## 15. Circuit Breaking — Deferred

A circuit breaker was not included in the core implementation.

The current solution already handles Benefits Register failures through graceful degradation.

A future circuit breaker could stop repeatedly calling a source that is comprehensively unavailable.

Before adding it, we would define:

- Failure threshold
- Open-circuit duration
- Half-open behaviour
- Recovery behaviour

This was deliberately deferred until the required floor was satisfied.

---

## 16. Day-2 Change Resilience

The architecture intentionally keeps each source adapter independent.

A change to the Resident Index should primarily affect:

```text
app/resident_adapter.py
```

A change to the Benefits Register should primarily affect:

```text
app/benefits_adapter.py
```

REST-specific and XML-specific behaviour is kept outside the aggregation logic.

This means a source-specific Day-2 change can be handled without rewriting the entire Unified API.

---

## 17. What We Rejected

The following approaches were rejected for the core implementation:

### Automatic identity matching

Rejected because there is no shared key and incorrect matching could silently associate the wrong resident.

### Database persistence

Rejected because it is not required for the integration problem.

### Frontend

Rejected because interface quality is not assessed for this problem.

### Caching

Deferred because freshness and expiry policy must be defined before introducing stale data.

### Circuit breaker

Deferred because graceful degradation was prioritized first.

### Authentication and authorization

Not implemented because they are outside the required problem scope.

---

## 18. What We Would Improve First

If additional development time were available, the priority would be:

1. Expand automated timeout and network-failure tests.
2. Add a circuit breaker for repeated Benefits Register failures.
3. Add caching with a documented and defensible expiry policy.
4. Add conservative identity matching with an explicit confidence threshold and uncertain-match policy.
5. Expand integration tests for simultaneous upstream failures.

These improvements would only be added without weakening the existing correctness and degradation guarantees.

---

## 19. Design Priorities

The implementation prioritizes:

1. Correct integration with both legacy systems.
2. Graceful degradation.
3. Explicit source failure information.
4. Pagination correctness.
5. Duplicate prevention.
6. Retry-safe read-only behaviour.
7. Independent source adapters.
8. Simple and maintainable architecture.

---

## 20. Summary

The core design deliberately focuses on reliable integration rather than unnecessary complexity.

The Unified API provides one entry point while preserving clear information about source availability and failures.

When a source is healthy, its data is included.

When a source fails, the available data is still returned and the caller is explicitly told what is missing and why.
