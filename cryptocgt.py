# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 12:30:35 2017

@author: ihassan1
need to add the Personal Use Asset 10,000
need to add the Institution vs Company entity and hence the 50% CGT discount and how to output it
"""

import dateutil.parser
import datetime

data = [{
        "AvgPrice":1.0,
        "CreatedTimestampUtc":"2014-08-05T06:42:11.3032208Z",
        "FeePercent":0.005,
        "OrderGuid":"5c8885cd-5384-4e05-b397-9f5119353e10",
        "OrderType":"MarketBid",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":17.47,
        "Volume":5.00000000
        },
        {
        "AvgPrice":2.0,
        "CreatedTimestampUtc":"2015-08-03T18:33:55.4327861Z",
        "FeePercent":0.005,
        "OrderGuid":"719c495c-a39e-4884-93ac-280b37245037",
        "OrderType":"LimitBid",
        "Outstanding":0.5,
        "Price":700,
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"PartiallyFilledAndCancelled",
        "Value":1050,
        "Volume":10.00000000
        },
        {
        "AvgPrice":3.0,
        "CreatedTimestampUtc":"2016-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketBid",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":20.00000000,
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2016-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":30.00000000
        },
        {
        "AvgPrice":1.0,
        "CreatedTimestampUtc":"2014-08-05T06:42:11.3032208Z",
        "FeePercent":0.005,
        "OrderGuid":"5c8885cd-5384-4e05-b397-9f5119353e10",
        "OrderType":"MarketBid",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":17.47,
        "Volume":5.00000000
        },
        {
        "AvgPrice":2.0,
        "CreatedTimestampUtc":"2015-08-03T18:33:55.4327861Z",
        "FeePercent":0.005,
        "OrderGuid":"719c495c-a39e-4884-93ac-280b37245037",
        "OrderType":"LimitBid",
        "Outstanding":0.5,
        "Price":700,
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"PartiallyFilledAndCancelled",
        "Value":1050,
        "Volume":10.00000000
        },
        {
        "AvgPrice":3.0,
        "CreatedTimestampUtc":"2016-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketBid",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":20.00000000,
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2016-09-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":5.00000000
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2016-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":25.00000000
        }]

#create list for Xbt, Eth, Bch

class Cryptotax():
    __name__ = "cryptotax"
    __version__ = "1.0"
    __author__ = "Ish Hassan"
    __description__ = "calculating the CGT tax for independent reserve by using the FIFO method | offers = Investor selling a crypto | bid = Investor buying a crypto"

    
    taxDiscountsDict = {"individual":0.5, "trust":2/3, "SMSF":2/3, "company":1}
    
    
    def getEntityTypes(self):
        return(list(self.taxDiscountsDict.keys()))
    
    #def __init__(self,data):
        #create data and then filter for only filled orders
        #self.data = data
        #self.data = self._filteredForFilledOrdersAndTimeSort(self.data)

        #initialise the crypto currencies in portfolio, the offers, and bids
        #self.cryptoList = self._uniqueCurrencies(data)
        #self.offers = self._offersList(data)
        #self.bids = self._bidsList(data)


    def _filteredForFilledOrdersAndTimeSort(self, data):
        #filter for only Filled orders and then sort based on date

        self._tempData = []
        filledStatusList = ["Filled","PartiallyFilledAndCancelled","PartiallyFilled","PartiallyFilledAndExpired"]

        for item in self._data:
            #if item['Status'] == "Filled" or "PartiallyFilledAndCancelled" or "PartiallyFilled" or "PartiallyFilledAndExpired": #check if order if filled or paritally filled
            if item['Status'] in filledStatusList:
                item["CreatedTimestampUtc"] = dateutil.parser.parse(item["CreatedTimestampUtc"])  #convert to datetime
                self._tempData.append(item)

        self._tempData = sorted(self._tempData, key=lambda k: k['CreatedTimestampUtc']) #sorting times

        for item in self._tempData:
            item["CreatedTimestampUtc"] = item["CreatedTimestampUtc"].isoformat() #converting datetime objects to iso 8061 again

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
                self.offers[item['PrimaryCurrencyCode']].append({"Volume": item['Volume'],"AvgPrice": item['AvgPrice'],"FeePercent": item['FeePercent'],"CreatedTimestampUtc": item['CreatedTimestampUtc']})

        return self.offers

    def _bidsList(self,data):
        #sort the BIDS for each type of cryptocurrency
        self.bids = dict((crypto,[]) for crypto in self.cryptoList)
        bidsStatusList = ["MarketBid", "LimitBid"]

        for item in self._data:
            if item['OrderType'] in bidsStatusList:
            #if item['OrderType'] == "MarketBid" or item['OrderType']=="LimitBid": #if transaction is an order
                self.bids[item['PrimaryCurrencyCode']].append({"Volume": item['Volume'],"AvgPrice": item['AvgPrice'],"FeePercent": item['FeePercent'],"CreatedTimestampUtc": item['CreatedTimestampUtc']})

        return self.bids

    def _getFinYears(self, data):
    #get the financial year buckets when events can happen

        #get a list of all years and convert to date time object
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

    def calculateCGT(self, data, entityType="individual"):
        #calculates CGT and returns for each CGT event per crypto
        self._data = data
        self._data = self._filteredForFilledOrdersAndTimeSort(self._data)

        #initialise the crypto currencies in portfolio, the offers, and bids
        self._cryptoList = self._uniqueCurrencies(data)
        offers = self._offersList(data)
        bids = self._bidsList(data)
        
        taxDiscountRate = self.taxDiscountsDict[entityType]
        #print("offers",offers)
        #print("bids",bids)

        #this is to get finYears array
        finYears = self._getFinYears(offers)
        finYearsDict = {i[1].year:{} for i in finYears} #{2015:{}, 2016:{}}
        
        #put crypto in each finYears array
        for financialYear in finYearsDict:
            for crypto in self._cryptoList:
                finYearsDict[financialYear][crypto] = {}

        #taxableIncomeList = dict((crypto,{}) for crypto in self._cryptoList)

###############################################################################################################
###############################################################################################################
        for crypto in offers:

            for disposal in offers[crypto]:

                if disposal["Volume"] <= bids[crypto][0]["Volume"]:

                    taxableIncome = disposal["Volume"]*(disposal["AvgPrice"]-bids[crypto][0]["AvgPrice"])
                    newBidsVolume = bids[crypto][0]["Volume"]-disposal["Volume"]
                    if newBidsVolume != 0:
                        bids[crypto][0]["Volume"] = bids[crypto][0]["Volume"]-disposal["Volume"] #reduce the costbase volume down to reflect what was not included in the costbase just used
                    else:
                        del bids[crypto][0]
                        

                else:

                    temp = [] #initalize a list that we will use populate with bought items that filled up the volume
                    tempCostbase = 0
                    count = 0 #this is count of the number of items that make up the volume
                    cumDisposalVolume = 0 #this is the volume of the buys that we want a cumulative total for

                    while cumDisposalVolume < disposal["Volume"]: #if the disposal volume is higher than first cost base add more units till it isnt

                        cumDisposalVolume += bids[crypto][count]["Volume"]
                        temp.append(dict(bids[crypto][count]))
                        
                        count += 1
                        
                    #adjust Volume to accomodate the change in the last volume
                    if cumDisposalVolume > disposal["Volume"]:
                        temp[len(temp)-1]["Volume"] = bids[crypto][len(temp)-1]["Volume"]-(cumDisposalVolume - disposal["Volume"]) #reduce the volume of last point in temp to match disposal volume
                    
                    
                    for tempdisposal in temp:
                        tempCostbase = tempCostbase + tempdisposal["Volume"]*tempdisposal["AvgPrice"]

                    #calculate the taxable Income
                    taxableIncome = disposal["Volume"]*disposal["AvgPrice"] - tempCostbase
                    
                    #delete the bid which I have used
                    del bids[crypto][:count-1]
                    
                    bids[crypto][0]["Volume"] = cumDisposalVolume - disposal["Volume"] #change the bids volume in original list to match the difference in the temp list
###############################################################################################################                    
###############################################################################################################                    #taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)] = taxableIncom

                #loop through all date period buckets and find which bucket it belongs to
                for dateperiod in finYears:
                    d = dateutil.parser.parse(disposal["CreatedTimestampUtc"]).date()

                    if dateperiod[0] < d < dateperiod[1]:
                        cgtEventCount = len(finYearsDict[dateperiod[1].year][crypto].keys())+1 #find the number of keys in the year and then currency combo
                        finYearsDict[dateperiod[1].year][crypto]["CGTevent"+str(cgtEventCount)] = {"taxableIncome":taxableIncome, "date": disposal["CreatedTimestampUtc"]}

                #taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)] = {"taxableIncome":taxableIncome, "date": disposal["CreatedTimestampUtc"]}

                #adding financial years
                #d = dateutil.parser.parse(taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)]["date"])
                #d = d.date()

                #for years in finYears:
                    #if years[0] < d < years[1]:
                        #taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)]["FY"] = years[1].isoformat()

        #add cummulative and crypto totals
        #cummulativeTotal = 0
        #for crypto in taxableIncomeList:
            #total = 0
            #for CGTevent in taxableIncomeList[crypto]:
                #total += taxableIncomeList[crypto][CGTevent]["taxableIncome"]
                #cummulativeTotal += taxableIncomeList[crypto][CGTevent]["taxableIncome"]

            #taxableIncomeList[crypto]["total"] = total
        #delete the year is there is no data in any of the cryptos

        #del all empty years and crypto's
        cryptoCount = len(self._cryptoList)

        for year in list(finYearsDict.keys()):
            emptyDict = True

            for num,crypto in enumerate(list(finYearsDict[year].keys())):
                if finYearsDict[year][crypto]:
                    emptyDict = False
                else:
                    del finYearsDict[year][crypto]

                #if we are at the end of the list and its all empty del
                if num+1 == cryptoCount and emptyDict == True:
                        del finYearsDict[year]


        taxableIncomeJson = {"taxYears":finYearsDict,"taxDiscountRate":taxDiscountRate, "entityType":entityType}
        #taxableIncomeList["cumulativeTotal"] = cummulativeTotal


        for crypto in taxableIncomeJson["taxYears"]:
            for event in taxableIncomeJson["taxYears"][crypto]:
                #finYearsDict[taxableIncomeList["taxEvents"][crypto][event]["FY"]]= taxableIncomeList["taxEvents"][crypto][event]
                pass

        #taxableIncomeList["offers"] = offers
        #taxableIncomeList["years"] = finYears
        return taxableIncomeJson

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
"""