import os
import sys
from server.logger.logger_config import my_logger as logger


os.environ["TOKENIZERS_PARALLELISM"] = "false"


def check_env_variables():
    # URL for obtaining the authentication token
    GET_TOKEN_URL = os.getenv('GET_TOKEN_URL', '')
    if not GET_TOKEN_URL.startswith('http://') and not GET_TOKEN_URL.startswith('https://'):
        logger.error(f"GET_TOKEN_URL: '{GET_TOKEN_URL}' is illegal! It must be like 'http://IP:PORT' or 'https://IP:PORT'")
        sys.exit(-1)

    # URL for adding a new bot
    ADD_BOT_URL = os.getenv('ADD_BOT_URL', '')
    if not ADD_BOT_URL.startswith('http://') and not ADD_BOT_URL.startswith('https://'):
        logger.error(f"ADD_BOT_URL: '{ADD_BOT_URL}' is illegal! It must be like 'http://IP:PORT' or 'https://IP:PORT'")
        sys.exit(-1)

    # URL for updating an existing bot
    UPDATE_BOT_URL = os.getenv('UPDATE_BOT_URL', '')
    if not UPDATE_BOT_URL.startswith('http://') and not UPDATE_BOT_URL.startswith('https://'):
        logger.error(f"UPDATE_BOT_URL: '{UPDATE_BOT_URL}' is illegal! It must be like 'http://IP:PORT' or 'https://IP:PORT'")
        sys.exit(-1)

    # URL for sending messages to IM server
    SEND_MSG_URL = os.getenv('SEND_MSG_URL', '')
    if not SEND_MSG_URL.startswith('http://') and not SEND_MSG_URL.startswith('https://'):
        logger.error(f"SEND_MSG_URL: '{SEND_MSG_URL}' is illegal! It must be like 'http://IP:PORT' or 'https://IP:PORT'")
        sys.exit(-1)

    # Number of days before the token expires
    TOKEN_EXPIRE_DAYS = os.getenv('TOKEN_EXPIRE_DAYS')
    try:
        token_expire_days = int(TOKEN_EXPIRE_DAYS)
    except Exception as e:
        logger.error(f"TOKEN_EXPIRE_DAYS: {TOKEN_EXPIRE_DAYS} is illegal! It should be an integer!")
        sys.exit(-1)

    # Maximum number of messages to keep in session history
    MAX_HISTORY_SESSION_LENGTH = os.getenv('MAX_HISTORY_SESSION_LENGTH')
    try:
        max_history_session_length = int(MAX_HISTORY_SESSION_LENGTH)
    except Exception as e:
        logger.error(f"MAX_HISTORY_SESSION_LENGTH: {MAX_HISTORY_SESSION_LENGTH} is illegal! It should be an integer!")
        sys.exit(-1)

    # Number of seconds before the session expires
    SESSION_EXPIRE_SECONDS = os.getenv('SESSION_EXPIRE_SECONDS')
    try:
        session_expire_seconds = int(SESSION_EXPIRE_SECONDS)
    except Exception as e:
        logger.error(f"SESSION_EXPIRE_SECONDS: {SESSION_EXPIRE_SECONDS} is illegal! It should be an integer!")
        sys.exit(-1)
