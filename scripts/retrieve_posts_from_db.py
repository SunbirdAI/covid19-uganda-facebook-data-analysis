import pymongo

db_client = pymongo.MongoClient()
posts_db = db_client["fbposts"]
col = posts_db["covid-posts"]
