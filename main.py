#!/usr/bin/env python

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

os.environ["ROOT_DIR"] = os.path.abspath(os.curdir)

from src.lib.endpoints import get_health_check
from src.config import check_config
from src.bot import bot_factory


def main():
    check_config()

    application, logger = bot_factory.create_bot()
    application.run_polling(allowed_updates=Update.ALL_TYPES)
    application.idle()


if __name__ == "__main__":
    main()
