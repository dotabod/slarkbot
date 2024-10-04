import re


async def say_youre_welcome(update, context):
    text = update.message.text
    text_options = [
        "thanks pudgebot",
        "thank you pudgebot",
        "thanksies pudgebot",
        "thamks pudgebot",
    ]
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(" +", " ", text)

    if any(x in text.lower() for x in text_options):
        await update.message.reply_text("You're welcome :)")
        update.message.reply_sticker(
            "CAACAgQAAx0CPjTD9AABC2m9YLfsTcojjSPl7L_DFbWS3IWrp34AAocAA_tjggqQUNMScJneeB8E",
            quote=False,
        )
