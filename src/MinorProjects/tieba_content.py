import os

import bs4
import requests


def extract_content(url):
    url = url.strip()
    html = requests.get(url, params={'see_lz': 1}).text
    soup = bs4.BeautifulSoup(html, 'html.parser')
    contents = soup.find_all('div', attrs={'class': 'p_content'})
    # contents = contents[1:]
    return soup.title.text, '\n'.join(map(str, contents))


def crawl(url_list):
    head = str(bs4.BeautifulSoup(requests.get(url_list[0]).text, 'html.parser').head)
    result_list = [head]
    result_list.append('<body>')
    for url in url_list:
        print(url, end='\t')
        title, content = extract_content(url)
        print(title)
        result_list.append('<h1>{}</h1>'.format(title))
        result_list.append(content)
    result_list.append('</body>')
    result = '\n'.join(result_list)
    return result


def main():
    path = 'url_list.txt'
    if not os.path.exists(path):
        os.system(' '.join(['vim', path]))
    urls = [i for i in open(path).readlines() if len(i) > 5]
    content = crawl(urls)
    open('tieba.html', 'w').write(content)


if __name__ == '__main__':
    main()
