import os
from flask import Flask, request
from pymessenger.bot import Bot

app = Flask(__name__)
PAGE_ACCESS_TOKEN = os.environ['PAGE_ACCESS_TOKEN']
VERIFY_TOKEN = 'testing'
bot = Bot(PAGE_ACCESS_TOKEN)

@app.route('/', methods=['GET'])
def verify_token():
    request_data = request.args.to_dict()
    if request_data.get('hub.mode') == 'subscribe' and request_data.get('hub.challenge'):
        if not request_data.get("hub.verify_token") == VERIFY_TOKEN:
            return "Token Mismatch", 403
        return request_data['hub.challenge'], 200

@app.route('/', methods=['POST'])
def webhook():
    request_data = request.get_json(force=True)
    if request_data["object"] == "page":
        for entry in request_data["entry"]:
             for messaging in entry["messaging"]:
                 # Someone sends you the message
                 if messaging.get("message"):
                     # Recipient Id
                     recipient_id = messaging["sender"]["id"]
                     if messaging['message'].get('text'):
                         send_text = "Hey !! This is Kasam"
                         # Sending message to Recipient
                         bot.send_text_message(recipient_id, send_text)

    return "ok", 200

if __name__ == '__main__':
    app.run(debug=True)
