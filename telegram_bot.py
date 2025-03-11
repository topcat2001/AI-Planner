from typing import Dict, Any, Callable
from telegram import Update, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

from config import TELEGRAM_TOKEN, WELCOME_MESSAGE, ERROR_MESSAGES

class TelegramBot:
    """Handles all interactions with the Telegram API."""
    
    def __init__(self, process_message_callback: Callable, save_goals_callback: Callable):
        """Initialize the Telegram bot.
        
        Args:
            process_message_callback: Callback function to process user messages with AI
            save_goals_callback: Callback function to save goals to Notion
        """
        self.token = TELEGRAM_TOKEN
        self.process_message = process_message_callback
        self.save_goals = save_goals_callback
        self.conversations = {}
    
    def start(self):
        """Start the Telegram bot."""
        try:
            # Create the Updater and pass it the bot's token
            updater = Updater(self.token)
            
            # Get the dispatcher to register handlers
            dispatcher = updater.dispatcher
            
            # Add command handlers
            dispatcher.add_handler(CommandHandler("start", self._start_command))
            dispatcher.add_handler(CommandHandler("chat", self._chat_command))
            dispatcher.add_handler(CommandHandler("save", self._save_command))
            dispatcher.add_handler(CommandHandler("cancel", self._cancel_command))
            dispatcher.add_handler(CommandHandler("help", self._help_command))
            
            # Add message handler for regular messages
            dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self._handle_message))
            
            # Add error handler
            dispatcher.add_error_handler(self._error_handler)
            
            # Start the Bot
            updater.start_polling()
            print("Telegram bot started successfully!")
            
            # Run the bot until the user presses Ctrl-C
            updater.idle()
            
        except Exception as e:
            print(f"Error starting Telegram bot: {e}")
    
    def _start_command(self, update: Update, context: CallbackContext) -> None:
        """Handle the /start command."""
        update.message.reply_text(WELCOME_MESSAGE, parse_mode=ParseMode.MARKDOWN)
    
    def _help_command(self, update: Update, context: CallbackContext) -> None:
        """Handle the /help command."""
        update.message.reply_text(
            "Here are the commands you can use:\n\n"
            "/chat - Start or continue our conversation about your goals\n"
            "/save - Save the current goals to Notion\n"
            "/cancel - End the current conversation\n"
            "/help - Show this help message"
        )
    
    def _chat_command(self, update: Update, context: CallbackContext) -> None:
        """Start or continue a chat conversation."""
        user_id = update.effective_user.id
        
        # Initialize conversation if it doesn't exist
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            # Add system message to conversation history
            self.conversations[user_id].append({"role": "system", "content": "You are a yearly goal-setting assistant helping the user develop meaningful goals."})
            update.message.reply_text("Let's talk about your goals! Tell me about what you'd like to achieve this year.")
        else:
            update.message.reply_text("Continuing our conversation. What else would you like to discuss about your goals?")
    
    def _save_command(self, update: Update, context: CallbackContext) -> None:
        """Save the current goals to Notion."""
        user_id = update.effective_user.id
        
        if user_id not in self.conversations or len(self.conversations[user_id]) <= 1:  # Only system message
            update.message.reply_text("We haven't discussed any goals yet. Use /chat to start a conversation.")
            return
        
        update.message.reply_text("Processing your goals and saving them to Notion...")
        
        try:
            # Call the save_goals callback with the conversation history
            notion_url = self.save_goals(self.conversations[user_id])
            
            # Send success message with the Notion URL
            update.message.reply_text(
                f"Your goals have been saved to Notion! You can view them here: {notion_url}",
                parse_mode=ParseMode.MARKDOWN
            )
        except Exception as e:
            print(f"Error saving goals to Notion: {e}")
            update.message.reply_text(ERROR_MESSAGES["notion_error"])
    
    def _cancel_command(self, update: Update, context: CallbackContext) -> None:
        """Cancel the current conversation."""
        user_id = update.effective_user.id
        
        if user_id in self.conversations:
            del self.conversations[user_id]
        
        update.message.reply_text("Conversation ended. Use /chat to start a new conversation about your goals.")
    
    def _handle_message(self, update: Update, context: CallbackContext) -> None:
        """Handle regular text messages from the user."""
        user_id = update.effective_user.id
        user_message = update.message.text
        
        # Initialize conversation if it doesn't exist
        if user_id not in self.conversations:
            self.conversations[user_id] = []
            # Add system message to conversation history
            self.conversations[user_id].append({"role": "system", "content": "You are a yearly goal-setting assistant helping the user develop meaningful goals."})
            
        # Add user message to conversation history
        self.conversations[user_id].append({"role": "user", "content": user_message})
        
        try:
            # Process the message with AI
            ai_response = self.process_message(self.conversations[user_id])
            
            # Add AI response to conversation history
            self.conversations[user_id].append({"role": "assistant", "content": ai_response})
            
            # Send the AI response to the user
            update.message.reply_text(ai_response, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            print(f"Error processing message: {e}")
            update.message.reply_text(ERROR_MESSAGES["ai_error"])
    
    def _error_handler(self, update: object, context: CallbackContext) -> None:
        """Handle errors in the dispatcher."""
        print(f"Error: {context.error}")
