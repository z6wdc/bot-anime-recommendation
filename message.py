import copy

def create_content(image_url, title, button_uri):
    content_bubble = {
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
                    "wrap": True,
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

    content_bubble['hero']['url'] = image_url
    content_bubble['body']['contents'][0]['text'] = title
    content_bubble['footer']['contents'][0]['action']['uri'] = button_uri

    return content_bubble

def create_messages(message_list):
    template_messages = {
        'type': 'carousel',
        'contents': []
    }
    
    for message in message_list:
        content = create_content(message['image_url'], message['title'], message['button_uri'])
        template_messages['contents'].append(content)

    return template_messages
