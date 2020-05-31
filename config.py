import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # heroku database
    DATABASE_URL = "postgres://dnksgzdceixveu:e9289a3cd88b80874ba424a0" \
                   "e5f14c20113572f675cedc70a4cb5b94ba875c3a@ec2-18-206-" \
                   "84-251.compute-1.amazonaws.com:5432/dq7nmi44nhj5q"
    # local database
    # DATABASE_URL = "postgresql://objectrocket:mypass@localhost/postgres"
