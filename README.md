# Binance Square Combined Bot v3.0 🚀

A high-performance, automated bot for Binance Square that combines real-time news reporting with detailed market data analysis (Top Gainers and Losers).

## 🌟 Features

- **Breaking News Bot**: Automatically fetches high-impact crypto news and generates emoji-rich posts using **Gemini 2.5 Flash**.
- **Market Data Bot**: Finds the Top 3 Gainers and Top 3 Losers from Binance and creates separate, professional analysis posts.
- **Smart Scheduling**: 
  - 📰 News updates every **4 hours**.
  - 📊 Market reports every **6 hours**.
- **Telegram Notifications**: Get real-time updates and direct links to your Binance Square posts.
- **Advanced AI**: Uses the latest Gemini 2.5 Flash model for professional analysis.

## 🛠️ Required API Keys

You will need the following keys in your `.env` file:
- `NEWS_API_KEY`: From [newsapi.org](https://newsapi.org/)
- `GEMINI_API_KEY`: From [Google AI Studio](https://aistudio.google.com/)
- `GROQ_API_KEY`: (Optional fallback) From [Groq Console](https://console.groq.com/)
- `BINANCE_API_KEY`: Your Binance Square OpenAPI Key.
- `TELEGRAM_BOT_TOKEN` & `TELEGRAM_CHAT_ID`: For notifications.

## 🚀 Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/satyamsk05/binance_square.git
   cd binance_square
   ```

2. **Setup Virtual Environment & Install dependencies**:
   ```bash
   # Create a virtual environment (if not already done)
   python3 -m venv .venv
   
   # Activate the virtual environment
   source .venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**:
   Create a `.env` file based on the keys mentioned above.

4. **Run the Bot**:
   ```bash
   # Ensure the virtual environment is activated
   source .venv/bin/activate
   
   # Run the bot
   python main.py
   ```

## 📂 Project Structure

- `main.py`: The unified entry point and scheduler.
- `news_fetcher.py`: Handles breaking news data.
- `market_fetcher.py`: Fetches real-time market tickers from Binance.
- `generator.py`: AI-powered post generation logic.
- `poster.py`: Secure Binance Square publishing logic.
- `telegram_notify.py`: Live notification system.

---
*Developed for professional crypto content creators.*
