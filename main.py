import os
import openai
from typing import Dict, Any, List

from config import OPENAI_API_KEY, AI_MODEL, AI_SYSTEM_PROMPT, ERROR_MESSAGES
from telegram_bot import TelegramBot
from notion_api import NotionAPI

class GoalBot:
    """Main class that orchestrates the goal-setting workflow."""
    
    def __init__(self):
        """Initialize the GoalBot with necessary components."""
        # Set up OpenAI API
        openai.api_key = OPENAI_API_KEY
        
        # Initialize Notion API client
        self.notion_api = NotionAPI()
        
        # Initialize Telegram bot with callbacks
        self.telegram_bot = TelegramBot(self.process_message, self.save_goals_to_notion)
    
    def start(self):
        """Start the GoalBot."""
        print("Starting GoalBot...")
        self.telegram_bot.start()
    
    def process_message(self, conversation_history: List[Dict[str, str]]) -> str:
        """Process a message from the user with AI.
        
        Args:
            conversation_history: List of conversation messages with roles and content
            
        Returns:
            AI response as a string
        """
        try:
            # Make sure there's a system message at the beginning
            if conversation_history[0]['role'] != 'system':
                conversation_history.insert(0, {
                    'role': 'system',
                    'content': AI_SYSTEM_PROMPT
                })
                
            # Call OpenAI API using the new SDK format
            response = openai.chat.completions.create(
                model=AI_MODEL,
                messages=conversation_history,
                max_completion_tokens=1000
            )
            
            # Extract and return the AI's response
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error processing message with AI: {e}")
            return ERROR_MESSAGES['ai_error']
    
    def save_goals_to_notion(self, conversation_history: List[Dict[str, str]]) -> str:
        """Extract goals from conversation and save to Notion.
        
        Args:
            conversation_history: List of conversation messages with roles and content
            
        Returns:
            URL to the Notion page
        """
        try:
            # Extract conversation for AI to summarize
            messages = [
                {
                    'role': 'system',
                    'content': 'You are a helpful assistant that extracts yearly goals from a conversation. '
                              'Identify the main goals discussed and format them as a clear, numbered list.'
                },
            ]
            
            # Add the relevant conversation messages
            for message in conversation_history:
                if message['role'] != 'system':
                    messages.append(message)
            
            # Call OpenAI API to extract goals using the new SDK format
            response = openai.chat.completions.create(
                model=AI_MODEL,
                messages=messages,
                max_completion_tokens=1000
            )
            
            # Extract the AI's response
            goals_text = response.choices[0].message.content
            
            # Create a Notion page with the extracted goals
            notion_url = self.notion_api.create_goal_page(
                title="Yearly Goals",
                goals=goals_text,
                user_id=str(conversation_history[1]['content'] if len(conversation_history) > 1 else "User")
            )
            
            return notion_url
            
        except Exception as e:
            print(f"Error saving goals to Notion: {e}")
            return ERROR_MESSAGES['notion_error']
        



if __name__ == "__main__":
    # Create and start the GoalBot
    bot = GoalBot()
    bot.start()
