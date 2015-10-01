from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
authors = Table('authors', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('author_f_nm', String(length=250), nullable=False),
    Column('author_l_nm', String(length=250), nullable=False),
)

authors = Table('authors', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first', String(length=250), nullable=False),
    Column('last', String(length=250), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['authors'].columns['author_f_nm'].drop()
    pre_meta.tables['authors'].columns['author_l_nm'].drop()
    post_meta.tables['authors'].columns['first'].create()
    post_meta.tables['authors'].columns['last'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['authors'].columns['author_f_nm'].create()
    pre_meta.tables['authors'].columns['author_l_nm'].create()
    post_meta.tables['authors'].columns['first'].drop()
    post_meta.tables['authors'].columns['last'].drop()
