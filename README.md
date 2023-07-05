
# Slark Bot

Telegram Bot for Dota2. Get DOTA statistics about matches, players, etc

## Prerequisites

- Python 3.6+
- A Telegram account and steam account (to test your changes)
- BeautifulSoup may give issues. You may need to install the system package alongside the virtualenv dependency. There is a package named `bs4` that may also need to be installed with `pip`.

## Installation & Environment Configuration

- Clone or fork the repository and cd into the project root.
  - `git clone https://github.com/slarkbot/slarkbot.git && cd slarkbot`
- Create a virtual environment using `python -m venv venv`
- Activate virtual environment with `source venv/bin/activate` or windows equivalent
- `pip install -r requirements.txt` to install dependencies
- `cp .env.example .env` and change values as needed using the **Environment Variables** section below as a reference.
- `pre-commit install` adds the lint hook to pre-push (makes it look pretty before you PR)
- To run your local development bot, do `./main.py` or `python main.py`.
- Message your bot in telegram with slarkbot commands like `/status` or `/changes` and you should get an OK response.

## Scripts

Scripts are made available to the command line via `setup.py`. To use these scripts, run `python setup.py install`.

## Environment Variables

- `OPEN_DOTA_API_BASE_URL` :: Base url for OpenDota API
- `LOG_LEVEL` :: Log level to use, defaults to `debug`. Options are info, warning, critical, error, and debug
- `TELEGRAM_BOT_TOKEN` :: Bot token obtained from @BotFather on telegram. Used for personal development with live testing
- `POSTGRES_USER` :: User name for the dockerized postgres instance
- `POSTGRES_PASSWORD` :: Password for the dockerized postgres instance
- `POSTGRES_DB` :: Name of the dockerized postgres database
- `POSTGRES_HOST` :: Hostname of the dockerized postgres instance
- `SLARKBOT_VERSION` :: The current semantic version of slarkbot

## Running the Database

### Seeding Data

- `./scripts/seed.py` will seed hero and alias data into the slarkbot database.

## Testing

Test cases uses default Python testing module `unittest` but uses `pytest` as the test runner

- Write your unit tests
- From the command line `pytest`

## Commands

- `/register <your id here>` :: Register your telegram handle to your steam id to use other commands\. Examples: `/register 55678920`, `/register tradeless`, `/register https://steamcommunity\.com/profiles/76561198073221358`\n
- `/help` :: Display this help message\n
- `/matchdata` :: Explains how to expose match data in the game and sync it to Opendota, where Slarkbot gets its data from\n
- `/recents <user:optional> <limit:optional>` :: Look up someone's most recent matches\. Defaults to 5 if limit is not defined and to you if user is not defined\. Must have account id registered using `/register`\. Example :: `/recents`, `/recents 10` for 10 most recent matches, `/recents danvb` for Daniel's last games, `/recents 20 KittyKirov` for Kirov's last 20 games\n
- `/lastmatch <user:optional> <hero:optional>` :: Gets the last match someone played\. Defaults to you if no argument is given\. If a hero name is given, shows the last match that user played with that hero\. User must be registered for this to work \n
- `/rank <user:optional>` :: Gets a user's current medal\. Defaults to you if no argument is given\. User must be registered for this to work \n
- `/winrate <user:optional> <hero name>` :: Gets your or someone else's winrate with the given hero\. User must be registered for this to work\n
