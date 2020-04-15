from flask import Flask
from createdatabase import createdatabase
from config import Config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

createdatabase(app.config['DATABASE_URL'])

from app import routes