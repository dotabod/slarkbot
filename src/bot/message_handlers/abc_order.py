import re

async def abc_order(update, context):
    text = update.message.text

    # Remove non-alphabetical characters and split the text into words
    words = re.findall(r'\b[a-zA-Z]+\b', text)

    # Check if the letter of each word is in alphabetical order
    is_in_order = all(''.join(sorted(word)) == word for word in words)

    if is_in_order:
        await update.message.reply_text("Would you look at that, all of the words in your message are in alphabetical order.")

