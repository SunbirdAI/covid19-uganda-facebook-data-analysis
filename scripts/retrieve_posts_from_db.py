from decouple import config
from utils import get_db_collection


def retrieve_posts(collection, query={}):
    posts = collection.find(query)
    return posts


if __name__ == '__main__':
    db = config('DB_NAME')
    col = config('MOH_DB_COLLECTION_NAME')
    posts_collection = get_db_collection(db, col)
    posts = retrieve_posts(posts_collection)
    print(posts.collection)
