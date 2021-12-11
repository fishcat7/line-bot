from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('QAg3loNXvq5W+ph3Yrwr7c1x/QMZO7H1hFNZVUp/eG0oMprvcnak/Q9bq1Pw450PplFMQQzSSubJHgX8zgzdoLVJsXZDEaStUIv6YENz9ZbEyBNdp0yykRzmZzalPwC2ekGKLvuMC62M++f/bMKZoAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0a11fa447a0407f81cb405a2e5026b4d')


@app.route("/callback", methods=['POST'])
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
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()