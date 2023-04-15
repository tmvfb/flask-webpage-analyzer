import psycopg2
import logging
import os


logger = logging.getLogger(__name__)
DATABASE_URL = os.getenv('DATABASE_URL')  # written into env via EXPORT


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
