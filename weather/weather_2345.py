import requests
import demjson
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.101 Safari/537.36'}


def get_js(url):
    content = requests.post(url, headers=headers)

    return content.text


def parse_js(content):
    content = content[16:-1]  # ';' in the tail!
    content = demjson.decode(content)

    # === print content
    # for key in content:
    #     print(key, end=': ')
    #     print(content[key])

    tqInfoes = content['tqInfo']
    tqInfoes = pd.DataFrame(tqInfoes[:-1])

    return tqInfoes


def main():
    for year in range(2011, 2017):
        pieces = []
        for month in range(1, 13):
            url = 'http://tianqi.2345.com/t/wea_history/js/%d%02d/57516_%d%02d.js' % (year, month, year, month)
            content = get_js(url)
            if content[:1] == '<':  # error url
                url = 'http://tianqi.2345.com/t/wea_history/js/57516_%d%d.js' % (year, month)
                content = get_js(url)
            print(url)
            content = parse_js(content)
            pieces.append(content)

        pieces = pd.concat(pieces, ignore_index=True)
        pieces.to_csv('./data/tq_cq_%d.csv' % year, index=False)


if __name__ == '__main__':
    main()
