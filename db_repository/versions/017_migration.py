from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
client_reading_levels = Table('client_reading_levels', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

reading_levels = Table('reading_levels', post_meta,
    Column('reading_level', String(length=250), primary_key=True, nullable=False),
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

clients = Table('clients', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('client_name', String(length=250), nullable=False),
    Column('phone', String(length=15), nullable=False),
    Column('email', String(length=250), nullable=False),
    Column('street_name', String(length=250), nullable=False),
    Column('city', String(length=250), nullable=False),
    Column('state', String(length=2), nullable=False),
    Column('zip_code', String(length=10), nullable=False),
    Column('contact_name', String(length=250)),
    Column('tokens', Integer, default=ColumnDefault(20)),
    Column('r_level', String(length=250), nullable=False),
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
    pre_meta.tables['client_reading_levels'].drop()
    post_meta.tables['reading_levels'].create()
    post_meta.tables['client_purchases'].columns['quantity'].create()
    post_meta.tables['clients'].columns['r_level'].create()
    post_meta.tables['client_purchases_held'].columns['quantity'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['client_reading_levels'].create()
    post_meta.tables['reading_levels'].drop()
    post_meta.tables['client_purchases'].columns['quantity'].drop()
    post_meta.tables['clients'].columns['r_level'].drop()
    post_meta.tables['client_purchases_held'].columns['quantity'].drop()
