from sqlalchemy import *
import uuid
import os

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///'+os.path.join(basedir,"appdatabases.db"))

metadata = MetaData(bind=engine)

users_tbl = Table('users_tbl', metadata,
    Column('id', Integer, primary_key=True),
    Column('public_id', String(36), unique=True, default=str(uuid.uuid4())),
    Column('company', String(40)),
    Column('token', String),
)

currencyfx_tbl = Table('currencyfx_tbl', metadata,
    Column("id", Integer, primary_key=True),
    Column("foreignfx", String(4), nullable=False),
    Column("basefx", String(4), nullable=False),
    Column("fxrate", Float),
    Column("date", Date, nullable=False)
    )
