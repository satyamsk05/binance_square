import requests
import os
from dotenv import load_dotenv
load_dotenv()

def get_latest_news():
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "bitcoin OR crypto OR binance OR altcoin OR ethereum",
        "sortBy": "publishedAt",
        "pageSize": 5,
        "language": "en",
        "apiKey": os.getenv("NEWS_API_KEY")
    }
    try:
        r = requests.get(url, params=params, timeout=10)
        articles = r.json().get("articles", [])
        if not articles:
            return None
        top = articles[0]
        return {
            "title": top["title"],
            "description": top["description"] or top["title"],
            "source": top["source"]["name"],
            "published": top["publishedAt"]
        }
    except Exception as e:
        print(f"❌ News fetch error: {e}")
        return None
