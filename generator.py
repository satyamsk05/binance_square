from google import genai
import os
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def generate_post(news):
    prompt = f"""You are a crypto content writer for Binance Square.

Write an engaging post based on this news:
Title: {news['title']}
Details: {news['description']}

STRICT RULES:
- Max 900 characters total
- Maximum 2 hashtags only
- Use emojis
- Bullet points for key info
- End with a question to engage readers
- English language
- End with "DYOR 🙏"
- Plain text only, no markdown bold or stars

Output only the post text, nothing else."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        post = response.text.strip()
        if len(post) > 1000:
            post = post[:997] + "..."
        return post
    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            print(f"❌ Gemini quota reached: {e}")
        else:
            print(f"❌ Gemini error: {e}")
        return None

def generate_post_groq(news):
    from groq import Groq
    client_groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are a crypto content writer for Binance Square.
Write an engaging post based on this news:
Title: {news['title']}
Details: {news['description']}

STRICT RULES:
- Max 900 characters total
- Maximum 2 hashtags only
- Use emojis, bullet points
- End with a question + "DYOR 🙏"
- Plain text only

Output only the post text."""

    try:
        response = client_groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400
        )
        post = response.choices[0].message.content.strip()
        if len(post) > 1000:
            post = post[:997] + "..."
        return post
    except Exception as e:
        print(f"❌ Groq error: {e}")
        return None

def generate_market_post(tokens, mode="gainer"):
    """Generate a market update post for top gainers or losers."""
    from google import genai
    import os
    from dotenv import load_dotenv
    load_dotenv()
    
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    token_list = "\n".join([
        f"- {t['symbol'].replace('USDT', '')}: {float(t['priceChangePercent']):+.2f}%" 
        for t in tokens
    ])
    
    type_str = "Top Gainers (Bullish)" if mode == "gainer" else "Top Losers (Bearish)"
    
    prompt = f"""You are a professional crypto market analyst for Binance Square.
    Write an engaging market update post for these {type_str}:
    {token_list}

    STRICT RULES:
    - Max 900 characters
    - Use emojis, bullet points
    - Be professional yet exciting
    - Explain WHY these might be moving (general crypto context)
    - End with a question + "DYOR 🙏"
    - Maximum 2 hashtags
    - Plain text only

    Output only the post text."""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        post = response.text.strip()
        return post
    except Exception as e:
        print(f"❌ Market generation error: {e}")
        return None
