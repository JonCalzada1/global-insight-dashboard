from unittest.mock import Mock, patch

from src.api_clients.weather import geocode_location, get_current_weather


@patch("src.api_clients.weather.requests.get")
def test_geocode_location_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "results": [
            {
                "name": "Lisbon",
                "country": "Portugal",
                "latitude": 38.71667,
                "longitude": -9.13333,
            }
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = geocode_location("Lisbon")

    assert result["name"] == "Lisbon"
    assert result["country"] == "Portugal"
    assert result["latitude"] == 38.71667
    assert result["longitude"] == -9.13333


@patch("src.api_clients.weather.requests.get")
def test_geocode_location_no_results(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {"results": []}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = geocode_location("UnknownPlace")

    assert result is None


@patch("src.api_clients.weather.requests.get")
def test_get_current_weather_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "current": {
            "temperature_2m": 20.8,
            "wind_speed_10m": 17.1,
            "weather_code": 0,
            "time": "2026-03-28T13:15",
        }
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_current_weather(38.71667, -9.13333)

    assert result["temperature"] == 20.8
    assert result["wind_speed"] == 17.1
    assert result["weather_code"] == 0
    assert result["time"] == "2026-03-28T13:15"