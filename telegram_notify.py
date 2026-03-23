import requests
import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send(message):
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": CHAT_ID,
            "text": message,
            "parse_mode": "HTML"
        }
        r = requests.post(url, json=payload, timeout=10)
        return r.status_code == 200
    except Exception as e:
        print(f"❌ Telegram error: {e}")
        return False

def notify_success(post_text, post_num, post_id=None):
    link_html = f'\n\n🔗 <a href="https://www.binance.com/square/post/{post_id}">View on Binance Square</a>' if post_id else ""
    msg = f"""✅ <b>Post #{post_num} Published!</b>

📤 <b>Binance Square pe live hai:</b>
<i>{post_text[:200]}...</i>{link_html}

🕐 Time: {__import__('datetime').datetime.now().strftime('%d %b %Y, %I:%M %p')}"""
    send(msg)

def notify_error(reason, post_num):
    msg = f"""❌ <b>Post #{post_num} FAILED!</b>

🔴 Reason: {reason}
🕐 Time: {__import__('datetime').datetime.now().strftime('%d %b %Y, %I:%M %p')}

⚠️ Check EC2 logs!"""
    send(msg)

def notify_startup():
    msg = f"""🚀 <b>News Bot Started!</b>

📅 Schedule (IST):
» 6:00 AM  - Morning update
» 9:30 AM  - Pre-market
» 12:00 PM - Midday recap
» 2:30 PM  - Breaking news
» 5:00 PM  - Market close
» 7:30 PM  - Evening analysis
» 10:00 PM - Night wrap

🧪 Test post running now..."""
    send(msg)

def notify_daily_summary(success, failed, total):
    msg = f"""📊 <b>Daily Summary</b>

✅ Successful posts: {success}/{total}
❌ Failed posts:     {failed}/{total}

📅 Date: {__import__('datetime').datetime.now().strftime('%d %b %Y')}
🔄 Bot running fine — next posts tomorrow!"""
    send(msg)
