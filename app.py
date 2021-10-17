from flask import Flask, request, abort
import os
import re
import copy
import json
import pickle
import pandas as pd

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, StickerMessage, StickerSendMessage
)

from message import create_messages

app = Flask(__name__)

#環境変数取得
CHANNEL_ACCESS_TOKEN = os.environ["CHANNEL_ACCESS_TOKEN"]
CHANNEL_SECRET = os.environ["CHANNEL_SECRET"]

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

usecols = ['Name', 'Japanese name', 'Score']
anime = pd.read_csv('data/anime.csv', usecols=usecols)
anime['Score'] = anime['Score'].replace('Unknown', 0).astype(float)

anime_image = pd.read_csv('data/anime_image.csv')

pkl_file = open('data/anime_indices.pkl', 'rb')
indices = pickle.load(pkl_file)

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

@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker_message(event):
    line_bot_api.reply_message(
        event.reply_token, 
        StickerSendMessage(package_id=event.message.package_id, sticker_id=event.message.sticker_id)
    )

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text
    result = re.match('TOP(\d+)', text, re.IGNORECASE)

    if result:
        n = int(result.group(1))
        if n > 100:
            n = 100
        top_n = anime.sort_values('Score', ascending=False).head(n)
        titles = ''
        for row in enumerate(top_n['Japanese name']):
            titles += f"{row[1]}, "

        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=f"アニメTOP{n}"),
                TextSendMessage(text=titles)
            ]
        )        
    else:
        query1 = anime['Japanese name'].str.contains(text, case=False)
        query2 = anime['Name'].str.contains(text, case=False)
        anime_index = anime[query1 | query2].head(1).index

        if anime_index.empty:
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text='見当たらない'),
                    StickerSendMessage(package_id='6136', sticker_id='10551393')
                ]
            )
        else:
            titles = ''
            contents = []
            for i, number in enumerate(indices[anime_index][0][:6]):
                if i == 0:
                    target = f"「{anime.at[number, 'Japanese name']}」をご覧になったあなたへ"
                    continue
                message = {}
                title = anime.at[number, 'Japanese name']
                message['title'] = title
                id = anime_image.at[number, 'MAL_ID']
                message['button_uri'] = f'https://myanimelist.net/anime/{id}'
                message['image_url'] = anime_image.at[number, 'IMAGE_URL']
                contents.append(message)

                titles += f"{title}, "
                
            line_bot_api.reply_message(
                event.reply_token, [
                    TextSendMessage(text=target),
                    FlexSendMessage(alt_text=titles, contents=create_messages(contents))
                ]
            )

if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT"))
    app.run(host="0.0.0.0", port=port)
