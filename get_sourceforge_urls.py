import requests
from bs4 import BeautifulSoup
import sys

p_url = str(sys.argv[1])+'/files'


def get_download_urls(url):
    files_page = requests.get(url)
    files_soup = BeautifulSoup(files_page.content, 'html.parser')
    for row in files_soup.find('table', {'id': 'files_list'}).find('tbody').find_all('tr'):
        link_type = row['class'][0]
        if link_type == 'folder':
            next_files_page = 'https://sourceforge.net' + row.find('a')['href']
            get_download_urls(next_files_page)
        elif link_type == 'file':
            dl_url = row.find('a')['href'][:-9]
            print(dl_url)


get_download_urls(p_url)
