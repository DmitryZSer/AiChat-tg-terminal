# AI ChatBot 🤖

A dual-interface chatbot powered by **AI**, offering both **console-based** and **Telegram-integrated** interactions. Built with Python and designed for seamless integration with AI APIs such as **ChatGPT**, **DeepSeek**, **Mistral**, **Qwen**, and more.

![Python Version](https://img.shields.io/badge/Python-3.10%2B-brightgreen)

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Configuration](#configuration-)
- [Usage](#usage-)
- [Examples](#examples)
- [Dependencies](#dependencies--addition)
- [Contributing](#contributing-)

# Features
- **Terminal Chat**: Command-line interface for local AI interactions
- **Telegram Bot**: Cloud-ready chatbot with message history management
- **Shared Core**: Common environment configuration and AI integration
- **Persistent Memory**: JSON-based conversation history for both interfaces

# Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-chatbot-project.git
   cd ai-chatbot-project
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate  # Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

# Configuration 🔧

### Environment Setup
The `load_env_variables()` function handles configuration automatically:

1. **Checks for .env file**: Creates one if missing
2. **Validates variables**: Ensures required credentials are present
3. **Interactive setup**: Prompts for missing values during first run

Required environment variables:
```ini
AI_API_KEY=your_ai_service_api_key
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
API_URL=your_api_url
AI_MODEL=your_ai_model
```

The `load_env_variables` function is a crucial component for setting up and validating the environment variables required for your application. [Here's a detailed and elegant description of its functionality](#function-load_env_variables).


# Usage 🚀

### Terminal Chat
```bash
python ai_terminal_chatbot.py
```
- **Type messages** directly in the console
- `clear`: Wipes conversation history
- `exit`: Quits the program

### Telegram Bot
```bash
python ai_tg_chatbot.py
```
- **Start chat**: Send `/start` to your bot
- **Clear history**: Use `/clear` command
- **Persistent context**: Maintains separate histories per user

### Conversation History 💾
Both versions store conversations in JSON format:
- Terminal: `data/user.json`
- Telegram: `data/{user_id}.json`

# Examples
### Terminal chatting:
![Terminal chatting](https://github.com/user-attachments/assets/ccbda57d-3d25-4e28-9105-97c29b74427b)
### Terminal chat history:
![Chat history](https://github.com/user-attachments/assets/72bdb44e-ce76-4e30-aba0-ae55e2ecf9f9)
### Telegram chatting:
![Telegram chatting](https://github.com/user-attachments/assets/266ee309-6c17-4d4c-8607-cd1c68b32cf3)
### Telegram chat history:
![Telegram chat history](https://github.com/user-attachments/assets/99a4671a-9dcc-455e-9ea4-8e7b879100e9)
### Data Structure Example:
![Data Structure Example](https://github.com/user-attachments/assets/3b577acd-e3e6-4ad7-8488-ee084aa8735e)


# Dependencies & addition📦
Package | Version
---|---
requests | 2.32.3
python-dotenv | 1.0.1
aiogram | 3.17.0

---

### Function: `load_env_variables`

#### Purpose
The `load_env_variables` function is designed to ensure that all necessary environment variables are loaded and validated before the application starts. This function plays a pivotal role in configuring the application by managing essential settings such as API keys, tokens, and URLs.

#### Key Features

1. **Environment File Management**:
   - The function begins by checking for the presence of a `.env` file. If the file is not found, it creates one to store the environment variables.

2. **Loading Environment Variables**:
   - It utilizes the `load_dotenv` function to load the environment variables from the `.env` file into the application's environment.

3. **Interactive Variable Setup**:
   - The function defines a list of required environment variables: `AI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `API_URL`, and `AI_MODEL`.
   - It iterates through this list and checks if each variable is set in the environment. If a variable is missing, the function prompts the user to enter the value interactively and writes it to the `.env` file.

4. **Validation**:
   - After ensuring all variables are set, the function validates them by checking their presence in the environment. If any variable is still missing, it raises an `EnvironmentError`.

5. **Configuration Storage**:
   - The validated environment variables are stored in a temporary configuration dictionary, which is then assigned to the global `CONFIG` variable for use throughout the application.

#### Usage
This function should be called at the start of applications to ensure that all required environment variables are properly set up and validated. This setup is essential for the smooth operation of your application, especially when dealing with external APIs and services.

---

## Contributing 🤝
Contributions welcome! Please fork the repository and submit pull requests for:
- Error handling improvements
- Additional platform integrations
- Enhanced configuration options

---

**Note**: Ensure proper API credentials and review rate limits before deployment.
🔐 *Always keep your .env file private!*
