import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


UNIFIED_URL = "http://127.0.0.1:8080/unified"


def get_unified():
    try:
        with urlopen(UNIFIED_URL, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))

    except HTTPError as error:
        raise AssertionError(
            f"Unified API returned HTTP {error.code}"
        )

    except URLError as error:
        raise AssertionError(
            f"Unified API unavailable: {error}"
        )


def test_unified_api():
    data = get_unified()

    assert "status" in data
    assert "resident_index" in data
    assert "benefits_register" in data

    resident = data["resident_index"]
    benefits = data["benefits_register"]

    print("================================")
    print("UNIFIED API TEST")
    print("================================")

    print("Overall status:", data["status"])

    print("Residents:", resident.get("record_count"))
    print("Resident available:", resident.get("available"))
    print("Resident error:", resident.get("error"))

    print("Benefits:", benefits.get("record_count"))
    print("Benefits available:", benefits.get("available"))
    print("Benefits error:", benefits.get("error"))


    if resident.get("available") and benefits.get("available"):

        assert data["status"] == "complete", (
            "Both sources are available, "
            "but status is not 'complete'"
        )

        assert resident["record_count"] == 620, (
            "Expected 620 residents"
        )

        assert benefits["record_count"] == 540, (
            "Expected 540 benefits"
        )


        print()
        print("FINAL RESULT:")
        print("CASE: Both sources available")
        print("RESULT: PASS")
        print("Expected: complete")
        print("Actual:", data["status"])

    elif not resident.get("available") and not benefits.get("available"):

        assert data["status"] == "partial", (
            "Both sources are unavailable, "
            "but status is not 'partial'"
        )

        assert resident["record_count"] == 0, (
            "Resident records should be 0"
        )

        assert benefits["record_count"] == 0, (
            "Benefits records should be 0"
        )

        assert resident.get("error"), (
            "Resident failure must be reported"
        )

        assert benefits.get("error"), (
            "Benefits failure must be reported"
        )

        print()
        print("FINAL RESULT:")
        print("CASE: Both sources unavailable")
        print("RESULT: PASS")
        print("Expected: partial")
        print("Actual:", data["status"])
        

    elif not resident.get("available"):

        assert data["status"] == "partial", (
            "Resident source is unavailable, "
            "but status is not 'partial'"
        )

        assert resident["record_count"] == 0, (
            "Resident records should be 0 when source is unavailable"
        )

        assert resident.get("error"), (
            "Resident failure must be reported"
        )

        print()
        print("FINAL RESULT:")
        print("CASE: Resident unavailable")
        print("RESULT: PASS")
        print("Expected: partial")
        print("Actual:", data["status"])

    elif not benefits.get("available"):

        assert data["status"] == "partial", (
            "Benefits source is unavailable, "
            "but status is not 'partial'"
        )

        assert resident["record_count"] == 620, (
            "Resident data should remain available"
        )

        assert benefits["record_count"] == 0, (
            "Benefits records should be 0 when source is unavailable"
        )

        assert benefits.get("error"), (
            "Benefits failure must be reported"
        )

        print()
        print("FINAL RESULT:")
        print("CASE: Benefits unavailable")
        print("RESULT: PASS")
        print("Expected: partial")
        print("Actual:", data["status"])

    print()
    print("TEST PASSED")


if __name__ == "__main__":
    test_unified_api()