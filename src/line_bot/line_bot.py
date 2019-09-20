from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

channel_token = ""
receivers = []

line_bot_api = LineBotApi(channel_token)

def pushMessage(message):
    try:
      for receiver in receivers:
        line_bot_api.push_message(receiver, TextSendMessage(text=message))
        print("success")
    except LineBotApiError as e:
        print(e)