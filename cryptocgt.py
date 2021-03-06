# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 12:30:35 2017

@author: ihassan1
need to add the Personal Use Asset 10,000 based on costbase
need to look at converting the currencies to aud
need to look at how transfers look
need to implement fees
need to add the Institution vs Company entity and hence the 50% CGT discount and how to output it(Added)
changes made to handle strings in date
"""

import dateutil.parser
import datetime
import calendar
import requests
import json
import os
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy import MetaData, Column, Table, ForeignKey
from sqlalchemy import Integer, String, Float, Date
from sqlalchemy import select
from dbconfig import users_tbl, currencyfx_tbl

data = [
    {
      "AvgPrice": 436,
      "CreatedTimestampUtc": "2011-03-27T12:29:25.771Z",
      "FeePercent": 0.005,
      "OrderGuid": "5c8885cd-5384-4e05-b397-9f5119353e10",
      "OrderType": "MarketBid",
      "Outstanding": 0,
      "Price": "null",
      "PrimaryCurrencyCode": "Eth",
      "SecondaryCurrencyCode": "Usd",
      "Status": "Filled",
      "Value": 17.47,
      "Volume": 36
    },
    {
      "AvgPrice": 598.0403164178242,
      "CreatedTimestampUtc": "2011-04-27T12:29:25.771Z",
      "FeePercent": 0.005,
      "OrderGuid": "5c8885cd-5384-4e05-b397-9f5119353e10",
      "OrderType": "MarketOffer",
      "Outstanding": 0,
      "Price": "null",
      "PrimaryCurrencyCode": "Eth",
      "SecondaryCurrencyCode": "Usd",
      "Status": "Filled",
      "Value": 17.47,
      "Volume": 36
    }
]

basedir = os.path.abspath(os.path.dirname(__file__))
engine = create_engine('sqlite:///'+os.path.join(basedir,"currfxdb"),echo=False,connect_args={'check_same_thread':False})
metadata = MetaData(bind=engine)

currencyfx_table = Table('currencyfxtbl', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('date', Date),
                    Column('base', String(3)),
                    Column('foreign', String(3)),
                    Column('fxrate', Float)
                    )

class Cryptotax():
    __name__ = "cryptotax"
    __version__ = "1.0"
    __author__ = "Ish Hassan"
    __description__ = "calculating the CGT tax for independent reserve by using the FIFO method | offers = Investor selling a crypto | bid = Investor buying a crypto"


    taxDiscountsDict = {"individual":0.5, "trust":0.5, "fund": 2/3, "SMSF":2/3, "company":1}

    def convertFX(self, date, foreign_currency, base_currency="AUD"):
        #reference for api docs http://fixer.io/

        #used the datetime in datetime.datetime format with time portion all zero's
        date = datetime.datetime(date.year, date.month, date.day, 0, 0, 0)

        foreign_currency = foreign_currency.upper()

        if base_currency:
            base_currency = base_currency.upper()

        #date = datetime.datetime(date.year,date.month, date.day)

        try:
            #db = sqlite3.connect(os.path.join(basedir,"currencyfxdb"))
            #cur = db.cursor()
            #cur.execute('''SELECT fxrate FROM currencyfx WHERE date=? AND foreignfx=?;''', (date,foreign_currency))
            #fxrate = cur.fetchone()

            #conn = engine.connect()
            #sqlQuery = select([currencyfx_table.c.fxrate], and_(currencyfx_table.c.date == date, currencyfx_table.c.foreign == foreign_currency))

            #sqlResult = conn.execute(sqlQuery)
            #fxrate = sqlResult.fetchone()

            selectQuery = select([currencyfx_tbl.c.fxrate], (currencyfx_tbl.c.date == date) & (currencyfx_tbl.c.foreignfx == foreign_currency))
            fxrate = list(selectQuery.execute())

            if fxrate != None:
                return fxrate[0][0]
            else:
                dateAPI = date.strftime("%Y-%m-%d")
                #convert FX rates using
                url = "https://api.fixer.io/{0}?base={1}&symbols={2}".format(dateAPI, base_currency, foreign_currency)

                i = 0
                while True:
                    r = requests.get(url)
                    i += 1
                    if r.status_code == 200:
                        break

                    if i == 20:
                        print("error in fx api")
                        exit()

                response = json.loads(r.text) #'{"base":"USD","date":"2013-08-05","rates":{"AUD":1.1247}}'
                fxrate = float(response["rates"][foreign_currency])

                insertStatement = currencyfx_tbl.insert().execute(foreignfx=foreign_currency, basefx=base_currency, fxrate=fxrate, date=date)
                return(fxrate)

        except Exception as e:
            print(e)

    def getEntityTypes(self):
        #get valid entity types to put in to calculation
        return(list(self.taxDiscountsDict.keys()))


    def _convertToDateTime(self,date):
        #convert to datetime format
        return dateutil.parser.parse(date)

    def _convertToDateIso(self,date):
        #convert dates to ISO format
        return date.isoformat()

    def _TimeSort(self, data):
        #sorts the list of dictionaries by date
        return sorted(data,key=lambda d: d["DisposalTimestampUtc"])


    def _filteredForFilledOrdersAndTimeSortAndConvertFX(self, data):
        #filter for only Filled orders, then convert FX and then sort based on date

        self._tempData = []
        filledStatusList = ["Filled","PartiallyFilledAndCancelled","PartiallyFilled","PartiallyFilledAndExpired"]

        for item in self._data:
            #if item['Status'] == "Filled" or "PartiallyFilledAndCancelled" or "PartiallyFilled" or "PartiallyFilledAndExpired": #check if order if filled or paritally filled
            if item['Status'] in filledStatusList:
                #item["CreatedTimestampUtc"] = dateutil.parser.parse(item["CreatedTimestampUtc"])  #convert to datetime # trial
                #tempDate = str(item["CreatedTimestampUtc"])
                #item["CreatedTimestampUtc"] = datetime.datetime.strptime(tempDate[0:10],"%Y-%m-%d")
                #convert foreign curreny to AUD
                if item["SecondaryCurrencyCode"].upper() != "AUD":
                    if item["SecondaryCurrencyCode"].upper() != "USD" and item["SecondaryCurrencyCode"].upper() != "NZD": #check if valid currency we account for
                        return "error not valid currency"

                    item["AvgPriceFx"] = item["AvgPrice"]

                    tempDate = dateutil.parser.parse(item["CreatedTimestampUtc"])
                    #fxRate = self.convertFX(item["CreatedTimestampUtc"], item["SecondaryCurrencyCode"].upper()) #trial
                    fxRate = self.convertFX(tempDate, item["SecondaryCurrencyCode"].upper())
                    item["AvgPrice"] = float(item["AvgPrice"])/fxRate

                #if type(item["CreatedTimestampUtc"]) is str:
                #    item["CreatedTimestampUtc"] = dateutil.parser.parse(item["CreatedTimestampUtc"])
                #else:
                #    pass

                self._tempData.append(item)

        self._tempData = sorted(self._tempData, key=lambda k: k['CreatedTimestampUtc']) #sorting times

        #for item in self._tempData:
            #item["CreatedTimestampUtc"] = item["CreatedTimestampUtc"].isoformat() #converting datetime objects to iso 8061 again
            #item["CreatedTimestampUtc"] = item["CreatedTimestampUtc"].strftime("%Y-%m-%d")

        return(self._tempData)


    def _uniqueCurrencies(self,data):
        #this creates a list of unique crypto currencies from the transaction data
        self.cryptoList = [i["PrimaryCurrencyCode"] for i in data]
        return set(self.cryptoList)

    def _offersList(self,data):
        #sort the ORDERS for each cryptocurrency
        self.offers = dict((crypto,[]) for crypto in self.cryptoList)
        offerStatusList = ["MarketOffer", "LimitOffer"]

        for item in self._data:
            #if item['OrderType'] == "MarketOffer" or item['OrderType']=="LimitOffer": #if transaction is an order
            if item['OrderType'] in offerStatusList:
                if "AvgPriceFx" in item:
                    self.offers[item['PrimaryCurrencyCode']].append({"Volume": item['Volume'],"AvgPrice": item['AvgPrice'],"FeePercent": item['FeePercent'],"CreatedTimestampUtc": item['CreatedTimestampUtc'], "SecondaryCurrencyCode": item['SecondaryCurrencyCode'], "AvgPriceFx": item["AvgPriceFx"]})
                else:
                    self.offers[item['PrimaryCurrencyCode']].append({"Volume": item['Volume'],"AvgPrice": item['AvgPrice'],"FeePercent": item['FeePercent'],"CreatedTimestampUtc": item['CreatedTimestampUtc'],"SecondaryCurrencyCode": item['SecondaryCurrencyCode']})

        return self.offers

    def _bidsList(self,data):
        #sort the BIDS for each type of cryptocurrency
        self.bids = dict((crypto,[]) for crypto in self.cryptoList)
        bidsStatusList = ["MarketBid", "LimitBid"]

        for item in self._data:
            if item['OrderType'] in bidsStatusList:
                if "AvgPriceFx" in item:
                    self.bids[item['PrimaryCurrencyCode']].append({"Volume": item['Volume'],"AvgPrice": item['AvgPrice'],"FeePercent": item['FeePercent'],"CreatedTimestampUtc": item['CreatedTimestampUtc'],"SecondaryCurrencyCode": item['SecondaryCurrencyCode'], "AvgPriceFx": item["AvgPriceFx"]})
                else:
                    self.bids[item['PrimaryCurrencyCode']].append({"Volume": item['Volume'],"AvgPrice": item['AvgPrice'],"FeePercent": item['FeePercent'],"CreatedTimestampUtc": item['CreatedTimestampUtc'], "SecondaryCurrencyCode": item['SecondaryCurrencyCode']})

        return self.bids

    def _getFinYears(self, data):
    #get the financial year buckets when events can happen

        #get a list of all years and convert to datetime object
        yearList = []
        for crypto in data:
            for item in data[crypto]:
                d = dateutil.parser.parse(item["CreatedTimestampUtc"])
                yearList.append(d.date().year)

        minYear = min(yearList)
        maxYear = max(yearList)

        #adding the datetime buckets
        yearList = [[datetime.date(i-1,7,1),datetime.date(i,6,30)] for i in range(minYear,maxYear+1)]
        yearList.append([datetime.date(maxYear,7,1),datetime.date(maxYear+1,6,30)])

        return yearList

    def _calculateTotalTaxYearCGT(self, losses, gainsNoDiscount, gainsDiscount, discountRate):
        #formula used to calculate CGT gains after losses and eligible discounts

        losses = abs(losses) *1
        if gainsNoDiscount + gainsDiscount < losses:#if losses greater than all my gains
            return gainsDiscount + (gainsNoDiscount - losses)
        elif gainsNoDiscount >= losses: #if gainsNoDiscount cover all losses offset only them
            return gainsDiscount*discountRate + (gainsNoDiscount-losses)
        elif gainsNoDiscount < losses: #if gainsNoDiscount cover only part of losses
            if gainsDiscount < gainsNoDiscount - losses:# gainsDiscount and gainNoDiscount cannot cover all losses
                return gainsDiscount + (gainsNoDiscount - losses)
            elif gainsDiscount >= gainsNoDiscount - losses: #gainsDiscount are able to cover leftover lossess
                return (gainsDiscount + (gainsNoDiscount - losses))*discountRate


    def calculateCGT(self, data, entityType="individual", previousLosses=0, CGTNoDiscountGains=0,discountedCGTGains=0):
        #calculates CGT and returns for each CGT event per crypto
        self._data = data
        self._data = self._filteredForFilledOrdersAndTimeSortAndConvertFX(self._data)

        #error check to see if not a valid currency
        if self._data == "error not valid currency":
            return({"message":"please only use Aud, Usd, and Nzd for the SecondaryCurrencyCode"})

        #initialise the crypto currencies in portfolio, the offers, and bids
        self._cryptoList = self._uniqueCurrencies(data)
        offers = self._offersList(data)
        bids = self._bidsList(data)

        #error checking for entity type lower it unless SMSF
        entityType = entityType.lower()
        if entityType == "smsf":
            entityType = entityType.upper()

        taxDiscountRate = self.taxDiscountsDict[entityType]
        #print("offers",offers)
        #print("bids",bids)

        personalUseAsset = True

        #this is to get finYears array like so {2015:{"cgtEvents":[]}, 2016:{"cgtEvents":[]}}
        finYears = self._getFinYears(offers)
        finYearsDict2 = {i[1].year:{"cgtGainsNoDiscount":{"cgtEvents":[]},"cgtGainsDiscount":{"cgtEvents":[]},"cgtLosses":{"cgtEvents":[]}} for i in finYears}
        #print(finYearsDict)


###############################################################################################################
###############################################################################################################

        #initalise all the transactions that I will use to calculate income tax
        cgtGainsNoDiscount = []
        cgtGainsDiscount = []
        cgtLosses = []

        cumcgtGainsNoDiscount = 0
        cumcgtGainsDiscount = 0
        cumcgtLosses = 0

        for crypto in offers:

            for disposal in offers[crypto]:

                tempCostbaseList = [] #initalize a list that we will use populate with bought items that filled up the volume
                count = 0 #this is count of the number of items that make up the volume
                cumDisposalVolume = 0 #this is the volume of the buys that we want a cumulative total for

                while cumDisposalVolume < disposal["Volume"]: #if the disposal volume is higher than first cost base add more units till it isnt

                    cumDisposalVolume += bids[crypto][count]["Volume"]
                    tempCostbaseList.append(dict(bids[crypto][count]))

                    count += 1

                #adjust Volume to accomodate the change in the last volume
                if cumDisposalVolume > disposal["Volume"]:
                    tempCostbaseList[len(tempCostbaseList)-1]["Volume"] = bids[crypto][len(tempCostbaseList)-1]["Volume"]-(cumDisposalVolume - disposal["Volume"]) #reduce the volume of last point in temp to match disposal volume

                #print(tempCostbaseList)
                dateSold = self._convertToDateTime(disposal["CreatedTimestampUtc"])
                #print(dateSold)

                #calculate the gainOrloss for each item in the tempCostbaseList which makes up the amount of crypto sold
                for tempAcquisition in tempCostbaseList:
                    dateBought = self._convertToDateTime(tempAcquisition["CreatedTimestampUtc"])

                    #how many days required to be eligible for discount depends on leap years
                    if calendar.isleap(dateBought.year) == True:
                        discountDaysRequired = 367
                    else:
                        discountDaysRequired = 366

                    #check if it is a gain or loss for each parcel of the cost base that makes up the cgt event and add the crypto and gainorloss
                    gainOrLoss = tempAcquisition["Volume"]*disposal["AvgPrice"]-tempAcquisition["Volume"]*tempAcquisition["AvgPrice"]
                    tempAcquisition["gainOrLoss"] = gainOrLoss
                    tempAcquisition["PrimaryCurrencyCode"]= crypto
                    tempAcquisition["DisposalTimestampUtc"] = disposal["CreatedTimestampUtc"]
                    tempAcquisition["OfferAvgPrice"]= disposal["AvgPrice"]
                    tempAcquisition["OfferSecondaryCurrencyCode"] = disposal["SecondaryCurrencyCode"]

                    if "AvgPriceFx" in disposal:
                        tempAcquisition["OfferAvgPriceFx"] = disposal["AvgPriceFx"]


                    #print("somthing",tempAcquisition)
                    #check if there is a loss event or if not if it is eligible for the cgt discount and put in respective lists btw cgtLoss, cgtGainDiscount, cgtGainNoDiscount
                    if gainOrLoss <0:
                        cgtLosses.append(tempAcquisition)
                        cumcgtLosses += gainOrLoss
                    elif (dateSold - dateBought).days > discountDaysRequired:
                        cgtGainsDiscount.append(tempAcquisition)
                        cumcgtGainsDiscount += gainOrLoss
                    else:
                        cgtGainsNoDiscount.append(tempAcquisition)
                        cumcgtGainsNoDiscount += gainOrLoss

                #delete the bids which I have used
                del bids[crypto][:count-1]

                #change the bids volume in original list to match the difference in the tempCostBaseList
                if cumDisposalVolume - disposal["Volume"] !=0:
                    bids[crypto][0]["Volume"] = cumDisposalVolume - disposal["Volume"]
                else:
                   del  bids[crypto][0]

###############################################################################################################
###############################################################################################################

        #put cgtGainsNoDiscount into tax year buckets
        for item in cgtGainsNoDiscount:
            d = self._convertToDateTime(item["DisposalTimestampUtc"]).date()
            for dateperiod in finYears:
                if dateperiod[0] < d < dateperiod[1]:
                    finYearsDict2[dateperiod[1].year]["cgtGainsNoDiscount"]["cgtEvents"].append(item)


        #put cgtGainsDiscount into tax year buckets
        for item in cgtGainsDiscount:
            d = self._convertToDateTime(item["DisposalTimestampUtc"]).date()
            for dateperiod in finYears:
                if dateperiod[0] < d < dateperiod[1]:
                    finYearsDict2[dateperiod[1].year]["cgtGainsDiscount"]["cgtEvents"].append(item)


        #put cgtLosses into tax year buckets
        for item in cgtLosses:
            d = self._convertToDateTime(item["DisposalTimestampUtc"]).date()
            for dateperiod in finYears:
                if dateperiod[0] < d < dateperiod[1]:
                    finYearsDict2[dateperiod[1].year]["cgtLosses"]["cgtEvents"].append(item)

        #calculate the taxable income or the tax losses for each tax year
        for taxYear in finYearsDict2: #loop through tax years
            tempDictYearCalc = {} #this is used to keep track of each cgt bucket total i.e. cgtNodiscount, cgtDiscount, cgtLosses
            for cgtBucket in finYearsDict2[taxYear]: #loop through the CGT types (buckets) i.e. cgtNodiscount, cgtDiscount, cgtLosses
                tempCGTtotals = 0  #use a variable to accumulate totals for cgt buckets
                if finYearsDict2[taxYear][cgtBucket]["cgtEvents"]:
                    for cgtEvent in finYearsDict2[taxYear][cgtBucket]["cgtEvents"]:
                            tempCGTtotals += cgtEvent["gainOrLoss"]

                finYearsDict2[taxYear][cgtBucket]["subTotal"]= tempCGTtotals #append cgtBucket total to each bucket
                tempDictYearCalc[cgtBucket] = tempCGTtotals #append to temp dictionary to calculate the overall tax for each year

            #calling the function "calculateTotalTaxYear" to calculate the overall tax for each year taking into account losses and discounts
            finYearsDict2[taxYear]["IncomeTaxOrLoss"] = self._calculateTotalTaxYearCGT(tempDictYearCalc["cgtLosses"],tempDictYearCalc["cgtGainsNoDiscount"],tempDictYearCalc["cgtGainsDiscount"], taxDiscountRate)


        #print("finYearDict",finYearsDict2)
        #print("###############################################")

        #print("cgtgainsnodiscount")
        #print(cgtGainsNoDiscount,"\n")
        #print("cgtgaindiscount")
        #print(cgtGainsDiscount,"\n")
        #print("cgtlosses")
        #print(cgtLosses,"\n")
        #print("cumcgtGainsNoDiscount",cumcgtGainsNoDiscount)
        #print("cgtGainsDiscount",cumcgtGainsDiscount)
        #print("cgtLosses",cumcgtLosses)
                #taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)] = {"taxableIncome":taxableIncome, "date": disposal["CreatedTimestampUtc"]}
            #finYearsDict2["entityType"] = entityType

        responseJson = {}
        responseJson["taxYear"] = finYearsDict2
        responseJson["entityType"] = entityType
        return responseJson

if __name__ == "__main__":
    a = Cryptotax()
    #print(a.cryptoList)
    #print(a.getFinYears(data))
    print(a.calculateCGT(data))
    #print(a.getEntityTypes())
    #print(a.offersStart)
    #print(a.bidsStart)
    #print(a.offers)
    #print(a.bids)

"""
•• Step 1 – The capital gains made during the year are reduced by current year capital losses.
To do this the taxpayer must first calculate gains and losses separately for each CGT event.

•• Step 2 – Reduce the amount remaining (after step 1) by any carry forward capital losses.
Where relevant, the taxpayer should apply the capital losses against gains that are not
eligible for the CGT general discount and then against gains that are eligible.

•• Step 3 – If there is a remaining gain (after step 2), apply the discount percentage to the
eligible gains.

•• Step 4 – If any remaining gains (after step 3, whether or not they are discount gains or not)
qualify for the small business entity concessions, apply those concessions (see the unit on
CGT – exemptions, rollovers and special topics).

•• Step 5 – Add up remaining gains (after step 4). This amount is the taxpayer’s net capital
gain for the year. If there are no remaining gains, add up remaining capital losses (if any),
carry it forward to offset future gains.

---------------------------------------------------------------------------------------------
from CA tax book
12 month holding period
115-25(1) asset must be held for a clear 12 months

(TD 2002/10) The ATO’s view is that both the day of acquisition and the day on which the CGT event happens
must be excluded in reckoning the 12-month period.

So, a period of 365 whole days(or 366 whole days in a leap year) must elapse between the day on which the CGT asset was
acquired and the day on which the CGT event happens
"""
