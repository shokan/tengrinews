import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

MAIN_LINK = "https://tengrinews.kz"
PAGE_NUM = 4

def _get_soup(some_link):
    response = requests.get(some_link, headers={"User-Agent": UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(response.content, "html.parser")
    return soup
_get_soup(MAIN_LINK)

def _get_link(PAGE_NUM):
    PAGE_LINK = "https://tengrinews.kz/news/page/{}/".format(PAGE_NUM)
    soup = _get_soup(PAGE_LINK)
    link_raw = soup.findAll("a", attrs={"class", "tn-link"})
    links = [i["href"] for i in link_raw]
    return links
all_links = _get_link(4)

TOTAL_PAGE_NUMBER = 5

all_links = []
for i in range(TOTAL_PAGE_NUMBER):
    links = _get_link(i)
    all_links.append(links)

def get_page_info(link):
    main_soup = _get_soup(link)
    news_text = main_soup.find("div", attrs={'class': 'tn-news-text'}).text
    news_title = main_soup.find("h1", attrs={'class': 'tn-content-title'}).text
    datetime = main_soup.find("li", attrs={"class": "tn-hidden@t"}).text

    info = {
        'news_text': news_text,
        'news_title': news_title,
        'datetime': datetime,
    }
    return info

news_dataset = pd.DataFrame(columns=['news_title', 'news_text', 'datetime'])

for link in tqdm(all_links):
    link = '{}{}'.format(MAIN_LINK, link)
    news_dataset = news_dataset.append(get_page_info(link), ignore_index=True)
    time.sleep(0.1)

print(news_dataset.head())