from decouple import config
import requests
from utils import get_db_collection


def fetch_posts(api_token, url):
    params = {
        'token': api_token,
        'listIds': group_list,
        'startDate': '2020-11-15',
        'sortBy': 'date',
        'count': 99
    }

    posts_data = requests.get(url, params=params)
    posts = posts_data.json()['result']['posts']

    posts_text = []
    for post in posts:
        text = post.get('message', '')
        posts_text.append({'text': text})
    return posts_text


def insert_posts_in_db(posts, db_name, collection_name):
    posts_collection = get_db_collection(db_name, collection_name)
    posts_collection.insert_many(posts)


if __name__ == '__main__':
    api_token = config('CROWDTANGLE_API_TOKEN')
    group_list = config('MOH_GROUP_LIST_ID')
    db = config('DB_NAME')
    col = config('MOH_DB_COLLECTION_NAME')
    url = 'https://api.crowdtangle.com/posts'
    posts = fetch_posts(api_token, url)
    insert_posts_in_db(posts, db, col)
