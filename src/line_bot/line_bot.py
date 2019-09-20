from linebot import LineBotApi
from linebot.models import TextSendMessage
from linebot.exceptions import LineBotApiError

channel_token = "FgRzCbM/VsbxtRoGtRAUpykdJIMnV1UWeRkPqrdY3t5LQjOGI+4tXdIPao5HZufyrq24ZmlnzzS66Evhev9AZOCe2qIKZIxH+k4WJWnqo+Xm18ZR8LENzpBsKwGYJDZhkK+CE/ZTbJoQxI4jwRH6RQdB04t89/1O/w1cDnyilFU="
receivers = []

line_bot_api = LineBotApi(channel_token)

def pushMessage(message):
    try:
      for receiver in receivers:
        line_bot_api.push_message(receiver, TextSendMessage(text=message))
        print("success")
    except LineBotApiError as e:
        print(e)