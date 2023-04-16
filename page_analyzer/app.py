from flask import (
    Flask,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
    session,
    flash
)
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from validators import url as validate
from .utils import prepare_database
from .database_requests import (
    select_duplicate_id_or_insert_new,
    select_url_desc_and_checks,
    select_checks_for_all_urls,
    insert_new_check
)
from flask_babel import Babel, gettext


app = Flask(__name__)


def get_locale():
    return session.get('language', 'en')


app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_TRANSLATION_DIRECTORIES'] = os.path.join(
    os.getcwd(), 'translations'
)
babel = Babel(app, locale_selector=get_locale)


load_dotenv()
load_dotenv(os.path.join(os.getcwd(), 'secret.env'))
app.secret_key = os.getenv('SECRET_KEY')
prepare_database()


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.get('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'index.html',
        messages=messages
    )


@app.post('/urls')
def add_url():
    url = request.form['url']
    parsed_url = urlparse(url)
    name = parsed_url.scheme + '://' + parsed_url.netloc

    if not validate(url) or len(name) > 255:
        flash(gettext('Incorrect URL'), 'danger')
        return redirect(url_for('index'))

    id = select_duplicate_id_or_insert_new(name)
    return redirect(
        url_for('show', id=id),
        code=302
    )


@app.get('/urls/<int:id>')
def show(id):
    url_desc, checks = select_url_desc_and_checks(id)
    messages = get_flashed_messages(with_categories=True)
    return render_template(
        'show.html',
        url_desc=url_desc,
        messages=messages,
        checks=checks
    )


@app.get('/urls')
def show_all():
    urls = select_checks_for_all_urls()
    return render_template(
        'show_all.html',
        urls=urls
    )


@app.post('/urls/<int:id>/checks')
def check(id):
    insert_new_check(id)
    return redirect(
        url_for('show', id=id),
        code=302
    )


@app.route('/language/<string:lang>')
def change_locale(lang):
    session['language'] = lang
    return redirect(session['path'])  # is set in html template
