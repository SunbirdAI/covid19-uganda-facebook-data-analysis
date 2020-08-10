from decouple import config
import requests
import pymongo

api_token = config('CROWDTANGLE_API_TOKEN')
group_list = config('GROUP_LIST_ID')

db_client = pymongo.MongoClient()
posts_db = db_client["fbposts"]
col = posts_db["posts"]

payload = {'token': api_token, 'listIds': group_list}
url = 'https://api.crowdtangle.com/posts'
posts_data = requests.get(url, params=payload)
posts = posts_data.json()['result']

col.insert_many(posts['posts'])
