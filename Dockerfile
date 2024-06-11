# Use an official Python runtime as a parent image, specifically the slim version to keep the image size down
FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod a+x start.sh

# Make port 9000 available to the world outside this container
EXPOSE 9000

# Define the command to run on container start. This script starts the Flask application.
CMD ["./start.sh"]
