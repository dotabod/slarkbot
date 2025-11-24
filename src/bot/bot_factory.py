import os
import ssl

from telegram.ext import Application, CallbackQueryHandler, CommandHandler, Updater

from src.bot import logger_factory
from src.bot.callback_handlers import match_callbacks
from src.bot.commands import (changelog_command, help_commands, match_commands,
                              user_commands)


def create_bot():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    logger = logger_factory.create_logger()
    
    # Build application with SSL verification disabled if env variable is set
    builder = Application.builder().token(bot_token)
    
    if os.getenv("DISABLE_SSL_VERIFY", "").lower() == "true":
        # Monkey-patch httpx to disable SSL verification
        import httpx
        original_async_client_init = httpx.AsyncClient.__init__
        
        def patched_async_client_init(self, *args, **kwargs):
            kwargs['verify'] = False
            return original_async_client_init(self, *args, **kwargs)
        
        httpx.AsyncClient.__init__ = patched_async_client_init
    
    application = builder.build()

    application.add_handler(CommandHandler("register", user_commands.run_register_command))
    application.add_handler(CommandHandler("rank", user_commands.run_get_player_rank_command))
    application.add_handler(
        CommandHandler(["winrate", "wr"], user_commands.run_get_player_hero_winrate_command)
    )
    application.add_handler(
        CommandHandler(
            ["recents", "matches"], user_commands.run_get_player_recents_command
        )
    )
    application.add_handler(CommandHandler(["help", "start"], help_commands.run_help_command))
    application.add_handler(CommandHandler(["lastmatch", "lm", "lg"], match_commands.run_last_match_command))
    application.add_handler(CommandHandler("match", match_commands.run_get_match_by_match_id))
    application.add_handler(
        CommandHandler(["bros", "gamers"], changelog_command.run_changes_command)
    )
    application.add_handler(
        CommandHandler("profile", user_commands.run_get_player_steam_profile_command)
    )
    application.add_handler(
        CommandHandler(
            ["exposedata", "matchdata"], help_commands.run_expose_data_command
        )
    )

    application.add_handler(
        CallbackQueryHandler(
            match_callbacks.handle_match_details_callback, pattern="(match )[0-9].*"
        )
    )

    return application, logger
