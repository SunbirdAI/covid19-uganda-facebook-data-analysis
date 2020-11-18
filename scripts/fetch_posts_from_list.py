from decouple import config
import requests
from utils import get_db_collection


def fetch_posts():
    params = {
        'token': api_token, 'listIds': group_list,
        'startDate': '2020-03-01', 'sortBy': 'date',
        'count': 99
    }
    url = 'https://api.crowdtangle.com/posts'
    posts_data = requests.get(url, params=params)
    posts = posts_data.json()['result']['posts']

    posts_text = []
    for post in posts:
        text = post.get('message', '')
        posts_text.append({'text': text})
    return posts_text


def insert_posts_in_db(posts):
    posts_collection = get_db_collection('fb_posts', 'moh-posts')
    posts_collection.insert_many(posts)


if __name__ == '__main__':
    api_token = config('CROWDTANGLE_API_TOKEN')
    group_list = config('MOH_GROUP_LIST_ID')
    posts = fetch_posts()
    insert_posts_in_db(posts)
