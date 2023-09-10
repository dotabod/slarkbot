from telegram.helpers import escape_markdown

from src import constants
from src.bot.commands import helpers
from src.bot.decorators.require_hero_args_decorator import require_hero_args
from src.bot.services import hero_services, item_services
from src.lib import endpoints, web_scraper


@require_hero_args
async def run_suggested_builds_command(update, hero):
    response, status_code = endpoints.get_hero_item_popularity(hero.id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        await update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = helpers.create_suggested_build_message(
        hero.localized_name, response
    )

    await update.message.reply_markdown_v2(output_message)


@require_hero_args
async def run_get_hero_aliases(update, hero):
    hero_aliases = hero_services.get_hero_aliases_by_hero_id(hero.id)

    aliases = [alias.alias for alias in hero_aliases]

    output = "Aliases\n%s" % "\n".join(aliases)

    output = escape_markdown(output, version=2)

    await update.message.reply_markdown_v2(output)


@require_hero_args
async def run_get_hero_counters_command(update, hero):
    counters = web_scraper.get_hero_counters(hero.localized_name)

    if not counters:
        await update.message.reply_markdown_v2(
            f"Oops, something went wrong and I don't what happened, try again"
        )

    column_headers = "Hero | Disadvantage | Hero win rate\n"
    output = f"{hero.localized_name.title()} counters\n{column_headers}"

    for counter in counters:
        row = f"{counter[0]} | {counter[1]}% | {counter[2]}%\n"
        output += row

    output = escape_markdown(output, version=2)
    await update.message.reply_markdown_v2(output)
