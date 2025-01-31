import os
import json
import requests
import logging
from dotenv import load_dotenv, find_dotenv

CONFIG = {}
DATA_FILE = "data/user.json"

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

def load_conversation():
    """Retrieve conversation history from a JSON file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.error("Error decoding JSON. Starting fresh.")
    return {"messages": []}

def save_conversation(messages):
    """Save conversation history to a JSON file."""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump({"messages": messages}, f, ensure_ascii=False, indent=4)
    except IOError as e:
        logging.error(f"Error saving conversation: {e}")

def send_ai_response(messages):
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

def main():
    """Main loop for console chat."""
    load_dotenv()
    load_env_variables()
    messages = load_conversation()["messages"]
    print("Welcome to AI Chat! Type 'exit' to quit, 'clear' to delete your chat history.")

    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            break
        if user_input.lower() == 'clear':
            if os.path.exists(DATA_FILE):
                os.remove(path=DATA_FILE)
                print("Chat history has been cleared!")
            else:
                print("Chat history is already empty!")
            continue

        messages.append({"role": "user", "content": user_input})
        ai_reply = send_ai_response(messages)
        messages.append({"role": "assistant", "content": ai_reply})
        save_conversation(messages)
        print(f"AI: {ai_reply}")

if __name__ == "__main__":
    main()
