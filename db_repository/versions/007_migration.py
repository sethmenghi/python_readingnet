from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_purchases = Table('client_purchases', post_meta,
    Column('purchase_id', Integer, primary_key=True, nullable=False),
    Column('date', Date, primary_key=True, nullable=False),
    Column('isbn', Integer),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
)

donors = Table('donors', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

donors = Table('donors', post_meta,
    Column('person_id', Integer, primary_key=True, nullable=False),
)

volunteers = Table('volunteers', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

volunteers = Table('volunteers', post_meta,
    Column('person_id', Integer, primary_key=True, nullable=False),
)

book_donations = Table('book_donations', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('isbn', Integer, nullable=False),
    Column('donor_id', Integer),
    Column('date', Date, nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('condition', String(length=250), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client_purchases'].columns['purchase_id'].create()
    pre_meta.tables['donors'].columns['id'].drop()
    post_meta.tables['donors'].columns['person_id'].create()
    pre_meta.tables['volunteers'].columns['id'].drop()
    post_meta.tables['volunteers'].columns['person_id'].create()
    post_meta.tables['book_donations'].columns['condition'].create()
    post_meta.tables['book_donations'].columns['isbn'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['client_purchases'].columns['purchase_id'].drop()
    pre_meta.tables['donors'].columns['id'].create()
    post_meta.tables['donors'].columns['person_id'].drop()
    pre_meta.tables['volunteers'].columns['id'].create()
    post_meta.tables['volunteers'].columns['person_id'].drop()
    post_meta.tables['book_donations'].columns['condition'].drop()
    post_meta.tables['book_donations'].columns['isbn'].drop()
