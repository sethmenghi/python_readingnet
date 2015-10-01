from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_purchases = Table('client_purchases', pre_meta,
    Column('purchase_id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('date', DATETIME, nullable=False),
    Column('isbn', String(length=13)),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
)

client_purchases = Table('client_purchases', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('date', DateTime, nullable=False),
    Column('isbn', String(length=13)),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
)

client_purchases_held = Table('client_purchases_held', pre_meta,
    Column('purchase_id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('date', DATETIME, primary_key=True, nullable=False),
    Column('isbn', String(length=13)),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
)

client_purchases_held = Table('client_purchases_held', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_id', Integer),
    Column('date', DateTime, primary_key=True, nullable=False),
    Column('isbn', String(length=13)),
    Column('condition', String(length=250), nullable=False),
    Column('edition', String(length=250), nullable=False),
    Column('quantity', Integer, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_purchases'].columns['purchase_id'].drop()
    post_meta.tables['client_purchases'].columns['id'].create()
    post_meta.tables['client_purchases'].columns['quantity'].create()
    pre_meta.tables['client_purchases_held'].columns['purchase_id'].drop()
    post_meta.tables['client_purchases_held'].columns['id'].create()
    post_meta.tables['client_purchases_held'].columns['quantity'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_purchases'].columns['purchase_id'].create()
    post_meta.tables['client_purchases'].columns['id'].drop()
    post_meta.tables['client_purchases'].columns['quantity'].drop()
    pre_meta.tables['client_purchases_held'].columns['purchase_id'].create()
    post_meta.tables['client_purchases_held'].columns['id'].drop()
    post_meta.tables['client_purchases_held'].columns['quantity'].drop()
