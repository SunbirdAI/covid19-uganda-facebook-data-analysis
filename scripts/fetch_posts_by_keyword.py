from decouple import config
import requests
import pandas as pd
# import pymongo

api_token = config('CROWDTANGLE_API_TOKEN')

params = {
    "count": '100',
    "sortBy": 'interaction_rate',
    "startDate": '2020-07-02T16:00:00',
    "endDate": '2020-07-03T08:00:00',
    "searchTerm": 'covid-19, covid19',
    "token": api_token
}

url = 'https://api.crowdtangle.com/posts/search'

keep_columns = [
                'id', 'platform', 'date', 'account.url',
                'statistics.actual.likeCount', 'statistics.actual.shareCount',
                'statistics.actual.loveCount', 'statistics.actual.wowCount',
                'statistics.actual.hahaCount', 'statistics.actual.sadCount',
                'statistics.actual.angryCount',
                'statistics.actual.thankfulCount',
                'statistics.actual.careCount'
                ]
new_columns = [
               'id', 'platform', 'date', 'url', 'like', 'share', 'love', 'wow',
               'haha', 'sad', 'angry', 'thankful', 'care'
               ]

resp = requests.get(url, params=params)
if resp.status_code != 200:
    print('GET /posts/ {}'.format(resp.status_code))
    pass

data = resp.json()
full_df = pd.json_normalize(data['result']['posts'])
interaction_df = full_df[keep_columns].fillna(0)
interaction_df.columns = new_columns

while 'nextPage' in data['result']['pagination']:
    next_page = data['result']['pagination']['nextPage']
    print(f'Loading page ... {next_page}')
    resp = requests.get(next_page)
    if resp.status_code != 200:
        print('GET /posts/ {}'.format(resp.status_code))
        break
    data = resp.json()
    full_df = pd.json_normalize(data['result']['posts'])
    inc_df = full_df[keep_columns].fillna(0)
    inc_df.columns = new_columns
    interaction_df = interaction_df.append(inc_df, ignore_index=True)
    next_page = data['result']['pagination']['nextPage']
