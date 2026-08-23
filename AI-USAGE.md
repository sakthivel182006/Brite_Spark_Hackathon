# AI Usage

## Brite Spark 2026 — No Wrong Door

### Problem 3 — Unified Resident View API

AI tools were used as a development assistance tool during the implementation of the project.

AI assistance was used to support development, debugging, documentation, and reasoning.

---

## Areas Where AI Assistance Was Used

### 1. Project Structure

AI was used to discuss and review the separation of the project into:

```text
app/
services/
tests/
```

The final project structure was reviewed against the actual implementation.

---

### 2. Architecture

AI was used to reason about the integration architecture involving:

- Unified API
- Resident Adapter
- Benefits Adapter
- Aggregator
- Legacy REST service
- Legacy XML service

The final architecture was implemented and verified by the developer.

---

### 3. Adapter Pattern

AI assistance was used to understand and apply the Adapter Pattern.

The adapters isolate the differences between:

- REST/JSON Resident Index
- XML Benefits Register

The implementation was reviewed against the actual service behaviour.

---

### 4. REST Integration

AI assistance was used during development of the Resident Index integration.

This included reasoning about:

- HTTP requests
- JSON responses
- Pagination
- Multiple pages
- Duplicate records

---

### 5. XML Integration

AI assistance was used to support XML integration with the Benefits Register.

This included:

- XML parsing
- Extracting records
- Converting XML data into application data
- Handling failed upstream responses

---

### 6. Error Handling

AI assistance was used to reason about handling Benefits Register HTTP 500 failures.

The final behaviour is:

```text
Benefits available
        |
        v
     complete
```

or:

```text
Benefits unavailable
        |
        v
      partial
```

Resident information remains available when the Benefits Register fails.

---

### 7. Testing

AI was used to help identify useful integration test scenarios.

Testing focused on:

- Unified API availability
- Resident Index integration
- Benefits Register integration
- Pagination
- Duplicate handling
- XML processing
- HTTP 500 handling
- Complete responses
- Partial responses

The tests were executed against the running application.

---

### 8. Debugging

AI assistance was used to help analyze development issues and suggest possible fixes.

Suggestions were checked against the actual project behaviour before being used.

---

### 9. Documentation

AI assistance was used to help organize:

- README documentation
- Architecture explanation
- Technology stack
- Project structure
- Engineering decisions
- API usage
- Testing instructions

---

## Developer Verification

AI-generated suggestions were not treated as automatically correct.

The developer:

- Reviewed the suggestions
- Modified code where required
- Ran the application
- Tested the APIs
- Verified responses
- Checked error-handling behaviour
- Confirmed the final implementation

---

## AI Role

AI was used as a development assistant, not as a replacement for developer responsibility.

The developer remained responsible for:

- Final implementation
- Code decisions
- Testing
- Debugging
- Verification
- Project submission

---

## Summary

AI assistance supported the development process through:

- Architecture reasoning
- Coding guidance
- Debugging
- Testing ideas
- Error-handling guidance
- Documentation

The final implementation was reviewed and verified by the developer.
