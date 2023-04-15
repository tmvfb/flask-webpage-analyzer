from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from dotenv import load_dotenv
import os
import psycopg2
import logging
from urllib.parse import urlparse
from validators import url as validate
from datetime import datetime


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


@app.get('/')
def index():
    # cursor = conn.cursor()
    # cursor.execute('SELECT * FROM urls')
    # all_urls = cursor.fetchall()
    # print(all_urls)

    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )


@app.post('/')
def add_url():
    conn = psycopg2.connect(DATABASE_URL)
    url = request.form['url']
    parsed_url = urlparse(url)
    name = parsed_url.scheme + '://' + parsed_url.netloc
    if not validate(url) or len(name) > 255:
        flash('Incorrect URL', 'danger')
        return redirect(
            url_for('index'),
            code=302
        )

    with conn.cursor() as cursor:
        cursor.execute(
            '''
            SELECT * FROM urls
            WHERE name=(%s);
            ''',
            (name,)
        )
        duplicate = cursor.fetchall()
        if not duplicate:
            cursor.execute(
                '''
                INSERT INTO urls (name, created_at)
                VALUES (%s, %s) RETURNING id, name, created_at;
                ''',
                (name, datetime.now())
            )
            row = cursor.fetchall()
            flash('URL added successfully!', 'success')
        else:
            row = duplicate
            flash('URL is already in URL list', 'info')
        id = row[0][0]
        session['url'] = row[0]
    return redirect(
        url_for('show', id=id),
        code=302
    )


@app.get('/urls/<id>')
def show(id):
    url_desc = session['url']
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        url_desc=url_desc,
        messages=messages
    )


@app.get('/urls')
def show_all():
    conn = psycopg2.connect(DATABASE_URL)
    with conn.cursor() as cursor:
        cursor.execute(
            '''
            SELECT * FROM urls
            '''
        )
        urls = cursor.fetchall()
    return render_template(
        'show_all.html',
        urls=urls
    )
