# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 16:46:25 2018

@author: ihassan1
"""
import requests
import json
import pandas as pd
import datetime as dt

def convertFX(date, foreign_currency, base_currency="AUD"):
    #reference for api docs http://fixer.io/
    #used the datetime iso format
    foreign_currency = foreign_currency.upper()

    if base_currency:
        base_currency = base_currency.upper()

    #convert to datetime
    #date = self._convertToDateTime(date)

    #convert to format "2012-12-01"
    date = date.strftime("%Y-%m-%d")
    #convert FX rates using
    url = "https://api.fixer.io/{0}?base={1}&symbols={2}".format(date, base_currency, foreign_currency)

    i = 0
    while True:
        r = requests.get(url)
        i += 1
        if r.status_code == 200 or i == 20:
            break
        else:
            return ("error in FX api")

    response = json.loads(r.text) #'{"base":"USD","date":"2013-08-05","rates":{"AUD":1.1247}}'
    return  float(response["rates"][foreign_currency])

dateIndex = pd.date_range(start="01-01-2009",end="03-01-2018",freq="d")

