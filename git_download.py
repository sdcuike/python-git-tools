import os
import subprocess
import sys
import requests
from requests import Response

PER_PAGE = 50
PRIVATE_TOKEN = ''
GIT_HOST = ''
HEADERS = {}
PATH = ''


def parse():
    print(sys.argv)
    global GIT_HOST
    global PRIVATE_TOKEN
    global HEADERS
    global PATH

    GIT_HOST = sys.argv[1]
    PRIVATE_TOKEN = sys.argv[2]
    HEADERS = {'PRIVATE-TOKEN': PRIVATE_TOKEN}
    PATH = sys.argv[3]
    print(GIT_HOST)
    print(HEADERS)
    print(PATH)


def get_project() -> set[str]:
    groups_url = "/".join([GIT_HOST, "api/v4/groups?per_page=50&page={pageNum}"])

    page = 1
    global HEADERS
    groups_ids = []

    while True:
        url = groups_url.format(pageNum=page)
        response: Response = requests.get(url, headers=HEADERS)
        if response.status_code != 200:
            raise Exception("status_code != 200")

        result_json = response.json()

        if not result_json:
            break

        page = page + 1

        for item in result_json:
            groups_ids.append(item['id'])

    print(groups_ids)

    project_url = "/".join([GIT_HOST, "api/v4/groups/{id}/projects?per_page=50&page={pageNum}"])

    all_project_git_url = set()
    for group_id in groups_ids:
        page = 1
        while True:
            url = project_url.format(pageNum=page, id=group_id)
            response: Response = requests.get(url, headers=HEADERS)
            if response.status_code != 200:
                raise Exception("status_code != 200")

            result_json = response.json()

            if not result_json:
                break

            page = page + 1

            for project in result_json:
                print("处理：" + project['path_with_namespace'])
                all_project_git_url.add(project['ssh_url_to_repo'])
                print(project['ssh_url_to_repo'])

    return all_project_git_url


def download(all_project_git_url):
    cwd = os.getcwd()
    os.chdir(PATH)

    for git_url in all_project_git_url:
        process = subprocess.run('echo $PWD && git clone ' + git_url, shell=True, capture_output=True, text=True)
        if process.stdout:
            print(process.stdout)
        if process.stderr:
            print(process.stderr)

    os.chdir(cwd)


if __name__ == '__main__':
    parse()
    all_project_git_url = get_project()
    download(all_project_git_url)
