from flask import Flask
from app.server import init_app

app = Flask(__name__)
init_app(app)
