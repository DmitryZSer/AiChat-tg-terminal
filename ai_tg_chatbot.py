import os
import asyncio
import logging
import json
import re

import requests
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram.filters import Command

dp = Dispatcher()
CONFIG = []

def load_env_variables():
    """Load and validate required environment variables."""
    global CONFIG
    if not find_dotenv():
        print(".env file not found. It will be created.")

    load_dotenv()
    env_vars = ["AI_API_KEY", "TELEGRAM_BOT_TOKEN", "API_URL", "AI_MODEL"]

    # Ensure all required environment variables are set
    with open(".env", "a") as env_file:
        for var in env_vars:
            if not os.getenv(var):
                value = input(f"Please enter your {var}: ")
                env_file.write(f"{var}={value}\n")
                os.environ[var] = value

    # Validate loaded environment variables
    temp_config = {}
    for var in env_vars:
        value = os.getenv(var)
        if not value:
            raise EnvironmentError(f"Error: {var} environment variable not set.")
        temp_config[var] = value

    CONFIG = temp_config

def load_conversation(user_id):
    """Retrieve conversation history from a JSON file."""
    file_path = os.path.join("data", f"{user_id}.json")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data if isinstance(data, dict) else {"messages": data}
    except FileNotFoundError:
        logging.info(f"No conversation history for user {user_id}. Starting new chat.")
        return {"messages": []}
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding JSON for user {user_id}: {e}")
        return {"messages": []}


def save_conversation(user_id, messages):
    """Save conversation history to a JSON file."""
    file_path = os.path.join("data", f"{user_id}.json")
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump({"messages": messages}, f, ensure_ascii=False, indent=4)
    except IOError as e:
        logging.error(f"Error saving conversation for user {user_id}: {e}")


async def send_ai_response(messages):
    """Send user input to AI API and return the response."""
    global CONFIG
    headers = {
        "Authorization": f"Bearer {CONFIG['AI_API_KEY']}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "model": CONFIG['AI_MODEL'],
        "messages": messages
    }
    try:
        response = requests.post(CONFIG['API_URL'], json=payload, headers=headers)
        response.raise_for_status()
        ai_reply = response.json().get('choices', [{}])[0].get('message', {}).get('content', '')
        if not ai_reply:
            raise ValueError("AI response is empty.")
        return ai_reply
    except requests.RequestException as e:
        logging.error(f"HTTP error during API request: {e}")
        return "An error occurred while processing your request."
    except ValueError as e:
        logging.error(f"Error in AI response: {e}")
        return "Received an invalid response from the AI service."


@dp.message(Command("start"))
async def start_command(message: Message):
    """Handle /start command."""
    user_id = message.from_user.id
    try:
        messages = load_conversation(user_id)["messages"]
        if not messages:
            messages.append({"role": "system", "content": "Hi, You are a helpful assistant!"})
            save_conversation(user_id, messages)
        await message.answer("Welcome to Mistral AI Chat Bot!")
    except Exception as e:
        logging.error(f"Error in /start command: {e}")
        await message.answer("An error occurred while starting the chat bot.")


@dp.message(Command("clear"))
async def clear_command(message: Message):
    """Handle /clear command."""
    user_id = message.from_user.id
    file_path = os.path.join("data", f"{user_id}.json")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            await message.answer("Chat history has been cleared!")
        else:
            await message.answer("Chat history is already empty!")
    except Exception as e:
        logging.error(f"Error clearing chat history for user {user_id}: {e}")
        await message.answer("An error occurred while clearing chat history.")

def split_text(text: str, max_length: int = 4000) -> list[str]:
    """Разбивает текст на части, сохраняя целостность Markdown блоков."""
    return [text[i:i + max_length] for i in range(0, len(text), max_length)]

@dp.message()
async def message_handler(message: Message):
    """Handle incoming user messages."""
    user_input = message.text
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        messages = load_conversation(user_id)["messages"]
        messages.append({"role": "user", "content": user_input})
        logging.info(f"User @{username} ({user_id}) wrote: {user_input}")

        processing_message = await message.reply("⏳ Please wait, processing your request...")
        ai_reply = await send_ai_response(messages)
        messages.append({"role": "assistant", "content": ai_reply})
        save_conversation(user_id, messages)
        await processing_message.delete()

        ai_reply = split_text(ai_reply)

        if(len(ai_reply)>1):
            for i in ai_reply:
                print(i, "\n")
                await message.answer(i, parse_mode="")
            return
        await message.answer(ai_reply[0], parse_mode="Markdown")
    except Exception as e:
        logging.error(f"Error handling message from user {user_id}: {e}")
        await message.answer("An error occurred while processing your message.")


async def main():
    """Start the Telegram bot."""
    load_dotenv()
    load_env_variables()
    logging.basicConfig(level=logging.INFO)
    os.makedirs("data", exist_ok=True)
    bot = Bot(token=CONFIG['TELEGRAM_BOT_TOKEN'])
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
