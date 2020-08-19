from decouple import config
import requests
import pymongo

api_token = config('CROWDTANGLE_API_TOKEN')
group_list = config('GROUP_LIST_ID')

db_client = pymongo.MongoClient()
posts_db = db_client["fbposts"]
col = posts_db["posts"]

payload = {
    'token': api_token, 'listIds': group_list,
    'startDate': '2020-03-01', 'sortBy': 'date',
    'count': 99
}
url = 'https://api.crowdtangle.com/posts'
posts_data = requests.get(url, params=payload)
posts = posts_data.json()['result']['posts']

post_text_list = []
for post in posts:
    text = post.get('message', '')
    post_text_list.append({'text': text})

col.insert_many(post_text_list)
print(len(post_text_list))
