import psycopg2
import logging
import os
from bs4 import BeautifulSoup
from dotenv import load_dotenv


logger = logging.getLogger(__name__)
load_dotenv()
load_dotenv(os.path.join(os.getcwd(), 'secret.env'))
DATABASE_URL = os.getenv('DATABASE_URL')  # or written into env via export


def connect():
    return psycopg2.connect(DATABASE_URL)


def prepare_database():
    with connect() as conn:
        with conn.cursor() as cursor:
            with open(os.path.join(os.getcwd(), 'database.sql'), 'r') as f:
                try:
                    cursor.execute(f.read())
                    conn.commit()
                except Exception as e:
                    conn.rollback()
                    logger.error(str(e))


def bs4_check(response):
    soup = BeautifulSoup(response, 'html.parser')
    h1 = soup.find('h1')
    title = soup.find('title')
    meta_tag = soup.find('meta', {'name': 'description'})

    if h1:
        h1 = soup.h1.text
    else:
        h1 = None
    if title:
        title = soup.title.text
    else:
        title = None
    if meta_tag:
        description = meta_tag['content']
    else:
        description = None

    return h1, title, description
