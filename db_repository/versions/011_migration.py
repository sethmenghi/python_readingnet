from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
book_details = Table('book_details', post_meta,
    Column('isbn', Integer, primary_key=True, nullable=False),
    Column('title', String(length=250), nullable=False),
    Column('reading_level', String(length=250), nullable=False),
    Column('publisher', String(length=250), nullable=False),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=50), nullable=False),
    Column('genre', String(length=250)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book_details'].columns['edition'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['book_details'].columns['edition'].drop()
