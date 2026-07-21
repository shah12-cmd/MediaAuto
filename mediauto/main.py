"""Main bot application"""

import asyncio
import logging
import sys
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from mediauto.config import config_manager
from mediauto.database import init_database, get_db
from mediauto.logger import setup_logger
from mediauto.bot_handler import BotHandlers
from mediauto.scheduler import scheduler

logger = setup_logger()


class MediaAutoBot:
    """Main bot application class"""
    
    def __init__(self):
        self.config_manager = config_manager
        self.db_manager = None
        self.application = None
        self.handlers = None
    
    def initialize(self):
        """Initialize bot components"""
        logger.info("Initializing MediaAuto Bot...")
        
        # Initialize database
        db_url = self.config_manager.config.database_url
        if not db_url:
            if self.config_manager.config.database_type == "postgresql":
                db_url = "postgresql://user:password@localhost/mediauto"
            else:
                db_url = "sqlite:///./data/mediauto.db"
        
        self.db_manager = init_database(db_url)
        
        # Create bot handlers
        self.handlers = BotHandlers(self.config_manager, self.db_manager)
        
        logger.info("Bot initialization complete")
    
    def setup_handlers(self):
        """Setup Telegram bot handlers"""
        # Create application
        self.application = Application.builder().token(
            self.config_manager.config.telegram_token
        ).build()
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        
        # Callback handlers
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.manage_sources_callback, pattern="^manage_sources$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.set_destination_callback, pattern="^set_destination$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.set_delay_callback, pattern="^set_delay$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.set_ad_text_callback, pattern="^set_ad_text$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.caption_settings_callback, pattern="^caption_settings$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.ai_settings_callback, pattern="^ai_settings$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.watermark_settings_callback, pattern="^watermark_settings$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.statistics_callback, pattern="^statistics$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.view_logs_callback, pattern="^view_logs$"
        ))
        self.application.add_handler(CallbackQueryHandler(
            self.handlers.restart_bot_callback, pattern="^restart_bot$"
        ))
        
        logger.info("Bot handlers setup complete")
    
    async def run(self):
        """Run the bot"""
        try:
            self.initialize()
            self.setup_handlers()
            
            # Start scheduler
            scheduler.start()
            
            logger.info("Starting MediaAuto Bot...")
            await self.application.run_polling()
        
        except KeyboardInterrupt:
            logger.info("Bot interrupted by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}", exc_info=True)
            sys.exit(1)
        finally:
            scheduler.stop()
            logger.info("Bot stopped")


def main():
    """Main entry point"""
    bot = MediaAutoBot()
    asyncio.run(bot.run())


if __name__ == "__main__":
    main()
