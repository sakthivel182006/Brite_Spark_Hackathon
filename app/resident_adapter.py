import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


BASE_URL = "http://127.0.0.1:8081"


def get_all_residents():
    residents = {}
    page = 1

    while True:
        url = f"{BASE_URL}/residents?page={page}&page_size=25"

        try:
            with urlopen(url, timeout=5) as response:
                data = json.loads(response.read().decode("utf-8"))

        except (HTTPError, URLError, TimeoutError) as error:
            raise RuntimeError(
                f"Resident Index unavailable: {error}"
            )

        for resident in data.get("results", []):
            resident_id = resident.get("id")

            if resident_id:
                residents[resident_id] = resident

        if not data.get("has_more", False):
            break

        page += 1

    return list(residents.values())