def extract_content(url):
    html = requests.get(url).text
    soup = bs4.BeautifulSoup(html, 'lxml')
    contents = soup.find_all('div', attrs={'class': 'p_content'})[1:]
    return soup.title, '\n'.join(map(str,contents))




result  = [str(soup.head)]
result.append('<body>')
for hh, ccc in zip(header, cc):
    result.append('<h1>{}</h1>'.format(hh))
    result.append(ccc)
result.append('</body>')
r = '\n'.join(result)

