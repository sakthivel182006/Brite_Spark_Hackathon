# AI Usage — Brite Spark 2026

## Problem 3 — No Wrong Door

AI assistance was used during development as a development support and reasoning tool.

The final architecture, implementation, integration, testing, debugging, and submission decisions were made and verified by the developer.

AI was not treated as the source of truth. Suggestions were reviewed, adapted where necessary, implemented, and tested against the provided legacy services.

---

## 1. Architecture and Design

AI was used to discuss possible approaches for building the Unified Resident View API.

The main areas discussed were:

* Separating the Resident Index and Benefits Register into independent adapters.
* Using an aggregation layer to combine responses from both legacy systems.
* Keeping legacy-service-specific logic outside the API layer.
* Handling REST/JSON and XML services independently.
* Designing the unified response so that partial source failures do not make the entire API unusable.

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
```

The architecture was reviewed and implemented by the developer.

---

## 2. Implementation Assistance

AI was used for development guidance and code-level suggestions for areas such as:

* Python HTTP request handling.
* REST and XML response processing.
* XML parsing.
* Pagination handling.
* Duplicate resident removal.
* Error handling for unavailable upstream services.
* Structuring adapters and the aggregation layer.
* API response modelling.
* Writing integration-test scenarios.

AI suggestions were not copied blindly. The implementation was adjusted to match the actual behaviour and constraints of the provided legacy services.

---

## 3. Debugging

AI was also used as a debugging assistant.

Examples of problems discussed included:

* HTTP 500 responses from the Benefits Register.
* XML parsing behaviour.
* Pagination and duplicate records.
* Handling an unavailable upstream service.
* Integration-test failures.
* Differences between complete and partial responses.

The developer reproduced the problems locally, applied appropriate fixes, and verified the results by running the services and tests.

---

## 4. Testing

AI was used to suggest test scenarios and edge cases.

The developer implemented and executed tests against the actual application.

Testing covered scenarios including:

* Both upstream services available.
* Resident Index available while Benefits Register is unavailable.
* Successful XML parsing.
* Pagination from the Resident Index.
* Duplicate removal.
* HTTP 500 handling.
* Complete unified responses.
* Partial unified responses.

Observed integration behaviour included:

* Complete response when both services are available.
* Partial response when the Benefits Register is unavailable.
* Resident Index pagination resulting in the expected unique resident set.

---

## 5. AI-Assisted Decisions vs Developer Decisions

AI was primarily used for:

* Brainstorming.
* Architecture discussion.
* Code suggestions.
* Debugging assistance.
* Test-case suggestions.

The developer made the final decisions regarding:

* Project structure.
* Adapter separation.
* Aggregation behaviour.
* Error/degradation behaviour.
* API response structure.
* Which suggestions to accept or reject.
* Final implementation.
* Testing and verification.

---

## 6. Verification of AI-Assisted Work

AI-generated suggestions were considered provisional until verified against the actual project.

Verification was performed by:

1. Running the provided legacy services.
2. Starting the Unified API.
3. Calling the API endpoints.
4. Testing both successful and failure scenarios.
5. Running integration tests.
6. Inspecting returned JSON responses.
7. Confirming that the implementation matched the problem requirements.

The final repository therefore represents the developer's tested implementation rather than unverified AI-generated code.

---

## 7. Developer Responsibility

The developer remains responsible for the final:

* Architecture
* Source code
* Error handling
* Degradation behaviour
* Tests
* Documentation
* Repository structure
* Submission

AI assistance does not replace developer review or verification.

---

## 8. Summary

AI was used as a development assistant throughout the project, primarily for reasoning, architecture discussion, implementation guidance, debugging, and test ideas.

The final solution was implemented, tested, and verified by the developer against the provided Brite Spark legacy services.
