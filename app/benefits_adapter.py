import xml.etree.ElementTree as ET
from urllib.request import urlopen
from urllib.error import HTTPError, URLError


BASE_URL = "http://127.0.0.1:8082"


def get_all_benefits():
    url = f"{BASE_URL}/records"

    try:
        with urlopen(url, timeout=5) as response:
            xml_data = response.read()

        root = ET.fromstring(xml_data)

        benefits = []

        for record in root.findall("Record"):
            benefits.append({
                "ref": record.findtext("Ref"),
                "name": record.findtext("Name"),
                "born": record.findtext("Born"),
                "address": record.findtext("Addr"),
                "town": record.findtext("Town"),
                "benefit_code": record.findtext("BenefitCode"),
                "review_due": record.findtext("ReviewDue")
            })

        return {
            "available": True,
            "records": benefits,
            "error": None
        }

    except HTTPError as error:
        return {
            "available": False,
            "records": [],
            "error": f"Benefits Register returned HTTP {error.code}"
        }

    except (URLError, TimeoutError) as error:
        return {
            "available": False,
            "records": [],
            "error": f"Benefits Register unavailable: {error}"
        }

    except ET.ParseError:
        return {
            "available": False,
            "records": [],
            "error": "Benefits Register returned invalid XML"
        }