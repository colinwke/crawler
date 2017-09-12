import requests
import demjson
import pandas as pd

from wktk import PdPrinter

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.101 Safari/537.36'}


def get_html(url):
    html = requests.get(url, headers=headers).text

    return html


def parse_html(html):
    html = demjson.decode(html)

    items = html['items']
    p_items = []
    for item in items:
        if 'embed_url' in item:
            p_item = []
            # account
            # p_item.append(item['account']['id'])
            # p_item.append(item['account']['is_company'])
            p_item.append(item['account']['resources_count'])
            p_item.append(item['account']['followers_count'])
            p_item.append(item['account']['honor_score'])
            # video
            p_item.append(item['views_count'])
            p_item.append(item['likes_count'])
            p_item.append(item['favorites_count'])
            p_item.append(item['comments_count'])
            p_item.append(item['duration'])
            p_item.append(item['title'])
            p_item.append(item['embed_url'])
            p_items.append(p_item)
        else:
            print('no embed_url')

    items = pd.DataFrame(p_items)
    items.columns = ['resources_count', 'followers_count', 'honor_score',
                     'views_count', 'likes_count', 'favorites_count', 'comments_count',
                     'duration', 'title', 'embed_url']

    return items


def main():
    url = 'https://www.skypixel.com/api/website/resources/videos?page=6&page_size=12&resourceType=&type=latest'

    # page count test
    # for i in range(437, 500, 1):
    #     url = 'https://www.skypixel.com/api/website/resources/videos?page=%d' % i
    #     html = get_html(url)
    #     print(url, len(html))
    #     if len(html) < 25:
    #         print('end')
    #         break

    pieces = []
    for i in range(0, 438):  # max page: 438
        url = 'https://www.skypixel.com/api/website/resources/videos?page=%d' % i
        print(url)
        html = get_html(url)
        content = parse_html(html)
        pieces.append(content)

    pieces = pd.concat(pieces, ignore_index=True)
    pieces.to_csv('./data/skypixel_438.csv', index=False)
    PdPrinter.print_full(pieces)


if __name__ == '__main__':
    main()
