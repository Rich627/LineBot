from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)

channel_access_token='/tZ2uEIDxOMNlXK74nW70LYdCAYdLh5B8zDV+x3car+f+v+IhcY65be0QrzUxHvPJnyliDupV+LsrG38uGDKxY0E9mpx0KaorhocDMm9OLVlNWHQ0TObJBam+dEvBbI8f61GdJ0PWKr8JvpHV9v7CwdB04t89/1O/w1cDnyilFU='
channel_secret = '1d2497c01a15d51f9550bf605b2c1fae'
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

# 修正translate_text()函數
def translate_text(source, target, text):
    translator = GoogleTranslator(source=source, target=target)
    return translator.translate(text)

@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    #if event.source.user_id == 'Udeadbeefdeadbeefdeadbeefdeadbeef':
        #return 'OK'
    if event.message.text[:3] == "@翻英":
        content = translate_text(source='zh-tw', target='en', text=event.message.text[3:])
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)
    if event.message.text[:3] == "@翻中":
        content = translate_text(source='en', target='zh-TW', text=event.message.text[3:])
        message = TextSendMessage(text=content)
        line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 
