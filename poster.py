import requests
import os
from dotenv import load_dotenv
load_dotenv()

def post_to_binance(content):
    headers = {
        "X-Square-OpenAPI-Key": os.getenv("BINANCE_API_KEY"),
        "Content-Type": "application/json",
        "clienttype": "binanceSkill"
    }
    payload = {
        "bodyTextOnly": content
    }
    url = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"
    try:
        r = requests.post(url, json=payload, headers=headers, timeout=15)
        try:
            data = r.json()
            # Success code for this API is usually "000000"
            if r.status_code == 200 and data.get("code") == "000000":
                print("✅ Posted to Binance Square!")
                return data.get("data", {}).get("id")
            else:
                print(f"❌ Binance error: {data.get('code')} | {data.get('message')}")
                return False
        except ValueError:
            print(f"❌ JSON parse error mapping response: {r.status_code}")
            print(f"📄 Response body: {r.text[:500]}") # Print first 500 chars of response
            return False
    except Exception as e:
        print(f"❌ Post error: {e}")
        return False
