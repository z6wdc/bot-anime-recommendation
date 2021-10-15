import time
import requests
import pandas as pd
from bs4 import BeautifulSoup

data = []
count = 0

def get_image_url(x):

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }    

    global count
    count += 1
    print(count)
    print(f"To find {x['Name']}'s icon")

    url = f'https://myanimelist.net/anime/{x["MAL_ID"]}/'
    try:
        res = requests.get(url, headers=headers, timeout=(3.0, 7.5))
        soup = BeautifulSoup(res.text, 'lxml')
        element = soup.find('meta', attrs={'property': 'og:image'})
        x["IMAGE_URL"] = element.get('content')
        print(x["IMAGE_URL"])
        print('found it')
        time.sleep(3)
    except Exception as e:
        print(e)
        time.sleep(120)

    print('\n')
    return x

df = pd.read_csv('data/anime_image.csv')

query = df['IMAGE_URL'].str.startswith('http')
df_sample = df[~query]
print(df_sample.head())
print(df_sample.shape)
df_sample = df_sample.apply(get_image_url, axis=1)

numbers = list(df_sample['MAL_ID'])
for number in numbers:
    df[df['MAL_ID'] == number] = df_sample[df_sample['MAL_ID'] == number]

df.to_csv("data/anime_image.csv", index=False)
