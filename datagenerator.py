# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 20:24:52 2018

@author: ihassan1
"""
import random
import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)

def randomData(number):
    cryptoCurrencies = ["Xbt","Btc","Eth"]

    data = []
    for i in range(0,number):

        dateRandom = []
        volumeRandom = []
        avgPriceRandom = []
        cryptoRandom = None

        for i in range(0,2):
             year = random.randint(2009, 2017)
             month = random.randint(1, 12)
             day = random.randint(1, 28)
             dateTemp = datetime.datetime(year, month, day)
             dateRandom.append(dateTemp)

             volumeRandom.append(random.randint(1,10000))
             avgPriceRandom.append(random.randint(1,1000))

        cryptoRandom = random.choice(cryptoCurrencies)


        tempData1= {
            "AvgPrice": avgPriceRandom[0],
            "CreatedTimestampUtc":(min(dateRandom)).isoformat(),
            "FeePercent":0.005,
            "OrderGuid":"5c8885cd-5384-4e05-b397-9f5119353e10",
            "OrderType":"MarketBid",
            "Outstanding":0,
            "Price":"null",
            "PrimaryCurrencyCode": cryptoRandom,
            "SecondaryCurrencyCode":"Aud",
            "Status":"Filled",
            "Value":17.47,
            "Volume":max(volumeRandom)
            }

        tempData2 = {
            "AvgPrice":avgPriceRandom[1],
            "CreatedTimestampUtc":(max(dateRandom)).isoformat(),
            "FeePercent":0.005,
            "OrderGuid":"5c8885cd-5384-4e05-b397-9f5119353e10",
            "OrderType":"MarketOffer",
            "Outstanding":0,
            "Price":"null",
            "PrimaryCurrencyCode": cryptoRandom,
            "SecondaryCurrencyCode":"Aud",
            "Status":"Filled",
            "Value":17.47,
            "Volume":min(volumeRandom)
            }

        data.append(tempData1)
        data.append(tempData2)

    return(data)
