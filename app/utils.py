import mysql.connector as mysql
import pandas as pd
import conf
import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup


def _establish_connection(credentials):
    try:
        db = mysql.connect(
            host = credentials['host'],
            user = credentials['user'],
            passwd = credentials['passwd']
        )
    except:
        print("Error: unable establish a connection with database")
    return db

def get_soup(some_link):
    response = requests.get(some_link, headers={"User-Agent": UserAgent(verify_ssl=False).chrome})
    soup = BeautifulSoup(response.content, "html.parser")
    return soup

