from flask import Flask
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()
app.secret_key = os.environ.get('SECRET_KEY')


@app.route('/')
def index():
    return 'Hello, world!'
