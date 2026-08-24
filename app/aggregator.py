def build_unified_view(
    residents,
    benefits_result,
    resident_available=True,
    resident_error=None
):
    """
    Combine Resident Index and Benefits Register information
    into one unified response.

    A failed source does not make the whole unified API fail.
    The caller receives available data plus explicit source
    availability and error information.

    We do not perform identity matching because the two
    source systems have no shared key.
    """

    benefits_available = benefits_result.get("available", False)
    benefits_records = benefits_result.get("records", [])
    benefits_error = benefits_result.get("error")

    # Complete only when BOTH sources are available.
    if resident_available and benefits_available:
        status = "complete"
    else:
        status = "partial"

    return {
        "status": status,

        "resident_index": {
            "available": resident_available,
            "record_count": len(residents),
            "records": residents,
            "error": resident_error
        },

        "benefits_register": {
            "available": benefits_available,
            "record_count": len(benefits_records),
            "records": benefits_records,
            "error": benefits_error
        }
    }