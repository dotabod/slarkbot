import logging
import os
import requests
import functools

logger = logging.getLogger(__name__)


def build_url(uri):
    API_URL = os.getenv("OPEN_DOTA_API_BASE_URL")
    # Remove trailing slash from API_URL if present
    API_URL = API_URL.rstrip("/")
    url = f"{API_URL}/{uri}"
    return url


def make_request(uri):
    url = build_url(uri)
    logger.debug(f"Making API request to: {url}")
    response = requests.get(url)
    logger.debug(f"API response: status_code={response.status_code}, url={url}")
    if response.status_code != 200:
        try:
            error_body = response.json()
            logger.warning(f"API error response: {error_body}, url={url}")
        except Exception:
            logger.warning(f"API error response (non-JSON): status_code={response.status_code}, url={url}")
    return response
