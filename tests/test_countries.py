from unittest.mock import Mock, patch

from src.api_clients.countries import get_country_by_name


@patch("src.api_clients.countries.requests.get")
def test_get_country_by_name_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = [
        {
            "name": {
                "common": "Portugal",
                "official": "Portuguese Republic",
            },
            "capital": ["Lisbon"],
            "region": "Europe",
            "subregion": "Southern Europe",
            "population": 10749635,
            "flags": {"png": "https://flagcdn.com/w320/pt.png"},
            "languages": {"por": "Portuguese"},
            "currencies": {"EUR": {"name": "Euro", "symbol": "€"}},
        }
    ]
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_country_by_name("Portugal")

    assert result["name"] == "Portugal"
    assert result["official_name"] == "Portuguese Republic"
    assert result["capital"] == "Lisbon"
    assert result["region"] == "Europe"
    assert result["subregion"] == "Southern Europe"
    assert result["population"] == 10749635
    assert result["flag"] == "https://flagcdn.com/w320/pt.png"
    assert result["languages"] == ["Portuguese"]
    assert result["currencies"] == ["EUR"]