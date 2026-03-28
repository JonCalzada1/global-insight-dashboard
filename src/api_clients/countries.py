import requests

BASE_URL = "https://restcountries.com/v3.1"

def get_country_by_name(name: str) -> dict:
    url = f"{BASE_URL}/name/{name}"
    params = {'fullText': 'false'}
    response = requests.get(url, params=params, timeout=20)
    response.raise_for_status()
    data = response.json()[0]

    return {
        "name": data.get("name", {}).get("common"),
        "official_name": data.get("name", {}).get("official"),
        "capital": data.get("capital", ["N/A"])[0],
        "region": data.get("region"),
        "subregion": data.get("subregion"),
        "population": data.get("population"),
        "flag": data.get("flags", {}).get("png"),
        "languages": list((data.get("languages") or {}).values()),
        "currencies": list((data.get("currencies") or {}).keys()),
        "area": data.get("area"),
        "borders": data.get("borders", []),
        "cca3": data.get("cca3"),
    }

def get_countries_by_codes(codes: list) -> dict:
    """Get country info by their 3-letter country codes"""
    borders_info = {}
    for code in codes:
        try:
            url = f"{BASE_URL}/alpha/{code}"
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            data = response.json()
            if isinstance(data, list):
                data = data[0]
            borders_info[code] = data.get("name", {}).get("common", code)
        except:
            borders_info[code] = code
    return borders_info