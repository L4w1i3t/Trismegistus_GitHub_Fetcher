# server.py
from flask import Flask, request
import json
import os
import requests

app = Flask(__name__)

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    if 'commits' in data:
        for commit in data['commits']:
            message = f"New commit by {commit['author']['name']}: {commit['message']}\n{commit['url']}"
            send_discord_notification(message)
    return 'OK', 200

def send_discord_notification(message):
    url = 'http://localhost:8080/send-message'
    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        'message': message
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    if response.status_code != 200:
        raise Exception(f"Request failed: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(port=5000)
