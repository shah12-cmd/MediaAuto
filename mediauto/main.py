"""Main bot application"""

import logging
import sys

from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler
)

from mediauto.config import config_manager
from mediauto.database import init_database
from mediauto.logger import setup_logger
from mediauto.bot_handler import BotHandlers
from mediauto.scheduler import scheduler


logger = setup_logger()


class MediaAutoBot:

    def __init__(self):
        self.config_manager = config_manager
        self.db_manager = None
        self.application = None
        self.handlers = None


    def initialize(self):
        logger.info("Initializing MediaAuto Bot...")

        db_url = self.config_manager.config.database_url

        if not db_url:
            if self.config_manager.config.database_type == "postgresql":
                db_url = "postgresql://user:password@localhost/mediauto"
            else:
                db_url = "sqlite:///./data/mediauto.db"

        self.db_manager = init_database(db_url)

        self.handlers = BotHandlers(
            self.config_manager,
            self.db_manager
        )

        logger.info("Bot initialization complete")


    def setup_handlers(self):

        self.application = Application.builder().token(
            self.config_manager.config.telegram_token
        ).build()


        # /start
        self.application.add_handler(
            CommandHandler(
                "start",
                self.handlers.start_command
            )
        )


        # ??? ???? ??? Inline
        callbacks = {
            "manage_sources": self.handlers.manage_sources_callback,
            "set_destination": self.handlers.set_destination_callback,
            "set_delay": self.handlers.set_delay_callback,
            "set_ad_text": self.handlers.set_ad_text_callback,
            "caption_settings": self.handlers.caption_settings_callback,
            "ai_settings": self.handlers.ai_settings_callback,
            "watermark_settings": self.handlers.watermark_settings_callback,
            "statistics": self.handlers.statistics_callback,
            "view_logs": self.handlers.view_logs_callback,
            "restart_bot": self.handlers.restart_bot_callback,
        }


        for name, func in callbacks.items():
            self.application.add_handler(
                CallbackQueryHandler(
                    func,
                    pattern=f"^{name}$"
                )
            )


        logger.info("Bot handlers setup complete")


    def run(self):

        try:
            self.initialize()
            self.setup_handlers()

            scheduler.start()

            logger.info("Starting MediaAuto Bot...")

            self.application.run_polling(
                drop_pending_updates=True
            )


        except KeyboardInterrupt:
            logger.info("Bot interrupted")


        except Exception as e:
            logger.error(
                f"Fatal error: {e}",
                exc_info=True
            )
            sys.exit(1)


        finally:
            scheduler.stop()
            logger.info("Bot stopped")



def main():

    bot = MediaAutoBot()
    bot.run()



if __name__ == "__main__":
    main()
