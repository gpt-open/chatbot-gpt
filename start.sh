#!/bin/bash

python upload_bot_config.py

gunicorn -c gunicorn_config.py chatbot_app:app
