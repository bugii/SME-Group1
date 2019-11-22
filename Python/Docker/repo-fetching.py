import pickle
import tarfile
import time
import os
import requests
import wget
from datetime import datetime

from analysis import run_analysis
from project import *

'''
for more infos about the github api: https://developer.github.com/v3/
'''

repos_to_fetch = 1000
per_page = 100
pages_to_query = int(repos_to_fetch / per_page)

API_KEY = '741eb4f12ce9d6cb13e319356b9d1da6d4893e56'
session = requests.Session()
session.auth = ('bugii', API_KEY)


def search_github(page):
    print('On page', page)
    '''
    Do 4 different queries based on different file sizes
    '''
    sizes = ["1..1000", "1001..2000", "2001..3000", "3001..4000", "5001..6000", "6001..7000", "7001..8000", "8001..9000", "9001..10000"]

    for size in sizes:
        print(size)

        res = session.get('https://api.github.com/search/code',
                          params={'q': 'path:/ filename:docker-compose.yml size:' + size,
                                  'sort': 'stars',
                                  'order': 'desc',
                                  'per_page': per_page,
                                  'page': page})

        if res.status_code != 200:
            print('Something went wrong', res.status_code)

        res_json = res.json()

        if page == 1:
            total_repos = res_json['total_count']
            print('Found:', total_repos)

        for i in res_json['items']:
            time.sleep(5)

            repo_url = i['repository']['url']
            print('Repo:', repo_url)

            # get the creation date of the project


            # get the latest update date
            repo = session.get(repo_url).json()
            last_updated_at = datetime.fromisoformat(repo['updated_at'][:-1])
            name = repo['full_name']

            # get the most used language

            # get the contributors

            # if language either python, java, c#, javascript, or go: run the following code

            # # create object
            # project = Project(name=name, url=repo_url, last_updated=last_updated_at)
            #
            # # download the repo and unzip it, delete compressed file afterwards
            # archive_path = wget.download(repo_url + '/tarball', 'repositories')
            # folder_name = archive_path[:-7]
            # tarfile.open(archive_path).extractall(folder_name)
            # os.remove(archive_path)
            #
            # # save project object inside the folder
            # with open(folder_name + '/project.pkl', 'wb') as f:
            #     pickle.dump(project, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    for page in range(1, pages_to_query + 1):
        search_github(page)
