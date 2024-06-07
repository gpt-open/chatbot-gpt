from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import os
import time
from typing import List, Dict, Any
import py3langid as langid
import requests
from unionllm import unionchat
from server.app.bot_config import get_bot_setting
from server.app.utils.diskcache_client import diskcache_client
from server.logger.logger_config import my_logger as logger


SEND_MSG_URL = os.getenv('SEND_MSG_URL')
MAX_HISTORY_SESSION_LENGTH = int(os.getenv('MAX_HISTORY_SESSION_LENGTH'))
SESSION_EXPIRE_SECONDS = int(os.getenv('SESSION_EXPIRE_SECONDS'))


def detect_query_lang(query: str) -> str:
    # Dictionary to map language codes to full language names
    lang_map = {
        'en': 'English',
        'zh': 'Chinese',
        'fr': 'French',
        'es': 'Spanish',
        'pt': 'Portuguese',
        'de': 'German',
        'ru': 'Russian',
        'ja': 'Japanese',
        'ko': 'Korean',
        'hi': 'Hindi',
        'ar': 'Arabic'
    }

    # Detect the language of the query
    lang, _ = langid.classify(query)

    # Get the full language name
    full_language = lang_map.get(lang, 'English')
    return full_language


def llm_generate_content(query: str, bot: Dict[str, Any], history_context: str) -> str:
    content = ''
    try:
        lang = detect_query_lang(query)
        api_key = bot["apiKey"]
        model = bot["model"]
        llmname = bot["llmname"]
        prompt = f"""You are a smart customer service assistant and problem-solver, tasked to answer any question.
Given a conversation (between Human and Assistant), answer the user's question to the best of your ability using the resources provided.

Chat History:
{history_context}

**Question:** {query}

**NOTE:** The detected language of the Input is '{lang}'. Please respond in '{lang}'.

The answer is:"""
        #logger.info(f"prompt is:\n{prompt}")

        beg_time = time.time()
        ret = unionchat(api_key=api_key, provider=llmname.lower(), model=model, messages=[{"content": prompt, "role": "user"}], stream=False)
        timecost = time.time() - beg_time
        logger.warning(f"For the query: '{query}', llmname: '{llmname}', model: '{model}', timecost is {timecost}")
        if ret:
            content = ret.choices[0].message.content
            logger.success(f"For the query: '{query}', llmname: '{llmname}', model: '{model}', the answer is '{content}'")
    except Exception as e:
        logger.error(f"llm_generate_content is failed, excpetion:{e}")
    return content


def get_single_msg_history(send_id: str, recv_id: str) -> List[Any]:
    try:
        history_key = f"open_chatbot:single_msg_history:{send_id}:{recv_id}"
        history_items = diskcache_client.get_list(history_key)
        history = [json.loads(item) for item in history_items]
        return history
    except Exception as e:
        logger.error(f"For hisotry_key: '{history_key}', get_single_msg_history is failed! exception: {e}")
        return []


def save_single_msg_history(send_id: str, recv_id: str, query: str, answer: str) -> None:
    try:
        history_key = f"open_chatbot:single_msg_history:{send_id}:{recv_id}"
        history_data = {
            "query": query,
            "answer": answer
        }
        diskcache_client.append_to_list(history_key, json.dumps(history_data), ttl=SESSION_EXPIRE_SECONDS, max_length=MAX_HISTORY_SESSION_LENGTH)
    except Exception as e:
        logger.error(f"For hisotry_key: '{history_key}', save_single_msg_history is failed! exception: {e}")


def send_single_msg_to_im(send_id: str, recv_id: str, query: str, bot: Dict[str, Any], im_token: str) -> None:
    history_context = ''
    history = get_single_msg_history(send_id, recv_id)
    if history:
        history_context = "\n--------------------\n".join([
            f"**Human:** {item['query']}\n**Assistant:** {item['answer']}"
            for item in history
        ])

    llm_content = llm_generate_content(query, bot, history_context)
    if not llm_content:
        logger.error(f"[send_single_msg_to_im] For the query: '{query}', the llm_content is empty! bot is {bot}")
        return None

    save_single_msg_history(send_id, recv_id, query, llm_content)

    try:
        url = SEND_MSG_URL
        payload = json.dumps({
           "sendID": send_id,
           "recvID": recv_id,
           "groupID": "",
           "senderNickname": bot["nickname"],
           "senderFaceURL": bot["faceURL"],
           "senderPlatformID": 10,
           "content": {
              "content": llm_content
           },
           "contentType": 101,
           "sessionType": 1,
           "isOnlineOnly": False,
           "notOfflinePush": False,
           "offlinePushInfo": {
              "title": "you have a new message",
              "desc": "you have a new message",
              "ex": "",
              "iOSPushSound": "default",
              "iOSBadgeCount": True
           }
        })
        headers = {
           'OperationID': '123',
           'token': im_token,
           'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload)
    except Exception as e:
        logger.error(f"send_single_msg_to_im is failed, send_id: '{send_id}', excpetion: {e}")


def get_group_msg_history(send_id: str, group_id: str) -> List[Any]:
    try:
        history_key = f"open_chatbot:single_group_history:{send_id}:{group_id}"
        history_items = diskcache_client.get_list(history_key)
        history = [json.loads(item) for item in history_items]
        return history
    except Exception as e:
        logger.error(f"For hisotry_key: '{history_key}', get_group_msg_history is failed! exception: {e}")
        return []


def save_group_msg_history(send_id: str, group_id: str, query: str, answer: str) -> None:
    try:
        history_key = f"open_chatbot:single_group_history:{send_id}:{group_id}"
        history_data = {
            "query": query,
            "answer": answer
        }
        diskcache_client.append_to_list(history_key, json.dumps(history_data), ttl=SESSION_EXPIRE_SECONDS, max_length=MAX_HISTORY_SESSION_LENGTH)
    except Exception as e:
        logger.error(f"For hisotry_key: '{history_key}', save_group_msg_history is failed! exception: {e}")


def send_group_msg_to_im(sender_nickname: str, origin_send_id: str, user_list: List[str], group_id: str, query: str, im_token) -> None:
    robot_dict = get_bot_setting()
    logger.warning(f"user_list: {user_list}, origin_send_id: {origin_send_id}")

    def _process_user(user_id):
        if user_id not in robot_dict:
            logger.warning(f"user_id: '{user_id}' is not in {robot_dict}")
            return

        bot = robot_dict[user_id]
        logger.info(f"For the query: '{query}', bot is {bot}")

        history_context = ''
        history = get_group_msg_history(user_id, group_id)
        if history:
            history_context = "\n--------------------\n".join([
                f"**Human:** {item['query']}\n**Assistant:** {item['answer']}"
                for item in history
            ])

        llm_content = llm_generate_content(query, bot, history_context)
        if not llm_content:
            logger.warning(f"[send_group_msg_to_im] For the query: '{query}', the llm_content is empty!, bot is {bot}")
            return

        save_group_msg_history(user_id, group_id, query, llm_content)

        try:
            url = SEND_MSG_URL
            payload = json.dumps({
                "sendID": user_id,
                "recvID": "",
                "groupID": group_id,
                "senderNickname": bot["nickname"],
                "senderFaceURL": bot["faceURL"],
                "senderPlatformID": 10,
                "content": {
                    "text": f"@{origin_send_id} {llm_content}",
                    "atUserList": [origin_send_id],
                    "atUsersInfo": [
                        {
                            "atUserID": origin_send_id,
                            "groupNickname": sender_nickname
                        }
                    ],
                    "isAtSelf": False
                },
                "contentType": 106,
                "sessionType": 3,
                "isOnlineOnly": False,
                "notOfflinePush": False,
                "offlinePushInfo": {
                    "title": "you have a new message",
                    "desc": "you have a new message",
                    "ex": "",
                    "iOSPushSound": "default",
                    "iOSBadgeCount": True
                }
            })
            headers = {
               'OperationID': '123',
               'token': im_token,
               'Content-Type': 'application/json'
            }
            response = requests.request("POST", url, headers=headers, data=payload)
        except Exception as e:
            logger.error(f"send_group_msg_to_im failed for user_id: '{user_id}', exception: {e}")

    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(_process_user, user_id): user_id for user_id in user_list}
        for future in as_completed(futures):
            user_id = futures[future]
            try:
                future.result()
            except Exception as e:
                logger.error(f"Exception for user_id: '{user_id}', exception: {e}")
