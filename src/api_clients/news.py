import requests

BASE_URL = "https://newsapi.org/v2/everything"


def get_news(query: str, api_key: str) -> list[dict]:
    response = requests.get(
        BASE_URL,
        params={
            "qInTitle": query,
            "pageSize": 5,
            "sortBy": "publishedAt",
            "language": "en",
            "apiKey": api_key,
        },
        timeout=20,
    )
    response.raise_for_status()
    articles = response.json().get("articles", [])

    return [
        {
            "title": article.get("title"),
            "source": (article.get("source") or {}).get("name"),
            "url": article.get("url"),
            "published_at": article.get("publishedAt"),
        }
        for article in articles
    ]