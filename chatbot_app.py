from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(override=True)
from server.constant.env_constants import check_env_variables
check_env_variables()

import json
import os
import re
from threading import Thread
from flask import Flask, request, send_from_directory, abort
from flask_cors import CORS
from werkzeug.utils import safe_join
from server.app.bot_config import get_bot_setting
from server.app.queries import send_single_msg_to_im, send_group_msg_to_im
from server.app.token_config import get_token_setting
from server.constant.constants import CONTENT_TYPE_TEXT, CONTENT_TYPE_AT, CONTENT_TYPE_QUOTE, STATIC_DIR
from server.logger.logger_config import my_logger as logger


app = Flask(__name__, static_folder=STATIC_DIR)
CORS(app)


"""
Background:
In scenarios where using a dedicated static file server (like Nginx) is not feasible or desired, Flask can be configured to serve static files directly. This setup is particularly useful during development or in lightweight production environments where simplicity is preferred over the scalability provided by dedicated static file servers.

This Flask application demonstrates how to serve:
- The homepages and assets for two single-page applications (SPAs)

Note:
While Flask is capable of serving static files, it's not optimized for the high performance and efficiency of a dedicated static file server like Nginx, especially under heavy load. For large-scale production use cases, deploying a dedicated static file server is recommended.

The provided routes include a dynamic route for serving files from a specified media directory and specific routes for SPA entry points and assets. This configuration ensures that SPA routing works correctly without a separate web server.
"""
@app.route(f'/<path:filename>')
def serve_media_file(filename):
    # Use safe_join to securely combine the static folder path and filename
    file_path = safe_join(app.static_folder, filename)

    # Check if the file exists and serve it if so
    if os.path.exists(file_path) and os.path.isfile(file_path):
        return send_from_directory(app.static_folder, filename)
    else:
        # Return a 404 error if the file does not exist
        return abort(404)


@app.route('/open_chatbot/get_bot_list', methods=['POST'])
def get_bot_list():
    robot_dict = get_bot_setting()
    bot_list = []
    try:
        for user_id in robot_dict:
            bot = robot_dict[user_id]
            bot_list.append({
                "userID": user_id,
                "nickname": bot["nickname"],
                "faceURL": bot["faceURL"],
                "email": f"{user_id}@gpt.com",
                "llmname": bot["llmname"],
                "model": bot["model"]
            })
    except Exception as e:
        logger.error(f"[get_bot_list] is failed, excpetion:{e}")

    return {
        "retcode": 0,
        "message": "success",
        "data": {
            "bot_list": bot_list
        }
    }


@app.route('/open_chatbot/callbackAfterSendSingleMsgCommand', methods=['POST'])
def callbackAfterSendSingleMsgCommand():
    robot_dict = get_bot_setting()
    token_dict = get_token_setting()

    try:
        data = request.json
        sendID = data["sendID"]
        recvID = data["recvID"]
        content = data["content"]
        contentType = data["contentType"]
        if recvID in robot_dict and contentType in [CONTENT_TYPE_TEXT, CONTENT_TYPE_QUOTE]:
            content_json = json.loads(content)
            if contentType == 101:
                query = content_json["content"]
            else:
                query = content_json["text"]
                if "quoteMessage" in content_json:
                    if "textElem" in content_json["quoteMessage"]:
                        text_elem = content_json["quoteMessage"]["textElem"]["content"]
                        query = f"{query}\t{text_elem}"

            bot = robot_dict[recvID]
            logger.info(f"[callbackAfterSendSingleMsgCommand] recv a msg from sendID: '{sendID}', the recvID is '{recvID}', content: {content}, contentType: {contentType}, query: '{query}', bot is {bot}")

            # Start another new thread to send_single_msg_to_im asynchronously
            Thread(target=send_single_msg_to_im, args=(recvID, sendID, query, bot, token_dict["im_token"])).start()
    except Exception as e:
        logger.error(f"[callbackAfterSendSingleMsgCommand] is failed, excpetion:{e}")

    return {
        "actionCode": 0,
        "errCode": 0,
        "errMsg": "",
        "errDlt": ""
    }


def clean_message(message: str) -> str:
    """
    Remove @robot tags and preceding content, including non-text characters, from a message.

    Parameters:
    message (str): The input message containing @robot tags and text.

    Returns:
    str: The cleaned message with @robot tags and preceding content removed.
    """
    # Use a regular expression to remove @robot tags and preceding content, including non-text characters
    cleaned_msg = re.sub(r'(@\S+\s*[,.!，。、！]*)+', '', message).strip()
    return cleaned_msg


@app.route('/open_chatbot/callbackAfterSendGroupMsgCommand', methods=['POST'])
def callbackAfterSendGroupMsgCommand():
    robot_dict = get_bot_setting()
    token_dict = get_token_setting()

    try:
        data = request.json
        sendID = data["sendID"]
        senderNickname = data["senderNickname"]
        groupID = data["groupID"]
        atUserList = data["atUserList"]
        content = data["content"]
        contentType = data["contentType"]
        if atUserList and contentType in [CONTENT_TYPE_AT]:
            content_json = json.loads(content)
            query = content_json["text"]
            for at_user in atUserList:
                at_str = f"@{at_user}"
                if query.find(at_str) != -1:
                    query = clean_message(query)
                    break

            if "quoteMessage" in content_json:
                if "textElem" in content_json["quoteMessage"]:
                    text_elem = content_json["quoteMessage"]["textElem"]["content"]
                    query = f"{query}\t{text_elem}"

            logger.info(f"[callbackAfterSendGroupMsgCommand] recv a msg from groupID: '{groupID}', sendID: '{sendID}', atUserList: {atUserList}, content: {content}, contentType: {contentType}, query: '{query}'")

            # Start another new thread to send_group_msg_to_im asynchronously
            Thread(target=send_group_msg_to_im, args=(senderNickname, sendID, atUserList, groupID, query, token_dict["im_token"])).start()
    except Exception as e:
        logger.error(f"[callbackAfterSendGroupMsgCommand] is failed, excpetion:{e}")

    return {
        "actionCode": 0,
        "errCode": 0,
        "errMsg": "Success",
        "errDlt": "",
        "nextCode": ""
    }


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=9000)
