from decouple import config
import requests
from db_utils import get_db_collection

# TO DO
# Refactor file and extract common functionality
# into a separate module


def fetch_posts(api_token, url):
    params = {
        "count": '100',
        "startDate": '2020-07-02T16:00:00',
        "endDate": '2020-07-03T08:00:00',
        "searchTerm": 'covid-19, covid19',
        "token": api_token
    }

    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        print('GET /posts/ {}'.format(resp.status_code))
        pass

    data = resp.json()
    all_posts = data['result']['posts']

    while 'nextPage' in data['result']['pagination']:
        next_page = data['result']['pagination']['nextPage']
        print(f'Loading page ... {next_page}')
        resp = requests.get(next_page)
        if resp.status_code != 200:
            print('GET /posts/ {}'.format(resp.status_code))
            break
        data = resp.json()
        all_posts.append(data['result']['posts'])
        next_page = data['result']['pagination']['nextPage']

    return all_posts


if __name__ == '__main__':
    api_token = config('CROWDTANGLE_API_TOKEN')
    db = config('DB_NAME')
    col = config('COVID_DB_COLLECTION_NAME')
    posts_collection = get_db_collection(db, col)
    url = config('POSTS_SEARCH_URL')
    posts = fetch_posts(api_token, url)
    posts_collection.insert_many(posts)
