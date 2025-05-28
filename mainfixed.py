from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from amazon_price_tracker import price_check
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN: Final = os.getenv("BOT_TOKEN")
USER_NAME: Final = "@News25_bot"
app = Application.builder().token(TOKEN).build()

# Command handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello, Thanks for chatting with me. Please type the Search and price you want to get.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a News bot. Please type something so that this bot can take action.")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("This is a custom command")

# Response function
def handle_response(text: str) -> str:
    processed: str = text.lower()
    if 'hello' in processed:
        return "Hey, How are you??"
    if 'how are you' in processed:
        return "I am good"
    if 'i love python' in processed:
        return "Great!!!"
    return "Couldn't recognize your command"

# Functionality
def handle_price(search: str, price: int) -> list:
    return price_check(search, price)
    


# Message handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    try:
        search, price = text.rsplit(" ", 1)
        price = int(price)
        products = handle_price(search, price)

        if products:
            response = "\n\n".join(
                [f"{p['Name']}\nPrice: ${p['Price']}\nRating: {p['Rating']}\n{p['URL']}" for p in products]
            )
        else:
            response = "No products found under that price."


    except ValueError:
        response = "Please send input like: `search_term price`, e.g., `headphones 50`"
    MAX_MESSAGE_LENGTH = 4000
    if len(response) > MAX_MESSAGE_LENGTH:
        chunks = [response[i:i+MAX_MESSAGE_LENGTH] for i in range(0, len(response), MAX_MESSAGE_LENGTH)]
        for chunk in chunks:
            await update.message.reply_text(chunk)
    else:
        await update.message.reply_text(response)

    await update.message.reply_text(response)


# Error handler
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

# Main function
if __name__ == '__main__':
    print("Starting...")
    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Error handler
    app.add_error_handler(error)

    # Start bot
    print("Polling...")
    app.run_polling(poll_interval=3)
