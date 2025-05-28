# 📦 Amazon Price Tracker Telegram Bot

A simple Telegram bot that lets users search for Amazon products by keyword and filter them by maximum price. It uses Selenium to scrape product data from [Amazon.com](https://amazon.com) and replies with matching products and their links.

## 🚀 Features

- ✅ Search Amazon using product keywords.
- 💲 Filter products based on a price threshold.
- 📩 Get product names, prices, and direct URLs.
- 🕵️ Runs headless using Selenium (no browser window).
- 📱 Integrates seamlessly with Telegram.

---

## 🔧 Technologies Used

- **Python 3**
- **Selenium** for web scraping
- **Telegram Bot API** via `python-telegram-bot`
- **dotenv** for secure environment variable handling

---

## 📸 Demo

![Demo Screenshot]https://github.com/Rafin-25/Amazon-Price-Tracker/blob/main/assets/demo-screenshot.png
---

## 💡 Usage

1. Send a message in the format:  
iphone 1000


2. The bot will return a list of matching Amazon products priced below or equal to the given amount.

---

## ⚙️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rafin-25/Amazon-Price-Tracker.git
cd Amazon-Price-Tracker
```
## Install Dependencies
```bash
pip install -r requirements.txt
```

## Set Up Environment Variable
Create a .env file with your Telegram bot token:
BOT_TOKEN=your_telegram_bot_token
Get your bot token from @BotFather on Telegram.



