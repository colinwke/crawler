import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/60.0.3112.101 '
                         'Safari/537.36'}


def get_html(url):
    html = requests.get(url, headers=headers).text

    return html
