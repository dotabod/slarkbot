import os

from telegram.ext import CallbackQueryHandler, CommandHandler, Updater

from src.bot import logger_factory
from src.bot.callback_handlers import match_callbacks
from src.bot.commands import (changelog_command, help_commands, match_commands,
                              user_commands)


def create_bot():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    logger = logger_factory.create_logger()
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("register", user_commands.run_register_command))
    dp.add_handler(CommandHandler("rank", user_commands.run_get_player_rank_command))
    dp.add_handler(
        CommandHandler(["winrate", "wr"], user_commands.run_get_player_hero_winrate_command)
    )
    dp.add_handler(
        CommandHandler(
            ["recents", "matches"], user_commands.run_get_player_recents_command
        )
    )
    dp.add_handler(CommandHandler(["help", "start"], help_commands.run_help_command))
    dp.add_handler(CommandHandler(["lastmatch", "lm", "lg"], match_commands.run_last_match_command))
    dp.add_handler(CommandHandler("match", match_commands.run_get_match_by_match_id))
    dp.add_handler(
        CommandHandler(["bros", "gamers"], changelog_command.run_changes_command)
    )
    dp.add_handler(
        CommandHandler("profile", user_commands.run_get_player_steam_profile_command)
    )
    dp.add_handler(
        CommandHandler(
            ["exposedata", "matchdata"], help_commands.run_expose_data_command
        )
    )

    dp.add_handler(
        CallbackQueryHandler(
            match_callbacks.handle_match_details_callback, pattern="(match )[0-9].*"
        )
    )

    return updater, logger
