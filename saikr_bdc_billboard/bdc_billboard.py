"""
version: next_page
"""
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'http://bdc.saikr.com/c/rl/34541?t=0'


def download_page(url):
    html = requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }).content

    return html


def parse_html(html):
    soup = BeautifulSoup(html)
    list_soup = soup.find('tbody')

    element_list = []

    for element_li in list_soup.find_all('tr'):
        element = element_li.find_all('td')
        element = [x.get_text().strip() for x in element]
        element_list.append(element)

    next_page = soup.find('li', attrs={'class': 'next'})
    if next_page:
        next_page = next_page.find('a')
        return element_list, DOWNLOAD_URL + next_page['href'][-7:]
    return element_list, None


def main():
    url = DOWNLOAD_URL

    contents = []
    while url:
        html = download_page(url)
        current_content, url = parse_html(html)
        print(current_content)
        contents += current_content

    import pandas as pd
    data = pd.DataFrame(contents)
    print(data)
    columns = ['rank', 'team', 'university', 'score', 'time']
    data.columns = columns

    data.to_csv('./data/billboard_a_end.csv', index=False)


if __name__ == '__main__':
    main()
