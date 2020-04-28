import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#	local database
 #   DATABASE_URL = "postgresql://objectrocket:mypass@localhost/postgres"
 #  heroku database
#    DATABASE_URL = "postgres://dnksgzdceixveu:e9289a3cd88b80874ba424a0e5f14c20113572f675cedc70a4cb5b94ba875c3a@ec2-18-206-84-251.compute-1.amazonaws.com:5432/dq7nmi44nhj5q"
    DATABASE_URL = "postgres://mavfbjiuszffsa:45a86f616132e192f5ed64cbba7b9d5d5854598f4dfbbecee7bec0b9404ce79b@ec2-34-234-228-127.compute-1.amazonaws.com:5432/d6vt0u73a6qmj1"