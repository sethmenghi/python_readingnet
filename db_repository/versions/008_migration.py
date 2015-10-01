from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
donors = Table('donors', pre_meta,
    Column('person_id', Integer, primary_key=True, nullable=False),
)

donors = Table('donors', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)

volunteers = Table('volunteers', pre_meta,
    Column('person_id', Integer, primary_key=True, nullable=False),
)

volunteers = Table('volunteers', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['donors'].columns['person_id'].drop()
    post_meta.tables['donors'].columns['id'].create()
    pre_meta.tables['volunteers'].columns['person_id'].drop()
    post_meta.tables['volunteers'].columns['id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['donors'].columns['person_id'].create()
    post_meta.tables['donors'].columns['id'].drop()
    pre_meta.tables['volunteers'].columns['person_id'].create()
    post_meta.tables['volunteers'].columns['id'].drop()
