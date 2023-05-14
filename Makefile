SHELL := /bin/bash

#设置项目下载路径
dir := /Users/sdcuike/gitlabproject

#设置gitlab域名
git_host := https://git.xxxx.com

#设置gitlab token
git_access_token := xxxxxxxx



download: venv
	. venv/bin/activate  && pip3 install -r requirements.txt && python3 git_download.py $(git_host) $(git_access_token)  $(dir)

pull:
	. venv/bin/activate  && pip3 install -r requirements.txt && python3 git_pull.py $(dir)


freeze:
	. venv/bin/activate && pip3 freeze requirements.txt 


venv:

	python3 -m venv venv
