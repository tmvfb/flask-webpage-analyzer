from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for
)
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators import url as validate
from datetime import datetime
from .utils import connect, prepare_database


app = Flask(__name__)


load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')
prepare_database()


@app.get('/')
def index():
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
            duplicate = cursor.fetchone()

            if not duplicate:
                cursor.execute(
                    '''
                    INSERT INTO urls (name, created_at)
                    VALUES (%s, %s) RETURNING id, name, created_at;
                    ''',
                    (name, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                row = cursor.fetchone()
                flash('URL added successfully!', 'success')

            else:
                row = duplicate
                flash('URL is already in URL list', 'info')

    id = row[0]
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
            url_desc = cursor.fetchone()

            cursor.execute(
                '''
                SELECT id, status_code, h1, title, description, created_at
                FROM url_checks
                WHERE url_id=(%s);
                ''',
                (id,)
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
                SELECT name FROM urls
                WHERE id=(%s);
                ''',
                (id)
            )
            url = cursor.fetchone()
            try:
                r = requests.get(url[0])
                status_code = r.status_code
            except Exception as e:
                flash(f'Connection error: {str(e)}', 'danger')
                return redirect(
                    url_for('show', id=id),
                    code=302
                )
            cursor.execute(
                '''
                INSERT INTO url_checks (url_id, status_code, created_at)
                VALUES (%s, %s, %s);
                ''',
                (id, status_code, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            )

    return redirect(
        url_for('show', id=id),
        code=302
    )
