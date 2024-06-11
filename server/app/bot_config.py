import json
from typing import Dict, Any
from server.app.utils.diskcache_client import diskcache_client
from server.logger.logger_config import my_logger as logger


def get_bot_setting() -> None:
    setting_data = None
    try:
        # Attempt to get the chatbot setting from Cache
        key = "open_kf:chatbot_setting"
        setting_cache = diskcache_client.get(key)
        if setting_cache:
            setting_data = json.loads(setting_cache)
        else:
            logger.warning(f"could not find '{key}' in Cache!")
    except Exception as e:
        logger.error(f"Get bot setting from Cache, excpetion: {e}")
    return setting_data


def save_bot_setting(bot_config_dict: Dict[str, Any]) -> None:
    try:
        # Save the chatbot setting in Cache
        key = "open_kf:chatbot_setting"
        diskcache_client.set(key, json.dumps(bot_config_dict))
    except Exception as e:
        logger.error(f"Save bot setting in Cache is failed, exception: {e}")
