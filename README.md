
# Slark Bot

Telegram Bot for Dota2. Get DOTA statistics about matches, players, etc

The `docs` directory contains some handy documentation for various purposes.

## Prerequisites
 - Python 3.6+
 - A Telegram account and steam account (to test your changes)
 - BeautifulSoup may give issues. You may need to install the system package alongside the virtualenv dependency. There is a package named `bs4` that may also need to be installed with `pip`.

## Installation & Environment Configuration
 - Clone or fork the repository and cd into the project root.
    * `git clone https://github.com/slarkbot/slarkbot.git && cd slarkbot`
 - Create a virtual environment using `python -m venv venv`
 - Activate virtual environment with `source venv/bin/activate` or windows equivalent
 - `pip install -r requirements.txt` to install dependencies
 - `cp .env.example .env` and change values as needed using the **Environment Variables** section below as a reference.
 - `pre-commit install` adds the lint hook to pre-push (makes it look pretty before you PR)
 - To run your local development bot, do `./main.py` or `python main.py`.
 - Message your bot in telegram with slarkbot commands like `/status` or `/changes` and you should get an OK response.

## Scripts
Scripts are made available to the command line via `setup.py`. To use these scripts, run `python setup.py install`.
The following is a short list of the scripts provided with a short description:
 - `slarbot_reseed` :: Drop, recreate, and reseed the slarkbot database

Usage for these scripts are as follows:
`$ slarkbot_reseed`

## Environment Variables
 - `OPEN_DOTA_API_BASE_URL` :: Base url for OpenDota API
 - `LOG_LEVEL` :: Log level to use, defaults to `debug`. Options are info, warning, critical, error, and debug
 - `TELEGRAM_BOT_TOKEN` :: Bot token obtained from @BotFather on telegram. Used for personal development with live testing
 - `POSTGRES_USER` :: User name for the dockerized postgres instance
 - `POSTGRES_PASSWORD` :: Password for the dockerized postgres instance
 - `POSTGRES_DB` :: Name of the dockerized postgres database
 - `SLARKBOT_VERSION` :: The current semantic version of slarkbot

## Running the Database

### Seeding Data
 - `./scripts/seed.py` will seed hero and alias data into the slarkbot database.

## Testing
Test cases uses default Python testing module `unittest` but uses `pytest` as the test runner
 - Write your unit tests
 - From the command line `pytest`

## Slarkbot Directory Structure
 - `scripts` :: Handy scripts to manage and configure slarkbot and his database,.
 - `src` :: All of the code and logic to make slarkbot run
 - `src/bot` :: All of the logic related to bot aspect of slarkbot. This includes `bot_factory.py` which registers all of the commands, message handlers, etc and creates a `bot` object.
 - `src/constant_data` :: soon to be deprecated. Holds JSON for constant lookups.
 - `src/lib` :: API requests and responses are handled here.
 - `src/test` :: Unit tests for endpoint and API logic.
 - `src/bot/models` :: Holds ORM models used by `src/bot/services`
 - `src/bot/services` :: Data access services. Uses the SQLAlchemy ORM to perform database operations.
 - `src/bot/commands` :: Holds all of the commands for slarkbot. Anything starting with `/` is considered a command. Register these in `bot_factory.py`.
 - `src/bot/message_handlers` :: Logic to handle messages based on regex matches. When slarkbot says you're welcome after you thank him, thats a message handler.
 - `src/bot/callback_handlers` :: Used for telegram inline querying.

## Commands
Commands must preceed with `/` and match arguments given in the help text.
 - `/help` :: Show a help text describing commands and usage.
 - `/register <friend_id>` :: Register your friend ID to your telegram handle. Must be done to use some commands. Your friend ID is found on your dota profile in game.
 - `/status` :: Check to see if everything is up and running.
