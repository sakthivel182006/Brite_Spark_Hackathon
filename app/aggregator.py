def build_unified_view(residents, benefits_result):
    """
    Combine Resident Index and Benefits Register information
    into one unified response.

    We do not perform identity matching because the two
    source systems have no shared key.
    """

    benefits_available = benefits_result.get("available", False)
    benefits_records = benefits_result.get("records", [])
    benefits_error = benefits_result.get("error")

    result = {
        "status": "complete" if benefits_available else "partial",

        "resident_index": {
            "available": True,
            "record_count": len(residents),
            "records": residents
        },

        "benefits_register": {
            "available": benefits_available,
            "record_count": len(benefits_records),
            "records": benefits_records,
            "error": benefits_error
        }
    }

    return result