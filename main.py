#!/usr/bin/env python

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

os.environ["ROOT_DIR"] = os.path.abspath(os.curdir)

# Disable SSL verification if environment variable is set
# This must be done before importing any modules that use requests
if os.getenv("DISABLE_SSL_VERIFY", "").lower() == "true":
    import ssl
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Also monkey-patch requests to disable SSL verification
    import requests
    original_request = requests.Session.request
    
    def patched_request(self, *args, **kwargs):
        kwargs['verify'] = False
        return original_request(self, *args, **kwargs)
    
    requests.Session.request = patched_request

from src.lib.endpoints import get_health_check
from src.config import check_config
from src.bot import bot_factory
from telegram import Update


def main():
    check_config()

    application, logger = bot_factory.create_bot()
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
