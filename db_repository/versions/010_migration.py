from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
volunteer_purchases = Table('volunteer_purchases', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DATE, primary_key=True, nullable=False),
    Column('isbn', Integer),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('cost', Integer, nullable=False),
)

volunteer_purchases = Table('volunteer_purchases', post_meta,
    Column('purchase_id', Integer, primary_key=True, nullable=False),
    Column('volunteer_id', Integer),
    Column('date', Date, primary_key=True, nullable=False),
    Column('isbn', Integer),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
    Column('cost', Integer, nullable=False),
)

book_details = Table('book_details', post_meta,
    Column('isbn', Integer, primary_key=True, nullable=False),
    Column('title', String(length=250), nullable=False),
    Column('reading_level', String(length=250), nullable=False),
    Column('publisher', String(length=250), nullable=False),
    Column('condition', String(length=250), nullable=False),
    Column('genre', String(length=250)),
)

client_purchases = Table('client_purchases', post_meta,
    Column('purchase_id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('date', Date, primary_key=True, nullable=False),
    Column('isbn', Integer),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
)

client_purchases_held = Table('client_purchases_held', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DATE, primary_key=True, nullable=False),
    Column('isbn', Integer),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
)

client_purchases_held = Table('client_purchases_held', post_meta,
    Column('purchase_id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('date', Date, primary_key=True, nullable=False),
    Column('isbn', Integer),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['volunteer_purchases'].columns['id'].drop()
    post_meta.tables['volunteer_purchases'].columns['purchase_id'].create()
    post_meta.tables['volunteer_purchases'].columns['volunteer_id'].create()
    post_meta.tables['book_details'].columns['condition'].create()
    post_meta.tables['client_purchases'].columns['client_id'].create()
    pre_meta.tables['client_purchases_held'].columns['id'].drop()
    post_meta.tables['client_purchases_held'].columns['client_id'].create()
    post_meta.tables['client_purchases_held'].columns['purchase_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['volunteer_purchases'].columns['id'].create()
    post_meta.tables['volunteer_purchases'].columns['purchase_id'].drop()
    post_meta.tables['volunteer_purchases'].columns['volunteer_id'].drop()
    post_meta.tables['book_details'].columns['condition'].drop()
    post_meta.tables['client_purchases'].columns['client_id'].drop()
    pre_meta.tables['client_purchases_held'].columns['id'].create()
    post_meta.tables['client_purchases_held'].columns['client_id'].drop()
    post_meta.tables['client_purchases_held'].columns['purchase_id'].drop()
