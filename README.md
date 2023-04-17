# flask-webpage-analyzer
[![Website tmvfb-project-83.onrender.com](https://img.shields.io/website-up-down-green-red/https/tmvfb-project-83.onrender.com.svg)](https://tmvfb-project-83.onrender.com/)
[![Actions Status](https://github.com/tmvfb/python-project-83/workflows/hexlet-check/badge.svg)](https://github.com/tmvfb/python-project-83/actions)
[![Github Actions Status](https://github.com/tmvfb/flask-webpage-analyzer/workflows/Python%20CI/badge.svg)](https://github.com/tmvfb/flask-webpage-analyzer/actions)
[![Maintainability](https://api.codeclimate.com/v1/badges/95ac546f1a0c77bde568/maintainability)](https://codeclimate.com/github/tmvfb/flask-webpage-analyzer/maintainability)

### Tools used

| Tool                                                                        | Description                                             |
|-----------------------------------------------------------------------------|---------------------------------------------------------|
| [Flask](https://flask.palletsprojects.com/en/2.2.x/)                        | Web development, one drop at a time                  |
| [Gunicorn](https://gunicorn.org/)                                           | Python WSGI HTTP Server for UNIX                      |
| [psycopg2](https://www.psycopg.org/docs/)                                   | Python-PostgreSQL Database Adapter for Python         |
| [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)    | Python library for pulling data out of HTML and XML files |
| [requests](https://requests.readthedocs.io/en/latest/)                      | HTTP for Humans                                       |
| [Flask-Babel](https://python-babel.github.io/flask-babel/)                  | Implements i18n and l10n support for Flask            |

### Description

Simple web application and SEO tool that scrapes **h1**, **title** and **description** tags for the desired website. Backend is written in Python using Flask for routing, psycopg2 for PostgreSQL database management, Beautiful Soup and requests for HTML parsing. Flask-Babel is used for adding Russian translation. Database and final project are deployed using [render](https://render.com/). Frontend relies on Bootstrap 5.0 and jinja2 templating engine. Database is reset on every server restart.  
  
![image](https://user-images.githubusercontent.com/116455436/232334772-eaf8d74d-21f2-495d-bfce-7c618d69317f.png)

### Prerequisites
* Python >=3.7.10
* pip >=19.0
* poetry >=1.2.0
* PostgreSQL database for local deploy

### Code usage

To reuse this code, a PostgreSQL database server is needed. 

1. `git clone https://github.com/tmvfb/flask-webpage-analyzer.git`
2. `cd flask-webpage-analyzer`
3. `make install` to build dependencies
4. `sh setup.sh` to configure environment variables. You will be prompted to enter your database URL
  
Successful configuration can be started using either `make dev` (Flask dev server) or `make start` (gunicorn production server).

### Acknowledgements

Made as a project for [hexlet.io](https://ru.hexlet.io/) python course.

### Miscellaneous

Update localization files:
1. `pybabel extract -F babel.cfg -o messages.pot .`
2. `pybabel update -i messages.pot -d translations`
3. Complete the corresponding *messsages.po* file
4. `pybabel compile -d translations`
5. `flask --app page_analyzer:app run --extra-files translations/{LANGUAGE}/LC_MESSAGES/messages.mo` to update localization files. Server restart works as well

New translations can be added using following commands:
1. `pybabel extract -F babel.cfg -o messages.pot .`
2. `pybabel init -i messages.pot -d translations -l {LANGUAGE}` (insert 2-digit country code instead of {LANGUAGE})
3. Complete the corresponding *messsages.po* file
4. `pybabel compile -d translations`
5. `flask --app page_analyzer:app run --extra-files translations/{LANGUAGE}/LC_MESSAGES/messages.mo` to update localization files. Server restart works as well
