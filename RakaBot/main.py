from typing import Final
import openai
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN: Final = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY: Final = os.getenv('OPENAI_API_KEY')

BOT_USERNAME: Final = '@noob_raka_bot'

# Initialize OpenAI
openai.api_key = OPENAI_API_KEY

# Command Handlers
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello! this is Raka 👋. How can I help you?') 

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am Raka, a bot created by @noob_raka. I can help you with some basic commands. Here are some commands you can use:\n\n/start - To start the bot\n/help - To get help\n/custom - To get a custom message') 

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom message!') 

# Response Handlers
async def get_openai_response(prompt: str) -> str:
    try:
        response = await openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant named Raka."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

async def handle_response(text: str) -> str:
    # Convert input text to lowercase for easier processing
    processed_text = text.lower()
    
    # Basic responses for common interactions
    greetings = ['hello', 'hi', 'hey', 'sup', 'whatsup']
    goodbyes = ['bye', 'goodbye', 'see you', 'cya']
    
    # Simple patterns continue to use predefined responses
    if any(word in processed_text for word in greetings):
        return "Hey! How can I help you today? 👋"
    elif any(word in processed_text for word in goodbyes):
        return "Goodbye! Have a great day! 👋"
    
    # For more complex queries, use OpenAI
    try:
        response = await get_openai_response(text)
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


if __name__ == '__main__':

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