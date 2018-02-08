from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, Float, Date
import os
from fxapitrial import convertFX
import pandas as pd
import datetime
from sqlalchemy.sql import select, and_

basedir = os.path.abspath(os.path.dirname(__file__))

engine = create_engine('sqlite:///'+os.path.join(basedir,"currfxdb"),echo=False)

metadata = MetaData(bind=engine)

currencyfx_table = Table('currencyfxtbl', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('date', Date),
                    Column('base', String(3)),
                    Column('foreign', String(3)),
                    Column('fxrate', Float)
                    )


#d = datetime.datetime(2009,1,1)
#d = d.strftime("%Y-%m-%d")
#conn = engine.connect()

#s = select([currencyfx_table.c.fxrate], and_(currencyfx_table.c.date == d, currencyfx_table.c.foreign == "CAD"))

#result = conn.execute(s)
#print(result.fetchone()[0])
metadata.create_all()
#d = pd.date_range("2009/01/01","2010/01/01")
#fxrate = []

#for i in d:
#    dt = datetime.date(i.year,i.month,i.day)
#    a = convertFX(i,"USD")
#    print(i,a)
#    currencyfx_table.insert().execute(date = dt, base = "AUD", foreign = "USD", fxrate = a)
