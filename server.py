# server.py
from flask import Flask, request
import json
import requests
import os
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

@app.route('/github-webhook', methods=['POST'])
def github_webhook():
    data = request.json
    if 'commits' in data:
        for commit in data['commits']:
            message = f"New commit by {commit['author']['name']}: {commit['message']}\n{commit['url']}"
            send_discord_notification(message)
    return 'OK', 200

def send_discord_notification(message):
    data = {
        "content": message
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, data=json.dumps(data), headers=headers)
    if response.status_code != 204:
        raise Exception(f"Request failed: {response.status_code}, {response.text}")

if __name__ == '__main__':
    app.run(port=5000)
