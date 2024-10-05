import time
from sqlalchemy.exc import OperationalError
from functools import wraps
from src.bot.models.user import User
from src.bot.models.sessions import create_session

def retry_on_exception(exception, tries=3, delay=2, backoff=2):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _tries, _delay = tries, delay
            while _tries > 1:
                try:
                    return func(*args, **kwargs)
                except exception as e:
                    time.sleep(_delay)
                    _tries -= 1
                    _delay *= backoff
            return func(*args, **kwargs)
        return wrapper
    return decorator

@retry_on_exception(OperationalError)
def lookup_user_by_telegram_handle(telegram_handle):
    telegram_handle = telegram_handle.lower().replace("@", "")
    session = create_session()
    try:
        bot_user = (
            session.query(User)
            .order_by(User.updated_at.desc().nullslast(), User.user_id.desc())
            .filter(User.telegram_handle == telegram_handle)
            .first()
        )
    finally:
        session.close()
    return bot_user

@retry_on_exception(OperationalError)
def lookup_user_by_account_id(account_id):
    account_id = int(account_id)
    session = create_session()
    try:
        bot_user = (
            session.query(User)
            .order_by(User.updated_at.desc().nullslast(), User.user_id.desc())
            .filter(User.account_id == account_id)
            .first()
        )
    finally:
        session.close()
    return bot_user
