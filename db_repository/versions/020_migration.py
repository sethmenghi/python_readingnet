from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
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


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['clients'].columns['r_level'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['clients'].columns['r_level'].drop()
