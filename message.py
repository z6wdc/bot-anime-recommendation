template_messages = {
    "type": "carousel",
    "contents": []
}

content_bubble =  {
    "type": "bubble",
    "hero": {
        "type": "image",
        "size": "full",
        "aspectMode": "fit",
        "url": "https://cdn.myanimelist.net/images/anime/1899/117237.jpg"
    },
    "body": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "text",
                "text": "ANIME TITLE",
                "wrap": true,
                "weight": "bold",
                "size": "xl"
            }
        ],
        "alignItems": "center"
    },
    "footer": {
        "type": "box",
        "layout": "vertical",
        "spacing": "sm",
        "contents": [
            {
                "type": "button",
                "action": {
                    "type": "uri",
                    "label": "more info",
                    "uri": "https://myanimelist.net/anime/48926/"
                }
            }
        ]
    }
}
