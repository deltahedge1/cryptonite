from sqlalchemy import *
import uuid
import os
from appconfig import APP_SECRET_KEY
import jwt

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///'+os.path.join(basedir,"appdatabases.db"))

metadata = MetaData(bind=engine)

#function to get the public id pararmeter just created for the jwt token
def get_publicid(context):
    global APP_SECRET_KEY
    public_id = context.current_parameters.get("public_id")
    token = jwt.encode({"public_id": public_id}, APP_SECRET_KEY, algorithm='HS256')
    return str(token.decode("UTF-8"))

users_tbl = Table('users_tbl', metadata,
    Column('id', Integer, primary_key=True),
    Column('public_id', String(36), unique=True, default=str(uuid.uuid4())),
    Column('company', String(40)),
    Column('token', String, default= get_publicid),
    Column('active',Boolean, default=True)
)

currencyfx_tbl = Table('currencyfx_tbl', metadata,
    Column("id", Integer, primary_key=True),
    Column("foreignfx", String(4), nullable=False),
    Column("basefx", String(4), nullable=False),
    Column("fxrate", Float),
    Column("date", Date, nullable=False)
    )
