from flask import Flask, request
import json
import os
import requests

app = Flask(__name__)  # Initialize Flask application

# GitHub webhook handler
@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json  # Parse JSON payload from GitHub
    print(f"Received GitHub webhook: {data}")  # Debugging line
    if 'commits' in data:
        for commit in data['commits']:
            # Format the commit message
            message = f"New commit by {commit['author']['name']}: {commit['message']}\n{commit['url']}"
            send_discord_notification(message)  # Send the notification to Discord
    return 'OK', 200

# Test endpoint to manually send a test message
@app.route('/test', methods=['GET'])
def test():
    message = "Test message from server"
    send_discord_notification(message)
    return 'Test message sent', 200

# Function to send a notification to the Discord bot
def send_discord_notification(message):
    url = 'http://localhost:8080/send-message'  # URL of the Discord bot's AIOHTTP server
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'message': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))  # Send POST request to the bot
    if response.status_code != 200:
        print(f"Request failed: {response.status_code}, {response.text}")  # Debugging line
        raise Exception(f"Request failed: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(port=5000)  # Run the Flask server on port 5000
