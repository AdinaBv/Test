import requests
import sys
import datetime
import time

urls = []
try:
    url = sys.argv[1]
except:
    exit(
        "Something went horribly wrong! Your computer will shut down in 5 seconds!"
    )

if len(url.split("/")) != 2:
    url = url.split("/")[3] + "/" + url.split("/")[4]

tags_url = 'https://api.github.com/repos/' + url + '/git/refs/tags'
API_HEAD = {'Authorization': 'token 872eaaf9118c5b01ed2937a6f77f1df37149402'}

def get_time_remaining():
    api_main_url = 'https://api.github.com/rate_limit'
    api_main_page = requests.get(api_main_url, headers=API_HEAD).json()
    reset_time = datetime.datetime.fromtimestamp(api_main_page['resources']['core']['reset'])
    now = datetime.datetime.now()
    remaining = int((reset_time - now).total_seconds()) + 1  # add one extra second, just to make sure
    return remaining

while True:
    tags_page = requests.get(tags_url,headers=API_HEAD)
    if tags_page.status_code == 200:
        tags_json = tags_page.json()
        for item in tags_json:
            tag_name = item['ref'].replace('refs/tags/', '')
            urls.append('https://github.com/' + url + '/archive/' + tag_name + '.zip')
            urls.append('https://github.com/' + url + '/archive/' + tag_name + '.tar.gz')
        break
    else:
        wait_for = get_time_remaining()
        print('API Limit reached. Waiting %d seconds...' % wait_for)
        time.sleep(wait_for)

p = 1
while True:
    rel_url = 'https://api.github.com/repos/' + url + '/releases?per_page=100&page=' + str(p)
    rel_page = requests.get(rel_url,headers=API_HEAD)
    if rel_page.status_code == 200:
        next_page = rel_page.headers.get('Link', None)
        rel_json = rel_page.json()
        if rel_json:
            for i in range(0, len(rel_json)):
                for j in range(0, len(rel_json[i]['assets'])):
                    urls.append(rel_json[i]['assets'][j]['browser_download_url'])
        if next_page and 'rel="next"' in next_page:
            p += 1
        else:
            break
    else:
        wait_for = get_time_remaining()
        print('API Limit reached. Waiting %d seconds...' % wait_for)
        time.sleep(wait_for)

for url in urls:
    print(url)
