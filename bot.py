import logging
import asyncio
import sys
import os
from typing import Optional, NoReturn
import traceback

from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, CallbackQueryHandler, ContextTypes
)
from handlers import (
    start_command, message_handler, handle_callback,
    help_command, search_files_handler, file_transfer_handler
)
from utils import load_config

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

def log_error(e: Exception, context: str = "") -> None:
    """Log error with full traceback."""
    logger.error(
        f"{'[' + context + '] ' if context else ''}Error occurred: {str(e)}\n"
        f"Traceback:\n{''.join(traceback.format_tb(e.__traceback__))}"
    )

async def error_handler(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log Errors caused by Updates."""
    try:
        if context.error:
            log_error(context.error, "Update Handler")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ Произошла ошибка при выполнении команды.\n"
                "Попробуйте еще раз или обратитесь к администратору."
            )
    except Exception as e:
        log_error(e, "Error Handler")

def setup_handlers(application: Application) -> None:
    """Setup all handlers for the application."""
    try:
        # Add error handler
        application.add_error_handler(error_handler)

        # Add command handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("help", help_command))
        application.add_handler(CommandHandler("search", search_files_handler))
        
        # Add callback query handler
        application.add_handler(CallbackQueryHandler(handle_callback))
        
        # Add message handlers
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
        application.add_handler(MessageHandler(filters.Document.ALL, file_transfer_handler))
        
        logger.info("All handlers have been set up successfully")
    except Exception as e:
        log_error(e, "Setup Handlers")
        raise

def run_bot(application: Application) -> NoReturn:
    """Run the bot with error handling."""
    try:
        logger.info("Starting bot...")
        application.run_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES,
            close_loop=False
        )
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        raise
    except Exception as e:
        log_error(e, "Bot Runtime")
        raise
    finally:
        logger.info("Bot shutdown complete")

def main() -> int:
    """Start the bot."""
    try:
        # Load configuration
        config = load_config()
        if not config:
            logger.error("Could not load configuration!")
            return 1

        # Get token
        token = config.get('TELEGRAM_TOKEN')
        if not token:
            logger.error("No token provided in config!")
            return 1

        # Create application
        application = Application.builder().token(token).build()

        # Setup handlers
        setup_handlers(application)

        # Run the bot
        run_bot(application)
        return 0

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        return 0
    except Exception as e:
        log_error(e, "Main")
        return 1

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        log_error(e, "Program")
        sys.exit(1)
