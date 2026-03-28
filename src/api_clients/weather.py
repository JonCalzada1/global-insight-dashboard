import requests

GEOCODE_URL = "https://geocoding-api.open-meteo.com/v1/search"
FORECAST_URL = "https://api.open-meteo.com/v1/forecast"


def geocode_location(query: str) -> dict | None:
    response = requests.get(
        GEOCODE_URL,
        params={
            "name": query,
            "count": 1,
            "language": "en",
            "format": "json",
        },
        timeout=20,
    )
    response.raise_for_status()
    results = response.json().get("results", [])

    if not results:
        return None

    top = results[0]
    return {
        "name": top.get("name"),
        "country": top.get("country"),
        "latitude": top.get("latitude"),
        "longitude": top.get("longitude"),
    }


def get_current_weather(lat: float, lon: float) -> dict:
    response = requests.get(
        FORECAST_URL,
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,weather_code",
            "timezone": "auto",
        },
        timeout=20,
    )
    response.raise_for_status()
    current = response.json().get("current", {})

    return {
        "temperature": current.get("temperature_2m"),
        "wind_speed": current.get("wind_speed_10m"),
        "weather_code": current.get("weather_code"),
        "time": current.get("time"),
    }