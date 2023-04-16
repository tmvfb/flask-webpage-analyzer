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

    meta_tag = soup.find('meta', {'name': 'description'})

    h1 = soup.h1.text if soup.find('h1') else None
    title = soup.title.text if soup.find('title') else None
    description = meta_tag['content'] if meta_tag else None

    return h1, title, description
