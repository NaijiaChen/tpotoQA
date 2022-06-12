import requests
import json
from bs4 import BeautifulSoup

chapter_contents = []

def get_resp(url):
    resp = requests.get(url)
    if resp.status_code != 200:
        return 'error'
    else:
        return resp

def get_articles(resp):
    soup = BeautifulSoup(resp.text, 'html5lib')
    contents = soup.find_all('div', class_='content')
    for content in contents:
        cont = content.find("br").getText().strip()
        chapter_contents.append({'conts': cont})
    next_url = 'https://czbooks.net/n/cpn327f/cp4mmop7?chapterNumber=1' + \
        soup.select_one('.next-chapter')['href']
    return next_url

if __name__ == '__main__':
    url = 'https://czbooks.net/n/cpn327f/cp4mmop7?chapterNumber=1'
    for now_page_number in range(4):
        print(f'crawing {url}')
        resp = get_resp(url)
        if resp != 'error':
            url = get_articles(resp)
        print(f'======={now_page_number+1}=======')
    with open('contents.json', 'w', encoding='utf-8') as f:
        json.dump(chapter_contents, f, indent=2,
                  sort_keys=True, ensure_ascii=False)
