import requests

def get_market_data():
    """Fetch 24hr ticker data for all USDT pairs with >1M volume."""
    try:
        url = "https://api.binance.com/api/v3/ticker/24hr"
        r = requests.get(url, timeout=15)
        r.raise_for_status()
        data = r.json()
        
        # Filter for USDT pairs with > 1M quote volume
        filtered = [
            t for t in data
            if t["symbol"].endswith("USDT")
            and float(t.get("quoteVolume", 0)) >= 1_000_000
        ]
        return filtered
    except Exception as e:
        print(f"❌ Market data fetch error: {e}")
        return []

def get_top_gainers(data, top_n=3):
    sorted_data = sorted(data, key=lambda x: float(x["priceChangePercent"]), reverse=True)
    return sorted_data[:top_n]

def get_top_losers(data, top_n=3):
    sorted_data = sorted(data, key=lambda x: float(x["priceChangePercent"]))
    return sorted_data[:top_n]
