import pandas as pd
from tqdm import tqdm
import time
from utils import get_soup, _establish_connection
import mysql.connector as mysql
import conf
import requests
import sys

try:
    TOTAL_PAGE_NUMBER = int(sys.argv[1])
except:
    TOTAL_PAGE_NUMBER = 3

def _get_link(PAGE_NUM):
    PAGE_LINK = "https://tengrinews.kz/news/page/{}/".format(PAGE_NUM)
    soup = get_soup(PAGE_LINK)
    link_raw = soup.findAll("a", attrs={"class", "tn-link"})
    links = [i["href"] for i in link_raw]
    return links

def _existance_checker(link):
    conection = _establish_connection(conf.DB_CREDENTIALS)
    mysql_cursor = conection.cursor()

    mysql_cursor.execute(
        "SELECT count(*) FROM news.links where link = '{}'".format(link)
    )
    row_count = mysql_cursor.fetchone()

    return row_count[0]

def insert_links(link):
    try:
        conection = _establish_connection(conf.DB_CREDENTIALS)
        mysql_cursor = conection.cursor()

        sql = "INSERT INTO news.links (link, is_broken) VALUES ('{}', 0)".format(link)
        mysql_cursor.execute(sql)

        conection.commit()
    except:
        result = 'Error: unable to record values {}'.format(link)
        print(result)

for i in tqdm(range(TOTAL_PAGE_NUMBER)):
    links = _get_link(i)
    for link in links:
        if _existance_checker(link) > 0:
            pass
        else:
            insert_links(link)

    time.sleep(0.1)

