import pandas as pd
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup

MAIN_LINK = "https://tengrinews.kz/"
PAGE_NUM = 4


def _get_soup(some_link):
    response = requests.get(some_link, headers={"User-Agent": UserAgent().chrome})
    soup = BeautifulSoup(response.content, "html.parser")
    return soup


def _get_link(PAGE_NUM):
    PAGE_LINK = "https://tengrinews.kz/news/page/{}/".format(PAGE_NUM)
    soup = _get_soup(PAGE_LINK)
    link_raw = soup.findAll("a", attrs={"class", "tn-link"})
    links = [i["href"] for i in link_raw]
    return links

# print(_get_link(4))

link = "https://tengrinews.kz/kazakhstan_news/pravila-denejnyih-vyiplat-medikam-izmenili-v-kazahstane-409391/"
main_soup = _get_soup(link)
news_text = main_soup.find("div", attrs={'class': 'tn-news-text'}).text
news_title = main_soup.find("h1", attrs={'class': 'tn-content-title'}).text
datetime = main_soup.find("li", attrs={"class": "tn-hidden@t"}).text

print(datetime)