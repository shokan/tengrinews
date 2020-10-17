from utils import get_soup, _establish_connection
import pandas as pd
from tqdm import tqdm
import conf
import time
import datetime as dt
import re
import requests

def _get_view_count(link):
    article_id = int(re.findall('\d+', link.split("-")[-1] )[0])
    view_count = requests.get('https://counter.tengrinews.kz/inc/tengrinews_ru/news/{}'.format(article_id))
    view_count = view_count.json()["results"]
    return view_count

def _get_article(link):
    try:
        link = '{}{}'.format(conf.MAIN_LINK, link)
        main_soup = get_soup(link)

        news_text = main_soup.find("div", attrs={'class': 'tn-news-text'}).text.replace('\n', ' ').replace('\r', '')
        news_title = main_soup.find("h1", attrs={'class': 'tn-content-title'}).text.replace('\n', ' ').replace('\r', '')
        datetime = main_soup.find("li", attrs={"class": "tn-hidden@t"}).text.replace('\n', ' ').replace('\r', '')
        view_count = _get_view_count(link)
    except:
        news_text = 'unknown'
        news_title = 'unknown'
        view_count = 0

        datetime = dt.datetime.now()

    return news_text, news_title, datetime, view_count


def _get_links():
    conection = _establish_connection(conf.DB_CREDENTIALS)
    df = pd.read_sql("select * FROM news.links where id not in (select link_id from news.articles) and is_broken = 0;", conection)
    return df
article_count = _get_links().shape[0]

def insert_article(id, link):
    news_text, news_title, datetime, view_count = _get_article(link)
    inserted_time = dt.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")

    try:
        conection = _establish_connection(conf.DB_CREDENTIALS)
        mysql_cursor = conection.cursor()

        sql = "DELETE FROM news.articles WHERE link_id = {}".format(id)
        mysql_cursor.execute(sql)

        sql = "INSERT INTO news.articles (link_id, news_text, news_title, published_datetime, inserted_time, view_count) VALUES ({}, '{}', '{}', '{}', '{}', {})".format(id, news_text, news_title, datetime, inserted_time, view_count)
        mysql_cursor.execute(sql)

        conection.commit()
    except:
        sql = "update news.links set is_broken=1 where link = '{}';".format(link)
        mysql_cursor.execute(sql)
        conection.commit()
        result = 'Error: unable to record values {}, {}'.format(id, link)
        print(result)


for i, j in tqdm(_get_links().iterrows()):
    insert_article(j["id"], j["link"])
    time.sleep(0.01)
#
# print("New article(s) count: {}".format(article_count))