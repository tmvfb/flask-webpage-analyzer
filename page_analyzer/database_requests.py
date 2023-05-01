import requests
from flask import flash
from datetime import datetime
from .utils import bs4_check, connect
from flask_babel import gettext


def select_duplicate_id_or_insert_new(name: str) -> list:
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
                flash(gettext('URL added successfully!'), 'success')

            else:
                row = duplicate
                flash(gettext('Page is already added'), 'info')

    return row[0]


def select_url_desc_and_checks(id: int) -> tuple:
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
    return url_desc, checks


def select_checks_for_all_urls() -> list:
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT DISTINCT ON (urls.id)
                    urls.id,
                    urls.name,
                    url_checks.created_at,
                    url_checks.status_code
                FROM urls
                LEFT JOIN url_checks ON url_checks.url_id = urls.id
                ORDER BY urls.id, url_checks.created_at DESC;
                '''
            )
            urls = cursor.fetchall()
    return urls


def insert_new_check(id: int):
    with connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                '''
                SELECT name FROM urls
                WHERE id=(%s);
                ''',
                (id,)
            )
            url = cursor.fetchone()

            try:
                response = requests.get(url[0])
                response.raise_for_status()
                status_code = response.status_code
                h1, title, description = bs4_check(response.content)

                cursor.execute(
                    '''
                    INSERT INTO url_checks
                    (url_id, status_code, h1, title, description, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s);
                    ''',
                    (id, status_code, h1, title,
                     description, datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                )
                flash(gettext('Page verified successfully'), 'success')

            except requests.exceptions.RequestException:
                flash(gettext('Verification error'), 'danger')

    return
