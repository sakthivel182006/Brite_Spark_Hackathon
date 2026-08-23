from app.resident_adapter import get_all_residents
from app.benefits_adapter import get_all_benefits
from app.aggregator import build_unified_view


residents = get_all_residents()

benefits = get_all_benefits()

result = build_unified_view(
    residents,
    benefits
)

print("================================")
print("UNIFIED VIEW")
print("================================")

print("Overall status:", result["status"])

print(
    "Residents:",
    result["resident_index"]["record_count"]
)

print(
    "Benefits:",
    result["benefits_register"]["record_count"]
)

print(
    "Benefits available:",
    result["benefits_register"]["available"]
)

print(
    "Benefits error:",
    result["benefits_register"]["error"]
)