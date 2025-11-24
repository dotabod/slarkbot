import logging
from . import request
from src.constants import API_URI_ENDPOINTS

logger = logging.getLogger(__name__)


def get_health_check():
    """
    returns response json and status code
    """
    uri = API_URI_ENDPOINTS.HEALTH_CHECK.value
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_match_by_id(id):
    uri = API_URI_ENDPOINTS.MATCHES.value % id
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_players_by_rank():
    uri = API_URI_ENDPOINTS.PLAYERS_BY_RANK.value
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_player_by_account_id(id):
    uri = API_URI_ENDPOINTS.PLAYERS_BY_ACCOUNT_ID.value % id
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_player_recent_matches_by_account_id(id):
    uri = API_URI_ENDPOINTS.PLAYER_RECENTS_BY_ACCOUNT_ID.value % id
    logger.debug(f"Getting recent matches for account_id={id}, uri={uri}")
    response = request.make_request(uri)
    try:
        response_json = response.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON response for account_id={id}: {e}, status_code={response.status_code}, response_text={response.text[:500]}")
        return {"error": "Failed to parse response"}, response.status_code
    return response_json, response.status_code


def get_player_matches_by_hero_id(id, hero_id):
    uri = API_URI_ENDPOINTS.PLAYER_MATCHES_BY_HERO.value % (id, hero_id)
    logger.debug(f"Getting matches for account_id={id}, hero_id={hero_id}, uri={uri}")
    response = request.make_request(uri)
    try:
        response_json = response.json()
    except Exception as e:
        logger.error(f"Failed to parse JSON response for account_id={id}, hero_id={hero_id}: {e}, status_code={response.status_code}, response_text={response.text[:500]}")
        return {"error": "Failed to parse response"}, response.status_code
    return response_json, response.status_code


def get_hero_stats():
    uri = API_URI_ENDPOINTS.HERO_STATS.value
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_constant_data(resource_name):
    uri = API_URI_ENDPOINTS.CONSTANTS.value % resource_name
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_player_rank_by_account_id(account_id):
    uri = API_URI_ENDPOINTS.PLAYERS.value % account_id
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_player_hero_stats(id):
    uri = API_URI_ENDPOINTS.PLAYER_HERO_STATS.value % id
    response = request.make_request(uri)
    return response.json(), response.status_code


def get_hero_item_popularity(id):
    uri = API_URI_ENDPOINTS.HERO_ITEM_POPULARITY.value % id
    response = request.make_request(uri)
    return response.json(), response.status_code
