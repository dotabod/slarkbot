import time
from io import BytesIO

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from src import constants
from src.bot.callback_handlers.match_callbacks import create_inline_keyboard
from src.bot.commands import helpers, match_helpers
from src.bot.decorators.require_registered_user_decorator import \
    require_register
from src.bot.models.sessions import create_session
from src.bot.models.user import User
from src.bot.services import hero_services, user_services
from src.lib import endpoints

# Function to take a screenshot of a specific element on a webpage


def capture_screenshot_of_element(url, xpath):
    # Set up Selenium webdriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run Chrome in headless mode (no GUI)
    # Disable GPU acceleration for headless mode
    options.add_argument('--disable-gpu')
    s=Service('/usr/bin/chromium')
    driver = webdriver.Chrome(service=s, options=options)

    try:
        # Open the webpage
        driver.get(url)

        # Wait for the page to finish loading (you can increase the wait time if needed)
        time.sleep(5)

        # Find the element by XPath
        element = driver.find_element(By.XPATH, xpath)

        # Get the dimensions of the element
        element_width = element.size['width']
        element_height = element.size['height']

        # Set the window size to match the element's dimensions (1080p resolution)
        driver.set_window_size(element_width, element_height)

        # Take a screenshot of the element
        screenshot = element.screenshot_as_png

        return screenshot

    finally:
        # Close the browser window
        driver.quit()


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

    if args:
        hero_name = " ".join(args)
        hero_id = helpers.get_hero_id_by_name_or_alias(hero_name)
        if not hero_id:
            await update.message.reply_markdown_v2(constants.USER_OR_HERO_NOT_FOUND_MESSAGE)

    if not registered_user:
        await update.message.reply_markdown_v2(constants.USER_NOT_REGISTERED_MESSAGE)

    if "hero_id" in locals():
        response, status_code = endpoints.get_player_matches_by_hero_id(
            registered_user.account_id, hero_id
        )
    else:
        response, status_code = endpoints.get_player_recent_matches_by_account_id(
            registered_user.account_id
        )

    if status_code != constants.HTTP_STATUS_CODES.OK.value:
        await update.message.reply_text(constants.BAD_RESPONSE_MESSAGE)

    try:
        output_message = match_helpers.create_match_message(response[0])
        match = match_helpers.MatchDto(**response[0])
        hero = hero_services.get_hero_by_id(match.hero_id)
        url=("https://stratz.com/matches/" + str(response[0]["match_id"]))
        img_url = f"https://cdn.cloudflare.steamstatic.com{hero.img}"

        # Capture a screenshot of the specified element
        element_xpath = "/html/body/main/div[3]/div[2]/div[2]"
        screenshot = capture_screenshot_of_element(url, element_xpath)

        # Send the screenshot as a photo
        img_bytes = BytesIO(screenshot)
        button = InlineKeyboardButton(
            "View on stratz",
            url,
        )
        markup = InlineKeyboardMarkup.from_button(button)
        await update.message.reply_photo(photo=img_bytes, caption=output_message, reply_markup=markup)

    except IndexError:
        await update.message.reply_markdown_v2(
            "I could not find a match by those criteria, sorry\!"
        )


async def run_get_match_by_match_id(update, context):
    try:
        match_id = context.args[0]
        match_id = int(match_id)
    except (IndexError, ValueError):
        await update.message.reply_markdown_v2(
            "That isn't a match ID\. Use `/match <match id here>`"
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
