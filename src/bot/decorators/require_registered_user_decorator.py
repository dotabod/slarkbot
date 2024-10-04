from functools import wraps
from src.bot.services import user_services
from src import constants


def require_register(func):
    """
    A decorator that checks if a user is registered or a registered
    user was given as an argument. Fails if a user was not given and
    if the user that sent the command is not registered
    """

    @wraps(func)
    async def inner(update, context):
        try:
            telegram_handle = context.args[0]
        except (IndexError, ValueError):
            telegram_handle = update.message.from_user.username

        user = user_services.lookup_user_by_telegram_handle(telegram_handle)

        if not user:
            await update.message.reply_markdown_v2(
                constants.USER_NOT_REGISTERED_MESSAGE
            )
            return

        await func(update, context, user)

    return inner
