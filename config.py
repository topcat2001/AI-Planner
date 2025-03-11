import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram configuration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')

# OpenAI configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AI_MODEL = os.getenv('AI_MODEL', 'gpt-4')

# Notion configuration
NOTION_TOKEN = os.getenv('NOTION_TOKEN')
NOTION_DATABASE_ID = os.getenv('NOTION_DATABASE_ID')

# Bot messages
WELCOME_MESSAGE = """Welcome to the AI Goal Planner! 🎯

I'm here to help you create meaningful yearly goals.

Commands:
/chat - Start or continue our conversation about your goals
/save - Save the current goals to Notion
/cancel - End the current conversation

Let's get started! Use /chat to begin."""

# AI system prompt
AI_SYSTEM_PROMPT = """You are a yearly goal-setting assistant. Your purpose is to help users develop meaningful yearly goals. 
Be conversational, empathetic, and guide the user through a natural discussion about their goals.

You should:
1. Ask about their current situation, desires, obligations, identity, strengths, and weaknesses
2. Help them develop 3-5 well-crafted yearly goals that are SMART (specific, measurable, achievable, relevant, time-bound)
3. For each goal, explain why it matters and suggest 2-3 actionable next steps

When the user is satisfied with their goals, remind them they can use /save to store them in Notion."""

# Error messages
ERROR_MESSAGES = {
    "general": "Sorry, something went wrong. Please try again later.",
    "ai_error": "I'm having trouble connecting to my brain right now. Please try again in a moment.",
    "notion_error": "I couldn't save your goals to Notion. Please check your connection and try again.",
    'telegram_connection': "Error connecting to Telegram. Please check your token and internet connection.",
    'openai_connection': "Error connecting to OpenAI. Please check your API key and internet connection.",
    'notion_connection': "Error connecting to Notion. Please check your API token and database ID.",
    'general': "An error occurred. Please try again later."
}
