from flask import Flask, request, abort
import os
import copy
import json
import pickle
import pandas as pd
import message_template

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FlexSendMessage
)

app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

usecols = ['Name', 'Japanese name', 'Score']
anime = pd.read_csv('data/anime.csv', usecols=usecols)
anime['Score'] = anime['Score'].replace('Unknown', 0).astype(float)

pkl_file = open('data/anime_indices.pkl', 'rb')
indices = pickle.load(pkl_file)

def search_anime(keyword):
    query1 = anime['Japanese name'].str.contains(keyword)
    query2 = anime['Name'].str.contains(keyword)
    return anime[query1 | query2].head(1).index

@app.route("/")
def hello_world():
    return "おすすめアニメ"

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
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text

    if 'TOP' in text:
        n = text.split()[-1]
        top_n = anime.sort_values('Score', ascending=False).head(int(n))
        titles = ''
        for row in enumerate(top_n['Japanese name']):
            titles += f"{row[1]},"

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=titles)
        )        
    else:
        query1 = anime['Japanese name'].str.contains(text)
        query2 = anime['Name'].str.contains(text)
        anime_index = anime[query1 | query2].head(1).index

        titles = ''
        for i, number in enumerate(indices[anime_index][0]):
            if i == 0:
                target = f"「{anime.loc[number]['Japanese name']}」をご覧になったあなたへ"
                continue
            titles += f"{anime.loc[number]['Japanese name']},"

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=target),
                TextSendMessage(text=titles)
            ]
        )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
