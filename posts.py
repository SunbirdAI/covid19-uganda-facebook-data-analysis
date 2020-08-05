from decouple import config
import requests

api_token = config('CROWDTANGLE_API_TOKEN')

import pymongo
db_client = pymongo.MongoClient()
pages_db = db_client["fbpages"]
col = pages_db["posts"]

url = f'https://api.crowdtangle.com/posts?token={api_token}'
posts_data = requests.get(url)
posts_data.text

col.insert_many(posts_data)