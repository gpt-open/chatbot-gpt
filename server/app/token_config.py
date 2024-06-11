import json
import os
from typing import Dict, Any, Tuple
import requests
from server.app.utils.diskcache_client import diskcache_client
from server.logger.logger_config import my_logger as logger


GET_TOKEN_URL = os.getenv('GET_TOKEN_URL')
TOKEN_EXPIRE_DAYS = os.getenv('TOKEN_EXPIRE_DAYS')


def get_token() -> Tuple[str, str]:
    url = GET_TOKEN_URL
    logger.warning(f"url: {url}")
    payload = json.dumps({
       "account": "chatAdmin",
       "password": "625031fc4e4f2de6b187e6bfa3697784"
    })
    headers = {
       'operationID': '123',
       'Content-Type': 'application/json'
    }

    token_setting_dict = None
    try:
        resp = requests.request("POST", url, headers=headers, data=payload)
        if resp.status_code == requests.codes.ok:
            ret = json.loads(resp.text)
            if ret["errCode"] != 0:
                logger.error(f"get_token is failed, ret: {ret}")
            else:
                token_setting_dict = {
                    "admin_token": ret["data"]["adminToken"],
                    "im_token": ret["data"]["imToken"]
                }
                save_token_setting(token_setting_dict)
        else:
            logger.error(f"get_token is failed. Status code: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        logger.error(f"get_token is faild, exception: {e}")
    return token_setting_dict


def get_token_setting(is_init: bool = False) -> None:
    setting_data = None
    try:
        if not is_init:
            # Attempt to get the token setting from Cache
            key = "open_kf:token_setting"
            setting_cache = diskcache_client.get(key)
            if setting_cache:
                setting_data = json.loads(setting_cache)
            else:
                logger.warning(f"Could not find '{key}' in Cache! Need to fetch from '{GET_TOKEN_URL}'!")
                setting_data = get_token()
                logger.info(f"Fetch token_setting: {setting_data}")
                save_token_setting(setting_data)
        else:
            setting_data = get_token()
            logger.info(f"Fetch token_setting: {setting_data}")
            save_token_setting(setting_data)
    except Exception as e:
        logger.error(f"Get token setting from Cache, excpetion: {e}")
    return setting_data


def save_token_setting(token_config_dict: Dict[str, Any]) -> None:
    try:
        # Save the token setting in Cache
        key = "open_kf:token_setting"
        ttl = int(TOKEN_EXPIRE_DAYS) * 86400
        diskcache_client.set(key, json.dumps(token_config_dict), ttl)
    except Exception as e:
        logger.error(f"Save token seeting in Cache is failed, exception: {e}")
