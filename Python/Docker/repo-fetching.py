import tarfile
import time
import os
import requests
import wget

from analysis import run_analysis

'''
for more infos about the github api: https://developer.github.com/v3/
'''

API_KEY = '741eb4f12ce9d6cb13e319356b9d1da6d4893e56'
session = requests.Session()
session.auth = ('bugii', API_KEY)

res = session.get('https://api.github.com/search/code',
                  params={'q': 'path:/ filename:docker-compose.yml',
                          'sort': 'stars',
                          'order': 'desc',
                          'per_page': '100'})

if res.status_code != 200:
    print('Something went wrong', res.status_code)

res_json = res.json()
total_repos = res_json['total_count']
print('Found:', total_repos)

'''
Here would be the loop to get all pages
Only do 100 repos to test for now
'''

for i in res_json['items']:
    time.sleep(5)
    repo_url = i['repository']['url']
    # download the repo and unzip it, delete compressed file afterwards
    archive_path = wget.download(repo_url + '/tarball', 'repositories')
    tarfile.open(archive_path).extractall('repositories/')
    os.remove(archive_path)

    # TODO: in order to save disk space, run analysis here and delete repos afterwards
    run_analysis(archive_path[:-7])
