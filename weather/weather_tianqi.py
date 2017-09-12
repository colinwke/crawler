import requests
from bs4 import BeautifulSoup
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.101 Safari/537.36'}


def get_html(url):
    html = requests.post(url, headers=headers).content

    return html


def parse_html(html):
    soup = BeautifulSoup(html, 'lxml')
    soup = soup.find(attrs={'class': 'tqtongji2'})

    pieces = []
    for ele in soup.find_all('ul')[1:]:
        ele = ele.find_all('li')
        ele = [e.get_text() for e in ele]
        pieces.append(ele)

    return pieces


def main():
    columns = ['date', 'max_temp', 'min_temp', 'weather', 'wind_dire', 'wind_level']
    for year in range(2011, 2017):
        pieces = []
        for month in range(1, 13):
            url = 'http://lishi.tianqi.com/chongqing/%d%02d.html' % (year, month)
            print(url)
            html = get_html(url)
            content = parse_html(html)
            pieces += content
        pieces = pd.DataFrame(pieces, columns=columns)
        pieces.to_csv('./data/tq_cq_%d_2.csv' % year, index=False)


if __name__ == '__main__':
    main()
