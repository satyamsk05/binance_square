"""
# Binance Square Auto Poster v1.0
# Run instructions:
# pip install requests
# python auto_poster.py
# For background: nohup python auto_poster.py >> poster.log 2>&1 &
# For EC2/Mac Mini screen: screen -S poster python auto_poster.py
"""

import requests
import json
import random
import time
import logging
from datetime import datetime
import os
from news_fetcher import get_latest_news
from generator import generate_post, generate_post_groq
from dotenv import load_dotenv
from apscheduler.schedulers.blocking import BlockingScheduler
import telegram_notify

# Load environment variables
load_dotenv()

# --- Config Block ---
SQUARE_TOKEN  = os.getenv("BINANCE_API_KEY")
SQUARE_URL    = "https://www.binance.com/bapi/composite/v1/public/pgc/openApi/content/add"
BINANCE_URL   = "https://api.binance.com/api/v3/ticker/24hr"
TOP_N         = 3
WAIT_BETWEEN  = 120   # seconds between posts in a cycle
SLEEP_CYCLE   = 21600 # 6 hours in seconds
MIN_VOLUME    = 500000
LAST_TEMPLATE_FILE = "last_template.json"
STABLECOINS = ["USDC", "BUSD", "TUSD", "FDUSD", "USDT"]

# --- Logging Setup ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s  %(levelname)s  %(message)s',
    handlers=[
        logging.FileHandler("poster.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# --- Template System ---

def load_templates_from_file(filepath, type_str):
    """Loads and parses templates from the txt file, replacing examples with placeholders."""
    if not os.path.exists(filepath):
        logger.error(f"Template file not found: {filepath}")
        return {}

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Split by separator
        blocks = content.split("════════════════════════════════════════════════════")
        templates = {}
        count = 0
        
        # Example tokens/values to find and replace with placeholders
        # Gainers examples
        g_tokens = ["$PEPE", "$WIF", "$BONK"]
        g_changes = ["+34.2%", "+21.7%", "+18.4%"]
        # Losers examples
        l_tokens = ["$LUNA", "$ICP", "$APT"]
        l_changes = ["-28.5%", "-19.3%", "-15.1%"]
        
        date_example = "25 Mar"
        
        for block in blocks:
            # Clean block
            lines = block.split("\n")
            cleaned_lines = []
            started = False
            for line in lines:
                # Skip the header line like "── POST 001 [Style 01] ──"
                if "── POST " in line and "──" in line:
                    started = True
                    continue
                if started:
                    cleaned_lines.append(line)
            
            raw_template = "\n".join(cleaned_lines).strip()
            if not raw_template:
                continue
                
            # Replace logic
            final_template = raw_template
            
            # Replace tokens and changes based on type
            if type_str == "gainer":
                for i in range(3):
                    # Replace tokens (like $PEPE or PEPE in Style 10)
                    final_template = final_template.replace(g_tokens[i], f"{{t{i+1}}}")
                    token_no_sign = g_tokens[i].replace("$", "")
                    final_template = final_template.replace(token_no_sign, f"{{t{i+1}}}")
                    # Replace changes
                    final_template = final_template.replace(g_changes[i], f"{{c{i+1}}}")
            else:
                for i in range(3):
                    # Replace tokens
                    final_template = final_template.replace(l_tokens[i], f"{{t{i+1}}}")
                    token_no_sign = l_tokens[i].replace("$", "")
                    final_template = final_template.replace(token_no_sign, f"{{t{i+1}}}")
                    # Replace changes
                    final_template = final_template.replace(l_changes[i], f"{{c{i+1}}}")
            
            # Replace date
            final_template = final_template.replace(date_example, "{date}")
            
            count += 1
            templates[count] = final_template
            
        logger.info(f"Loaded {len(templates)} templates for {type_str}")
        return templates
    except Exception as e:
        logger.error(f"Error loading {type_str} templates: {str(e)}")
        return {}

# Load templates at startup (Combining Hinglish and English versions)
GAINER_FILES = ["GAINERS_150_posts.txt", "GAINERS_150_english.txt"]
LOSER_FILES  = ["LOSERS_150_posts.txt", "LOSERS_150_english.txt"]

def load_all_templates():
    g_all = {}
    l_all = {}
    
    # Load Gainers
    current_idx = 1
    for f in GAINER_FILES:
        templates = load_templates_from_file(f, "gainer")
        for t in templates.values():
            g_all[current_idx] = t
            current_idx += 1
            
    # Load Losers
    current_idx = 1
    for f in LOSER_FILES:
        templates = load_templates_from_file(f, "loser")
        for t in templates.values():
            l_all[current_idx] = t
            current_idx += 1
            
    return g_all, l_all

GAINER_TEMPLATES, LOSER_TEMPLATES = load_all_templates()

def get_post_content(type_str, tokens, date):
    """Picks a template and replaces placeholders with token data."""
    templates = GAINER_TEMPLATES if type_str == "gainer" else LOSER_TEMPLATES
    if not templates:
        return None
        
    idx = get_next_template(type_str, len(templates))
    template_str = templates[idx]
    
    # Fill data
    try:
        data_map = {"date": date}
        for i in range(len(tokens)):
            data_map[f"t{i+1}"] = tokens[i]['symbol']
            data_map[f"c{i+1}"] = tokens[i]['change']
        
        return template_str.format(**data_map)
    except Exception as e:
        logger.error(f"Error formatting template {idx} for {type_str}: {str(e)}")
        return None

def get_footer():
    return "\n\nDYOR + Not financial advice\n📲 @ogcrypt0"

# Gainer Templates (Hinglish)
# These functions are now obsolete and will be replaced by dynamic loading.
# Keeping them commented out for reference if needed, but they are not used.
# def g1(tokens, date):
#     return f"Aaj market ka mahaul kaafi garam hai! 🔥\nTop Gainers:\n1. {tokens[0]['symbol']} ({tokens[0]['change']})\n2. {tokens[1]['symbol']} ({tokens[1]['change']})\n3. {tokens[2]['symbol']} ({tokens[2]['change']})\nKya aapne inme invest kiya? #Crypto #Profit" + get_footer()
# ... (all gainer templates g1-g20) ...

# Loser Templates (Hinglish)
# These functions are now obsolete and will be replaced by dynamic loading.
# Keeping them commented out for reference if needed, but they are not used.
# def l1(tokens, date):
#     return f"Market me thoda dar ka mahol hai. 📉\nTop Losers:\n1. {tokens[0]['symbol']} ({tokens[0]['change']})\n2. {tokens[1]['symbol']} ({tokens[1]['change']})\n3. {tokens[2]['symbol']} ({tokens[2]['change']})\nHold tight! #MarketDip #Crypto" + get_footer()
# ... (all loser templates l1-l20) ...

# GAINER_TEMPLATES = {i+1: func for i, func in enumerate([g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17, g18, g19, g20])}
# LOSER_TEMPLATES  = {i+1: func for i, func in enumerate([l1, l2, l3, l4, l5, l6, l7, l8, l9, l10, l11, l12, l13, l14, l15, l16, l17, l18, l19, l20])}

# --- Core Functions ---

def fetch_tokens():
    try:
        response = requests.get(BINANCE_URL, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        filtered = []
        for x in data:
            symbol = x['symbol']
            # Only USDT pairs
            if not symbol.endswith("USDT"):
                continue
            
            # Exclude stablecoins
            base_coin = symbol.replace("USDT", "")
            if base_coin in STABLECOINS:
                continue
                
            # Min volume $500k
            try:
                vol = float(x['quoteVolume'])
                if vol < MIN_VOLUME:
                    continue
            except:
                continue
                
            filtered.append({
                "symbol": base_coin,
                "change": float(x['priceChangePercent']),
                "change_str": f"{x['priceChangePercent']}%"
            })
            
        if not filtered:
            return None, None
            
        # Sort by change
        sorted_tokens = sorted(filtered, key=lambda x: x['change'], reverse=True)
        
        top_gainers = sorted_tokens[:TOP_N]
        top_losers = sorted_tokens[-TOP_N:]
        
        # Format for templates
        gainers_formatted = [{"symbol": x['symbol'], "change": ("+" if x['change'] > 0 else "") + x['change_str']} for x in top_gainers]
        losers_formatted = [{"symbol": x['symbol'], "change": x['change_str']} for x in reversed(top_losers)] # reversed so biggest loser is first
        
        return gainers_formatted, losers_formatted

    except Exception as e:
        logger.error(f"Binance API Error: {str(e)}")
        return None, None

def post_to_square(content):
    headers = {
        "X-Square-OpenAPI-Key": SQUARE_TOKEN,
        "Content-Type": "application/json",
        "clienttype": "binanceSkill",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }
    payload = {
        "bodyTextOnly": content
    }
    
    logger.info(f"Sending post content:\n{content}")
    
    try:
        response = requests.post(SQUARE_URL, headers=headers, json=payload, timeout=15)
        
        # Check success
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("code") == "000000" or data.get("success") == True:
                    logger.info("Posted successfully")
                else:
                    logger.error(f"Binance Square API Error: {data.get('code')} | {data.get('message')}")
            except:
                logger.info("Posted successfully (Non-JSON response but 200 OK)")
        else:
            logger.error(f"Square post failed! Status: {response.status_code}")
            logger.error(f"Response: {response.text}")
    except Exception as e:
        logger.error(f"Request error while posting: {str(e)}")

def get_next_template(type_str, num_templates):
    # Load last used
    last_indices = {"gainer": -1, "loser": -1}
    if os.path.exists(LAST_TEMPLATE_FILE):
        try:
            with open(LAST_TEMPLATE_FILE, "r") as f:
                last_indices = json.load(f)
        except:
            pass
            
    last_idx = last_indices.get(type_str, -1)
    
    # Pick new random index (1 to num_templates) that isn't the last one
    template_ids = list(range(1, num_templates + 1))
    if last_idx in template_ids and len(template_ids) > 1:
        template_ids.remove(last_idx)
    
    new_idx = random.choice(template_ids)
    
    # Update and save
    last_indices[type_str] = new_idx
    with open(LAST_TEMPLATE_FILE, "w") as f:
        json.dump(last_indices, f)
        
    return new_idx

# --- Jobs for Scheduler ---

def post_news_job():
    """Job to fetch news and post to Square."""
    try:
        logger.info("📰 Job Started: News Post")
        news_data = get_latest_news()
        
        if news_data:
            logger.info(f"🤖 Generating News post for: {news_data['title'][:50]}...")
            # Prioritize Groq
            news_post = generate_post_groq(news_data)
            if not news_post:
                logger.info("⚠️ Groq failed, trying Gemini fallback...")
                news_post = generate_post(news_data)
            
            if news_post:
                post_to_square(news_post)
                telegram_notify.notify_success(news_post, "News")
            else:
                logger.error("Failed to generate news post content.")
        else:
            logger.warning("No news found, skipping news post.")
            
    except Exception as e:
        logger.error(f"Error in post_news_job: {str(e)}")

def post_market_job():
    """Job to fetch market data and post to Square."""
    try:
        logger.info("📊 Job Started: Market Update")
        now_str = datetime.now().strftime('%d %b')
        
        # Step 1: Fetch Data
        gainers, losers = fetch_tokens()
        if not gainers or not losers:
            logger.warning("No tokens fetched or Binance API failed. Retrying in 60s...")
            time.sleep(60)
            gainers, losers = fetch_tokens()
            if not gainers or not losers:
                logger.error("Retry failed. Skipping this cycle.")
                return

        # Step 2: Post Gainer
        g_content = get_post_content("gainer", gainers, now_str)
        if g_content:
            post_to_square(g_content)
            telegram_notify.notify_success(g_content, "Gainer Update")
        
        logger.info(f"Waiting {WAIT_BETWEEN}s before loser post...")
        time.sleep(WAIT_BETWEEN)
        
        # Step 3: Post Loser
        l_content = get_post_content("loser", losers, now_str)
        if l_content:
            post_to_square(l_content)
            telegram_notify.notify_success(l_content, "Loser Update")
            
    except Exception as e:
        logger.error(f"Error in post_market_job: {str(e)}")

def main():
    logger.info("🚀 Auto Poster Script Started with APScheduler!")
    
    # Verify templates loaded
    if not GAINER_TEMPLATES or not LOSER_TEMPLATES:
        logger.error("Failed to load templates. Check txt files. Exiting.")
        return

    # Notify Startup
    telegram_notify.notify_startup()

    # Initial Run
    logger.info("Checking news and market data for initial run...")
    post_news_job()
    post_market_job()

    # Setup Scheduler
    scheduler = BlockingScheduler()
    
    # News Job: Every 3 hours
    scheduler.add_job(post_news_job, 'interval', hours=3, id='news_job')
    
    # Market Job: Every 6 hours
    scheduler.add_job(post_market_job, 'interval', hours=6, id='market_job')

    logger.info("Next news post in 3 hours. Next market update in 6 hours.")
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped by user.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Script stopped by user. Bye!")
        logger.info("Script stopped by user (KeyboardInterrupt)")
