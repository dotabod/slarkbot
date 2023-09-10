
import re


async def whats_dn(update, context):
    text = update.message.text
    search_for = "dn"

    if search_for in text.lower():
        await update.message.reply_text("What's DN? :)")
