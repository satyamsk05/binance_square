from apscheduler.schedulers.blocking import BlockingScheduler
from news_fetcher import get_latest_news
from generator import generate_post, generate_post_groq
from poster import post_to_binance
from telegram_notify import notify_success, notify_error, notify_startup, notify_daily_summary
from datetime import datetime

# Track daily stats
stats = {"success": 0, "failed": 0, "total": 0}
post_counter = 0

def run_post():
    global post_counter
    post_counter += 1
    stats["total"] += 1
    
    now = datetime.now().strftime('%H:%M:%S')
    print(f"\n{'='*40}")
    print(f"🕐 Running post #{post_counter} at {now}")
    print(f"{'='*40}")

    # Step 1: News fetch
    print("📰 Fetching latest news...")
    news = get_latest_news()
    if not news:
        msg = "NewsAPI returned no results"
        print(f"❌ {msg}")
        notify_error(msg, post_counter)
        stats["failed"] += 1
        return

    print(f"✅ Got: {news['title'][:60]}...")

    # Step 2: Generate (Gemini → Groq fallback)
    print("🤖 Generating with Gemini...")
    post = generate_post(news)

    if not post:
        print("⚠️ Gemini failed, trying Groq...")
        post = generate_post_groq(news)

    if not post:
        msg = "Both Gemini and Groq failed"
        print(f"❌ {msg}")
        notify_error(msg, post_counter)
        stats["failed"] += 1
        return

    print(f"\n📝 Post:\n{'-'*30}\n{post}\n{'-'*30}")
    print(f"📊 Characters: {len(post)}")

    # Step 3: Post to Binance
    print("📤 Posting to Binance Square...")
    post_id = post_to_binance(post)

    if post_id:
        stats["success"] += 1
        notify_success(post, post_counter, post_id)
    else:
        stats["failed"] += 1
        notify_error("Binance Square API rejected the post", post_counter)

def daily_summary():
    notify_daily_summary(stats["success"], stats["failed"], stats["total"])
    # Reset stats
    stats["success"] = 0
    stats["failed"] = 0
    stats["total"] = 0

from market_fetcher import get_market_data, get_top_gainers, get_top_losers
from generator import generate_post, generate_post_groq, generate_market_post
import time

def run_market_posts():
    """Fetch market data and post 2 separate updates (Gainers and Losers)."""
    global post_counter
    print(f"\n{'='*40}")
    print(f"📊 Running Market Update at {datetime.now().strftime('%H:%M:%S')}")
    print(f"{'='*40}")

    data = get_market_data()
    if not data:
        return

    # Post Gainers
    post_counter += 1
    stats["total"] += 1
    gainers = get_top_gainers(data)
    print("📈 Generating Gainers Post...")
    g_post = generate_market_post(gainers, "gainer")
    if g_post:
        print(f"📤 Posting Gainers to Binance Square...")
        g_id = post_to_binance(g_post)
        if g_id:
            stats["success"] += 1
            notify_success(g_post, post_counter, g_id)
        else:
            stats["failed"] += 1
            notify_error("Gainer post rejected", post_counter)
            
        print(f"⏳ Waiting 120s (2 min) before losers post...")
        time.sleep(120) 

    # Post Losers
    post_counter += 1
    stats["total"] += 1
    losers = get_top_losers(data)
    print("📉 Generating Losers Post...")
    l_post = generate_market_post(losers, "loser")
    if l_post:
        print(f"📤 Posting Losers to Binance Square...")
        l_id = post_to_binance(l_post)
        if l_id:
            stats["success"] += 1
            notify_success(l_post, post_counter, l_id)
        else:
            stats["failed"] += 1
            notify_error("Loser post rejected", post_counter)

# Scheduler setup (IST timezone)
scheduler = BlockingScheduler(timezone="Asia/Kolkata")

# News every 4 hours
scheduler.add_job(run_post, 'interval', hours=4, id='news_update')

# Market every 6 hours
scheduler.add_job(run_market_posts, 'interval', hours=6, id='market_update')

# Daily summary at 11:00 PM
scheduler.add_job(daily_summary, 'cron', hour=23, minute=0, id='summary')

if __name__ == "__main__":
    print("🚀 Binance Square Combined Bot Started!")
    print("📅 News: Every 4 Hours | Market: Every 6 Hours")
    
    # Optional: Run immediately on startup for testing
    # run_post()
    # run_market_posts()

    scheduler.start()
