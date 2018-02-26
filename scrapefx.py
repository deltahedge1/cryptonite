import pandas as pd
import datetime
from dbconfig import engine
import requests
import json

#import the engine connection from our dbconfig file
try:
    conn = engine.connect()
except:
    print("could not connect to sql database\n exiting python script")
    exit()

#df = pd.DataFrame([["USD","AUD",3.42,datetime.date(2012,6,12)]], columns=["foreignfx","basefx","fxrate","date"])
dateRange = pd.date_range(datetime.date(2009,1,1), datetime.date.today())
#dateRange = pd.date_range(datetime.date(2009,1,1), datetime.date(2009,1,5))

fxList = []
for dateItem in dateRange:
    dateAPI = dateItem.strftime("%Y-%m-%d")
    #convert FX rates using
    url = "https://api.fixer.io/{0}?base={1}&symbols={2},{3}".format(dateAPI, "AUD", "USD","NZD")
    r = requests.get(url)
    response = json.loads(r.text)

    USDRate = response['rates']['USD']
    NZDRate = response['rates']['NZD']

    USDList = ["USD","AUD", USDRate, dateItem]
    NZDList = ["NZD","AUD", NZDRate, dateItem]

    print(USDList, "\n", NZDList)
    fxList.append(USDList)
    fxList.append(NZDList)

df = pd.DataFrame(fxList, columns=["foreignfx","basefx","fxrate","date"])
df.to_sql("currencyfx_tbl", conn, if_exists="append", index=False)
