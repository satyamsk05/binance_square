# Binance Square Auto Poster v4.0 🚀

A high-performance, automated bot for Binance Square that combines real-time news reporting with dynamic market analysis using Hinglish templates and dual-AI fallback.

## 🌟 Features

- **Dual-AI Content Engine**: Uses **Groq (Llama-3)** for lightning-fast generation, with **Gemini 2.5 Flash** as a robust fallback.
- **Hinglish Template System**: Supports over 300+ viral templates in Hinglish for maximum engagement with the Indian/Global crypto community.
- **Smart Scheduling (APScheduler)**: 
  - 📰 **News Updates**: Every **3 hours**.
  - 📊 **Market Reports**: Every **6 hours** (Top 3 Gainers & Losers).
- **Telegram Notifications**: Real-time alerts for script startup and successful posts.
- **Robust Execution**: Includes automatic retry logic, API timeouts, and graceful exit handling.

## 🛠️ Required API Keys

Create a `.env` file with these keys:
- `NEWS_API_KEY`: From [newsapi.org](https://newsapi.org/)
- `GROQ_API_KEY`: Primary AI from [Groq Console](https://console.groq.com/)
- `GEMINI_API_KEY`: Fallback AI from [Google AI Studio](https://aistudio.google.com/)
- `BINANCE_API_KEY`: Your Binance Square OpenAPI Key.
- `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: For notifications.

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/satyamsk05/binance_square.git
   cd binance_square
   ```

2. **Setup Virtual Environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the Bot**:
   ```bash
   ./run_poster.sh
   ```

## 📂 Project Structure

- `auto_poster.py`: The main entry point and scheduler.
- `news_fetcher.py`: Fetches and filters latest crypto news.
- `generator.py`: Groq/Gemini generation logic with timeouts.
- `telegram_notify.py`: Live notification system.
- `GAINERS_150_*.txt`: Hinglish and English gainer templates.
- `LOSERS_150_*.txt`: Hinglish and English loser templates.

---
*Optimized for speed, reliability, and engagement.*
