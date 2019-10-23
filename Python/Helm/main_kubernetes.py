import requests
import math

'''
for more infos about the github api: https://developer.github.com/v3/
'''

API_KEY = '741eb4f12ce9d6cb13e319356b9d1da6d4893e56'
session = requests.Session()
session.auth = ('bugii', API_KEY)

res = session.get('https://api.github.com/search/code',
                  params={'q': 'filename:docker-compose.yml',
                          'sort': 'stars',
                          'order': 'desc'})

if res.status_code != 200:
    print('Something went wrong', res.status_code)

res_json = res.json()

total_repos = res_json['total_count']

# Calculate how many pages there are if 100 pages per page are requests (current max)
pages = math.ceil(total_repos/100)

print(pages)
print(res_json)

for i in res_json['items']:
    repo_url = i['html_url']
    print(repo_url)






