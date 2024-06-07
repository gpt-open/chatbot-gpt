from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
from server.constant.env_constants import check_env_variables
check_env_variables()


from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import sys
from typing import Dict, Any
import requests
import yaml
from server.app.bot_config import save_bot_setting, get_bot_setting
from server.app.token_config import save_token_setting, get_token_setting
from server.constant.constants import BOT_CONFIG_PATH
from server.logger.logger_config import my_logger as logger


ADD_BOT_URL = os.getenv('ADD_BOT_URL')
UPDATE_BOT_URL = os.getenv('UPDATE_BOT_URL')


def load_bot_config(config_path: str) -> Dict[str, Any]:
    config_dict = None
    with open(config_path, 'r') as fd:
        config_dict = yaml.safe_load(fd)
    
    robot_dict = {}
    user_id_set = set()
    if config_dict:
        bot_dict = config_dict["robots"]
        for llmname in bot_dict:
            for bot in bot_dict[llmname]:
                user_id = bot["userID"]
                if user_id in user_id_set:
                    logger.error(f"userID: '{user_id}' is duplicated!")
                    sys.exit(-1)

                user_id_set.add(user_id)
                if bot["apiKey"] != "xxxx":
                    bot["llmname"] = llmname
                    robot_dict[user_id] = bot

    if robot_dict:
        save_bot_setting(robot_dict)
    else:
        logger.error("load_bot_config is failed! No usable bot configuration found.")
        sys.exit(-1)
    return robot_dict


def add_bot_info(user_id: str, nickname: str, face_url: str, token: str) -> None:
    url = ADD_BOT_URL
    payload = json.dumps({
       "users": [
          {
             "userID": user_id,
             "nickname": nickname,
             "faceURL": face_url,
             "email": f"{user_id}@gpt.com"
          }
       ]
    })
    headers = {
       'OperationID': '123',
       'token': token,
       'Content-Type': 'application/json'
    }
    try:
        resp = requests.request("POST", url, headers=headers, data=payload)
        if resp.status_code == requests.codes.ok:
            logger.warning(f"resp: {resp.text}")
        else:
            logger.error(f"Failed to add bot info. Status code: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        logger.error(f"add_bot_info is failed, user_id: '{user_id}', the exception is {e}")


def update_bot_info(user_id: str, nickname: str, face_url: str, token: str) -> None:
    url = UPDATE_BOT_URL
    payload = json.dumps({
         "userID": user_id,
         "nickname": nickname,
         "faceURL": face_url,
         "email": f"{user_id}@gpt.com"
    })
    headers = {
       'OperationID': '123abc#$xyz',
       'token': token,
       'Content-Type': 'application/json'
    }
    try:
        resp = requests.request("POST", url, headers=headers, data=payload)
        if resp.status_code == requests.codes.ok:
            logger.warning(f"resp: {resp.text}")
        else:
            logger.error(f"Failed to update bot info. Status code: {resp.status_code}, Response: {resp.text}")
    except Exception as e:
        logger.error(f"update_bot_info is failed, user_id: '{user_id}', the exception is {e}")


def upload_bot_info() -> None:
    robot_dict = get_bot_setting()
    if not robot_dict:
        logger.error("robot setting is empty!")
        sys.exit(-1)

    is_init = True
    token_dict = get_token_setting(is_init)
    if not token_dict:
        logger.error("getting token is failed!")
        sys.exit(-1)

    logger.warning(f"bot_info: {robot_dict}")
    logger.warning(f"token_info: {token_dict}")

    with ThreadPoolExecutor() as executor:
        # First, execute the function to add user information
        futures = [executor.submit(add_bot_info, user_id, bot['nickname'], bot['faceURL'], token_dict["admin_token"])
                   for user_id, bot in robot_dict.items()]

        # Wait for all add operations to complete
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                logger.error(f'add_bot_info generated an exception: {e}')

        # After all add operations are complete, execute the update operations
        futures = [executor.submit(update_bot_info, user_id, bot['nickname'], bot['faceURL'], token_dict["admin_token"])
                   for user_id, bot in robot_dict.items()]

        # Wait for all update operations to complete
        for future in as_completed(futures):
            try:
                result = future.result()
            except Exception as e:
                logger.error(f'update_bot_info generated an exception: {e}')

    logger.info("All bot info has been uploaded and updated.")


load_bot_config(BOT_CONFIG_PATH)
upload_bot_info()
