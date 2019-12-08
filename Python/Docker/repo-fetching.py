import pickle
import shutil
import tarfile
import time
import os
import requests
import wget
from datetime import datetime

from project import Project

'''
for more infos about the github api: https://developer.github.com/v3/
'''

repos_to_fetch = 1000
per_page = 100
pages_to_query = int(repos_to_fetch / per_page)

API_KEY = '741eb4f12ce9d6cb13e319356b9d1da6d4893e56'
session = requests.Session()
session.auth = ('bugii', API_KEY)


def get_stats(repo):
    res = session.get(repo + "/stats/contributors")
    if res.status_code == 200:
        res_json = res.json()
        contributors = 0
        commits = 0
        for contributor in res_json:
            contributors += 1
            commits += contributor['total']
        print('got stats for', repo)
        return contributors, commits

    elif res.status_code == 202:
        time.sleep(10)
        return get_stats(repo)

    print('failed for', repo)
    return -1, -1


def search_github():
    '''
    Do 5 different queries based on different file sizes
    '''

    sizes = ["1..2000", "2001..4000", "4001..6000", "6001..8000", "8001..10000"]

    for size in sizes:
        print('size interval:', size)
        print('-----------------------------')

        for page in range(1, pages_to_query + 1):
            print('page:', page)
            print('-----------------------------')

            res = session.get('https://api.github.com/search/code',
                              params={'q': 'path:/ filename:docker-compose.yml size:' + size,
                                      'sort': 'stars',
                                      'order': 'desc',
                                      'per_page': per_page,
                                      'page': page})

            if res.status_code != 200:
                print('Something went wrong', res.status_code)

            res_json = res.json()

            for i in res_json['items']:
                time.sleep(5)

                repo_url = i['repository']['url']

                # get the latest update date
                repo = session.get(repo_url).json()
                last_updated_at = datetime.fromisoformat(repo['updated_at'][:-1])
                name = repo['full_name']
                print(name)
                print('url:', repo_url)

                # get the creation date of the project
                created_at = datetime.fromisoformat(repo['created_at'][:-1])

                # get the most used language
                language = repo['language']
                print('lang:', language)

                # get the contributors
                contributors, commits = get_stats(repo_url)
                print('contributors:', contributors)
                print('commits:', commits)
                print('-----------------------------')

                # create object
                project = Project(name=name, url=repo_url, created=created_at, last_updated=last_updated_at,
                                  language=language, contributors=contributors, commits=commits)

                # download the repo and unzip it, delete compressed file afterwards
                archive_path = wget.download(repo_url + '/tarball', 'repositories')
                folder_name = archive_path[:-7]
                tarfile.open(archive_path).extractall(folder_name)
                os.remove(archive_path)

                # save project object inside the folder
                with open(folder_name + '/project.pkl', 'wb') as f:
                    pickle.dump(project, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':

    if not os.path.exists('repositories'):
        os.mkdir('repositories')

    search_github()
