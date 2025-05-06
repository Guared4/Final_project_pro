from flask import Flask, request
import logging
import requests
import os

app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    filename='/var/log/telegram_webhook.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        app.logger.error("Telegram token or chat_id is not set.")
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message
    }

    try:
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            app.logger.error(f"Telegram API error: {response.text}")
    except Exception as e:
        app.logger.error(f"Error sending message to Telegram: {e}")

@app.route('/', methods=['POST'])
def webhook():
    data = request.json
    app.logger.info(f"Received alert: {data}")
    send_telegram_message(f"Alert received:\n{data}")
    return '', 200

@app.route('/', methods=['GET'])
def index():
    return 'Webhook works!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
