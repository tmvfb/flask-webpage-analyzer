from flask import Flask, render_template
from dotenv import load_dotenv
import os
import psycopg2
import logging


app = Flask(__name__)


logger = logging.getLogger(__name__)
load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')  # written into env via EXPORT
conn = psycopg2.connect(DATABASE_URL)


def prepare_database():
    cursor = conn.cursor()
    with open(os.path.join(os.getcwd(), 'database.sql'), 'r') as f:
        try:
            cursor.execute(f.read())
            conn.commit()
        except Exception as e:
            conn.rollback()
            logger.error(str(e))


prepare_database()


@app.route('/')
def index():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM urls')
    all_urls = cursor.fetchall()
    return all_urls
    # return render_template('index.html')
