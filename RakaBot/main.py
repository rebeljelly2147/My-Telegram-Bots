from typing import Final
import time
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os
import requests
from datetime import datetime, timedelta
from os import environ

if environ.get('IS_PROD'):
    TOKEN = environ.get('TELEGRAM_TOKEN')
    HUGGINGFACE_API_KEY = environ.get('HUGGINGFACE_API_KEY')
else:
    load_dotenv()
    TOKEN = os.getenv('TELEGRAM_TOKEN')
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')

BOT_USERNAME: Final = '@noob_raka_bot'

# Initialize HuggingFace API settings
API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"
headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

# Rate limiting class
class RateLimiter:
    def __init__(self, calls_per_minute=60):
        self.calls_per_minute = calls_per_minute
        self.calls = []
    
    def can_make_request(self) -> bool:
        now = datetime.now()
        self.calls = [call for call in self.calls if call > now - timedelta(minutes=1)]
        if len(self.calls) < self.calls_per_minute:
            self.calls.append(now)
            return True
        return False

# Initialize rate limiter
rate_limiter = RateLimiter(calls_per_minute=30)  # Adjust based on your needs

# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! this is Raka 👋. How can I help you?') 

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Raka, a bot created by @noob_raka. I can help you with some basic commands. Here are some commands you can use:\n\n/start - To start the bot\n/help - To get help\n/custom - To get a custom message') 

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom message!') 

# Response Handlers
async def get_huggingface_response(prompt: str) -> str:
    if not rate_limiter.can_make_request():
        return "I'm receiving too many requests right now. Please try again in a minute! 🕒"
    
    try:
        response = requests.post(
            API_URL, 
            headers=headers, 
            json={"inputs": prompt},
            timeout=10  # Add timeout
        )
        if response.status_code == 200:
            return response.json()[0]['generated_text']
        elif response.status_code == 429:
            return "I'm a bit overwhelmed right now. Please try again in a minute! 🔄"
        else:
            print(f"HuggingFace API Error: {response.status_code}")
            return f"I encountered an issue. Please try again later! 🔧"
    except requests.Timeout:
        return "The response took too long. Please try again! ⏱️"
    except Exception as e:
        print(f"Error in HuggingFace response: {str(e)}")
        return "I'm having trouble thinking right now. Let me respond simply! 🤖"

async def handle_response(text: str) -> str:
    processed_text = text.lower()
    
    # Basic responses for common interactions
    greetings = ['hello', 'hi', 'hey', 'sup', 'whatsup']
    goodbyes = ['bye', 'goodbye', 'see you', 'cya']
# Simple patterns continue to use predefined responses
    
# Simple patterns continue to use predefined responses
    if any(word in processed_text for word in greetings):
        return "Hey! How can I help you today? 👋"
    elif any(word in processed_text for word in goodbyes):
        return "Goodbye! Have a great day! 👋"
    
    # For more complex queries, use HuggingFace
    try:
        response = await get_huggingface_response(text)
        return response
    except Exception:
        return "I'm having trouble connecting to my AI brain. Let me respond simply: I'm here to help! 🤖"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type # Get the type of chat the message was sent in (private, group, etc.)
    text: str = update.message.text # Get the text of the message sent by the user
    
    print(f'User ({update.message.chat.id}) in {message_type}: {text}') # for debugging

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text = text.replace(BOT_USERNAME, '', 1).strip()
            response = await handle_response(new_text)
        else:
            return
    else:
        response = await handle_response(text)

    print(f'Bot ({BOT_USERNAME}): {response}') # for debugging
    await update.message.reply_text(response)


# Error Handlers
async def error(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__': # Entry point of the script to start the bot 

    print('Bot is running!')
    # Commands
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polling
    print('Bot is polling!')
    app.run_polling(poll_interval=1) # Polling interval is set to 1 second