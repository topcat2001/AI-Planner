# AI-Powered Yearly Goal-Setting Telegram Bot

A Telegram bot that helps users develop meaningful yearly goals based on their situation, desires, obligations, identity, strengths, and weaknesses, then stores them in Notion for easy reference and tracking.

## Features

- Comprehensive yearly goal-setting process that considers the whole person
- Interactive conversations to understand user's situation, desires, obligations, identity, strengths, and weaknesses
- AI-powered goal development with OpenAI's GPT-4
- Seamless storage of yearly goals in Notion
- Easy access to your yearly goals through Notion links

## Setup

### Prerequisites

- Python 3.8+
- Telegram Bot Token (from BotFather)
- OpenAI API Key
- Notion API Key and database ID

### Installation

1. Clone this repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project root with the following variables:
   ```
   TELEGRAM_TOKEN=your_telegram_bot_token
   OPENAI_API_KEY=your_openai_api_key
   NOTION_TOKEN=your_notion_api_key
   NOTION_DATABASE_ID=your_notion_database_id
   ```
4. Run the bot:
   ```
   python main.py
   ```

## Usage

1. Start a conversation with your bot on Telegram
2. Follow the prompts to share your current situation, desires, obligations, identity, strengths, and weaknesses
3. The AI will develop personalized yearly goals based on your responses
4. Once finalized, your yearly goals will be saved to Notion
5. You'll receive a link to view your yearly goals in Notion

## Project Structure

- `main.py`: Core logic and conversation flow
- `telegram_bot.py`: Telegram integration
- `notion_api.py`: Notion API integration
- `config.py`: Configuration and API key management
- `requirements.txt`: Project dependencies

## Future Enhancements

- Support for multiple AI models (Claude, etc.)
- Integration with additional databases
- Calendar integration (Google Calendar, etc.)
- Authentication system
- Goal tracking and reminders
