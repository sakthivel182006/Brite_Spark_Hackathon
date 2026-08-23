

And replace **`AI-USAGE.md`** with:

```markdown
# AI Usage — Brite Spark 2026

## Problem 3 — No Wrong Door

AI assistance was used during development as a development support tool.

The developer remained responsible for the final architecture, implementation, testing, debugging, and submission.

---

## Areas Where AI Assistance Was Used

### Architecture

AI was used to discuss and reason about:

- Separating the Resident Index and Benefits Register into independent adapters.
- Using an aggregation layer to combine source responses.
- Designing graceful degradation when one source is unavailable.
- Structuring the project into application, service, and test components.

---

### Development Assistance

AI assistance was used for:

- Python code scaffolding.
- REST integration guidance.
- XML parsing guidance.
- Error-handling approaches.
- Pagination handling.
- Duplicate-record handling.
- API structure and response design.
- Test ideas and debugging.

---

### Debugging

AI assistance was used to understand and resolve development issues including:

- Python package/import errors.
- Running tests with Python module syntax.
- Testing the Resident Index service.
- Testing the Benefits Register service.
- Handling intermittent HTTP 500 responses.
- Verifying the unified API response.

---

### Documentation

AI assistance was used to help prepare:

- `README.md`
- `DECISIONS.md`
- Project architecture explanations.
- Setup and testing instructions.

---

## Verification

AI-generated suggestions were not treated as automatically correct.

The implementation was run locally against the provided mock services.

The following behaviors were tested:

- Resident Index retrieval.
- Resident pagination.
- Duplicate resident handling.
- Benefits Register XML retrieval.
- Benefits Register HTTP 500 failure.
- Unified API response.
- Complete response when both sources are available.
- Partial response when the Benefits Register is unavailable.

---

## Human Responsibility

The developer is responsible for:

- Understanding the submitted solution.
- Reviewing generated code.
- Running and validating the application.
- Testing the integration.
- Making final engineering decisions.
- Ensuring the submission follows the Brite Spark rules.

AI assistance does not replace developer review or testing.

---

## Summary

AI was used as a development assistant for reasoning, implementation support, debugging, testing ideas, and documentation.

The final solution was reviewed and tested by the developer before submission.
