import os
basedir = os.path.abspath(os.path.dirname(__file__))

WTF_CSRF_ENABLED = True
SECRET_KEY = os.environ['READING_NET_SECRET_KEY']
SQLALCHEMY_DATABASE_URI = os.environ['READING_NET_DATABASE_URI']
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
READINGNET_BOOKS_PER_PAGE = 20
