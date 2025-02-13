from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage

app = Flask(__name__)

# 在這裡填入你的 LINE Bot 的 Channel Access Token 和 Channel Secret
LINE_CHANNEL_ACCESS_TOKEN = '你的 Channel Access Token'
LINE_CHANNEL_SECRET = '你的 Channel Secret'

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
line_handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 用來接收 webhook 事件的路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        # 驗證並處理 webhook 事件
        line_handler.handle(body, signature)
    except Exception as e:
        abort(400)

    return 'OK'

# 設定處理訊息事件的邏輯
@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # 回應使用者發送的文字訊息
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=f"你發送的訊息是: {event.message.text}")
    )

if __name__ == "__main__":
    app.run(port=5000)
