from decouple import config
import requests
import pymongo

db_client = pymongo.MongoClient()
posts_db = db_client["fbposts"]
col = posts_db["covid-posts"]

api_token = config('CROWDTANGLE_API_TOKEN')

params = {
    "count": '100',
    "startDate": '2020-07-02T16:00:00',
    "endDate": '2020-07-03T08:00:00',
    "searchTerm": 'covid-19, covid19',
    "token": api_token
}

url = 'https://api.crowdtangle.com/posts/search'

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
