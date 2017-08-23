#!/usr/bin/env python
import requests
import re
import bs4
from app.parse import parse
url = 'http://www.ssglobal.me/wp/blog/2017/02/22/%E8%B4%A6%E5%8F%B7%E5%88%86%E4%BA%AB/'
url2 = 'https://plus.google.com/communities/103542666306656189846/stream/dd570c04-df51-4394-8c83-eabb12cc0d0c'


def request_url(url):
    data = list()
    try:
        response = requests.get(url2, verify=False).text
        data += re.findall('ssr?://\w+', response)
    except Exception:
        pass
    soup = bs4.BeautifulSoup(response)
    title = soup.find('title')

    info = {'message': '', 'url': url, 'name': str(title)}
    servers = [parse(server) for server in data]
    return servers, info
