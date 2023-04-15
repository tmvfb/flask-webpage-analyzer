from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
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
    url = request.form['url']
    parsed_url = urlparse(url)
    name = parsed_url.scheme + '://' + parsed_url.netloc
    if not validate(url) or len(name) > 255:
        flash('Incorrect URL', 'danger')
        return redirect(
            url_for('index'),
            code=302
        )

    with connect() as conn:
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
    return redirect(
        url_for('show', id=id),
        code=302
    )


@app.get('/urls/<id>')
def show(id):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT * FROM urls
                WHERE id=(%s);
                ''',
                (id,)
            )
            url_desc = cursor.fetchall()[0]
            cursor.execute(
                '''
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id=(%s);
                ''',
                (id)
            )
            checks = cursor.fetchall()
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        url_desc=url_desc,
        messages=messages,
        checks=checks
    )


@app.get('/urls')
def show_all():
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT DISTINCT ON (url_checks.url_id)
                    urls.id,
                    urls.name,
                    url_checks.created_at,
                    url_checks.status_code
                FROM urls
                JOIN url_checks ON url_checks.url_id = urls.id
                ORDER BY url_checks.url_id, url_checks.created_at DESC;
                '''
            )
            urls = cursor.fetchall()
    return render_template(
        'show_all.html',
        urls=urls
    )


@app.post('/<id>/checks')
def check(id):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''
                INSERT INTO url_checks (url_id, created_at)
                VALUES (%s, %s);
                ''',
                (id, datetime.now())
            )
    return redirect(
        url_for('show', id=id),
        code=302
    )
