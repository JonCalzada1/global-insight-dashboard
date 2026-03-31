from unittest.mock import Mock, patch

from src.api_clients.news import get_news


@patch("src.api_clients.news.requests.get")
def test_get_news_success(mock_get):
    mock_response = Mock()
    mock_response.json.return_value = {
        "articles": [
            {
                "title": "Portugal Golden Visa Shows Resilience",
                "source": {"name": "GlobeNewswire"},
                "url": "https://example.com/article1",
                "publishedAt": "2026-03-27T12:00:00Z",
            },
            {
                "title": "Dreamy spa weekend in Portugal",
                "source": {"name": "Holidaypirates.com"},
                "url": "https://example.com/article2",
                "publishedAt": "2026-03-27T11:45:08Z",
            },
        ]
    }
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    result = get_news("Portugal", "fake_api_key")

    assert len(result) == 2
    assert result[0]["title"] == "Portugal Golden Visa Shows Resilience"
    assert result[0]["source"] == "GlobeNewswire"
    assert result[0]["url"] == "https://example.com/article1"
    assert result[0]["published_at"] == "2026-03-27T12:00:00Z"
