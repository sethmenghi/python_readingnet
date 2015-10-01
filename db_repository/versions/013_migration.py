from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
author_book_relationships = Table('author_book_relationships', pre_meta,
    Column('author_2id', Integer),
    Column('isbn', String(length=13)),
)

authors_books = Table('authors_books', post_meta,
    Column('author_id', Integer),
    Column('isbn', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['author_book_relationships'].drop()
    post_meta.tables['authors_books'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['author_book_relationships'].create()
    post_meta.tables['authors_books'].drop()
