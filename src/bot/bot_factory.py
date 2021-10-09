import os
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    Filters,
)

from src.bot import logger_factory
from src.bot.commands import health_check_command
from src.bot.commands import user_commands
from src.bot.commands import help_commands
from src.bot.commands import match_commands
from src.bot.commands import changelog_command
from src.bot.commands import hero_commands

from src.bot.message_handlers.freedom_units import convert_to_freedom_units
from src.bot.message_handlers.liberal_units import convert_to_liberal_units
from src.bot.message_handlers.youre_welcome import say_youre_welcome
from src.bot.message_handlers.nice import say_nice
from src.bot.message_handlers.who_asked import who_asked
from src.bot.message_handlers.feel_bad import feel_bad

from src.bot.callback_handlers import match_callbacks

from src.constants import LOG_LEVEL_MAP


def create_bot():
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

    logger = logger_factory.create_logger()
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("status", health_check_command.run_health_check))
    dp.add_handler(CommandHandler("register", user_commands.run_register_command))
    dp.add_handler(CommandHandler("rank", user_commands.run_get_player_rank_command))
    dp.add_handler(
        CommandHandler("winrate", user_commands.run_get_player_hero_winrate_command)
    )
    dp.add_handler(
        CommandHandler(
            ["recents", "matches"], user_commands.run_get_player_recents_command
        )
    )
    dp.add_handler(CommandHandler(["help", "start"], help_commands.run_help_command))
    dp.add_handler(CommandHandler("lastmatch", match_commands.run_last_match_command))
    dp.add_handler(CommandHandler("match", match_commands.run_get_match_by_match_id))
    dp.add_handler(
        CommandHandler(["changes", "changelog"], changelog_command.run_changes_command)
    )
    dp.add_handler(
        CommandHandler("profile", user_commands.run_get_player_steam_profile_command)
    )
    dp.add_handler(CommandHandler("build", hero_commands.run_suggested_builds_command))
    dp.add_handler(
        CommandHandler(["alias", "aliases"], hero_commands.run_get_hero_aliases)
    )
    dp.add_handler(
        CommandHandler(
            ["counter", "counters"], hero_commands.run_get_hero_counters_command
        )
    )
    dp.add_handler(
        CommandHandler(
            ["exposedata", "matchdata"], help_commands.run_expose_data_command
        )
    )

    # Group handlers with the same trigger separately
    # to ensure they don't conflict with each other
    dp.add_handler(
        MessageHandler(Filters.text & ~Filters.command, say_youre_welcome), 1
    )
    dp.add_handler(
        MessageHandler(Filters.text & ~Filters.command, convert_to_freedom_units), 2
    )
    dp.add_handler(
        MessageHandler(Filters.text & ~Filters.command, convert_to_liberal_units), 3
    )
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, say_nice), 4)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, who_asked), 5)
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, feel_bad), 6)

    dp.add_handler(
        CallbackQueryHandler(
            match_callbacks.handle_match_details_callback, pattern="(match )[0-9].*"
        )
    )

    return updater, logger
