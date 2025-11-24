import logging
import requests
from io import BytesIO
from src.lib import endpoints
from src import constants
from src.bot.models.user import User
from src.bot.models.sessions import create_session
from src.bot.services import hero_services, user_services
from src.bot.commands import helpers, match_helpers
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from src.bot.callback_handlers.match_callbacks import create_inline_keyboard
from src.bot.decorators.require_registered_user_decorator import require_register

logger = logging.getLogger(__name__)

async def run_last_match_command(update, context):
    registered_user = user_services.lookup_user_by_telegram_handle(
        update.message.from_user.username
    )

    args = context.args
    for arg in context.args:
        user = user_services.lookup_user_by_telegram_handle(arg)
        if user:
            registered_user = user
            args.remove(arg)

    hero_id = None
    if args:
        hero_name = " ".join(args)
        hero_id = helpers.get_hero_id_by_name_or_alias(hero_name)
        if not hero_id:
            await update.message.reply_markdown_v2(constants.USER_OR_HERO_NOT_FOUND_MESSAGE)
            return

    if not registered_user:
        await update.message.reply_markdown_v2(constants.USER_NOT_REGISTERED_MESSAGE)
        return

    if hero_id:
        endpoint_name = "get_player_matches_by_hero_id"
        logger.info(f"Fetching matches for account_id={registered_user.account_id}, hero_id={hero_id}")
        response, status_code = endpoints.get_player_matches_by_hero_id(
            registered_user.account_id, hero_id
        )
    else:
        endpoint_name = "get_player_recent_matches_by_account_id"
        logger.info(f"Fetching recent matches for account_id={registered_user.account_id}")
        response, status_code = endpoints.get_player_recent_matches_by_account_id(
            registered_user.account_id
        )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        logger.error(
            f"Bad response from {endpoint_name}: status_code={status_code}, "
            f"account_id={registered_user.account_id}, "
            f"hero_id={hero_id if hero_id else 'N/A'}, "
            f"response={response}, "
            f"telegram_username={update.message.from_user.username}"
        )

        # Provide more helpful error messages for specific status codes
        if status_code == constants.HTTP_STATUS_CODES.NOT_FOUND.value:
            logger.warning(
                f"Account not found in OpenDota: account_id={registered_user.account_id}, "
                f"telegram_username={update.message.from_user.username}"
            )
            await update.message.reply_markdown_v2(constants.ACCOUNT_NOT_FOUND_MESSAGE)
        else:
            await update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)
        return

    try:
        logger.debug(f"Processing match response: response_length={len(response) if response else 0}")
        if not response or len(response) == 0:
            logger.warning(f"Empty response array from {endpoint_name} for account_id={registered_user.account_id}")
            await update.message.reply_markdown_v2(
                r"I could not find a match by those criteria, sorry\!"
            )
            return

        output_message = match_helpers.create_match_message(response[0])
        match = match_helpers.MatchDto(**response[0])
        hero = hero_services.get_hero_by_id(match.hero_id)
        img_url = f"https://cdn.cloudflare.steamstatic.com{hero.img}"

        # Download the image
        logger.debug(f"Downloading hero image from {img_url}")
        img_response = requests.get(img_url)
        img_response.raise_for_status()
        img_bytes = BytesIO(img_response.content)

        button = InlineKeyboardButton(
            "View on stratz",
            url=("https://stratz.com/matches/" + str(response[0]["match_id"])),
        )
        markup = InlineKeyboardMarkup.from_button(button)
        await update.message.reply_photo(photo=img_bytes, caption=output_message, reply_markup=markup)
        logger.info(f"Successfully sent last match response for account_id={registered_user.account_id}")

    except (IndexError, KeyError) as e:
        logger.error(
            f"Error processing match response: {type(e).__name__}: {str(e)}, "
            f"response={response}, account_id={registered_user.account_id}"
        )
        await update.message.reply_markdown_v2(
            r"I could not find a match by those criteria, sorry\!"
        )
    except Exception as e:
        logger.exception(
            f"Unexpected error in run_last_match_command: {type(e).__name__}: {str(e)}, "
            f"account_id={registered_user.account_id}"
        )
        await update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)


async def run_get_match_by_match_id(update, context):
    try:
        match_id = context.args[0]
        match_id = int(match_id)
    except (IndexError, ValueError):
        await update.message.reply_markdown_v2(
            r"That isn't a match ID\. Use `/match <match id here>`"
        )
        return

    response, status_code = endpoints.get_match_by_id(match_id)

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        await update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    output_message = match_helpers.create_match_detail_message(response)

    markup = create_inline_keyboard(match_id)
    await update.message.reply_markdown_v2(
        output_message, reply_markup=markup, disable_web_page_preview=True
    )
