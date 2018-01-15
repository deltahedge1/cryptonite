# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 12:30:35 2017

@author: ihassan1
"""

import dateutil.parser

data = [{
        "AvgPrice":5.0,
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
        "AvgPrice":3.0,
        "CreatedTimestampUtc":"2014-08-03T18:33:55.4327861Z",
        "FeePercent":0.005,
        "OrderGuid":"719c495c-a39e-4884-93ac-280b37245037",
        "OrderType":"LimitBid",
        "Outstanding":0.5,
        "Price":700,
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"PartiallyFilledAndCancelled",
        "Value":1050,
        "Volume":20.00000000
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2014-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":5.00000000
        },
        {
        "AvgPrice":10.0,
        "CreatedTimestampUtc":"2014-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Xbt",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":7.00000000
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2014-08-05T06:42:11.3032208Z",
        "FeePercent":0.005,
        "OrderGuid":"5c8885cd-5384-4e05-b397-9f5119353e10",
        "OrderType":"MarketBid",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Eth",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":17.47,
        "Volume":5.00000000
        },
        {
        "AvgPrice":3.0,
        "CreatedTimestampUtc":"2014-08-03T18:33:55.4327861Z",
        "FeePercent":0.005,
        "OrderGuid":"719c495c-a39e-4884-93ac-280b37245037",
        "OrderType":"LimitBid",
        "Outstanding":0.5,
        "Price":700,
        "PrimaryCurrencyCode":"Eth",
        "SecondaryCurrencyCode":"Usd",
        "Status":"PartiallyFilledAndCancelled",
        "Value":1050,
        "Volume":20.00000000
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2014-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Eth",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":5.00000000
        },
        {
        "AvgPrice":10.0,
        "CreatedTimestampUtc":"2014-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Eth",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":7.00000000
        },
        {
        "AvgPrice":5.0,
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
        "AvgPrice":3.0,
        "CreatedTimestampUtc":"2014-08-03T18:33:55.4327861Z",
        "FeePercent":0.005,
        "OrderGuid":"719c495c-a39e-4884-93ac-280b37245037",
        "OrderType":"LimitBid",
        "Outstanding":0.5,
        "Price":700,
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"PartiallyFilledAndCancelled",
        "Value":1050,
        "Volume":20.00000000
        },
        {
        "AvgPrice":5.0,
        "CreatedTimestampUtc":"2014-08-02T05:33:48.2354125Z",
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
        "AvgPrice":10.0,
        "CreatedTimestampUtc":"2014-08-02T05:33:48.2354125Z",
        "FeePercent":0.005,
        "OrderGuid":"33ea8ee7-5b7b-4745-b604-1a3ce955ca1b",
        "OrderType":"MarketOffer",
        "Outstanding":0,
        "Price":"null",
        "PrimaryCurrencyCode":"Btc",
        "SecondaryCurrencyCode":"Usd",
        "Status":"Filled",
        "Value":975,
        "Volume":7.00000000
        }]

#create list for Xbt, Eth, Bch

class Cryptotax():
    __name__ = "cryptotax"
    __version__ = "1.0"
    __author__ = "Ish Hassan"
    __description__ = "calculating the CGT tax for independent reserve by using the FIFO method | offers = Investor selling a crypto | bid = Investor buying a crypto"

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

    def calculateCGT(self, data):
        #calculates CGT and returns for each CGT event per crypto
        self._data = data
        self._data = self._filteredForFilledOrdersAndTimeSort(self._data)

        #initialise the crypto currencies in portfolio, the offers, and bids
        self._cryptoList = self._uniqueCurrencies(data)
        offers = self._offersList(data)
        bids = self._bidsList(data)

        taxableIncomeList = dict((crypto,{}) for crypto in self._cryptoList)

        for crypto in offers:
            cgtEventCount = 0

            for disposal in offers[crypto]:
                cgtEventCount += 1

                if disposal["Volume"] <= bids[crypto][0]["Volume"]:

                    taxableIncome = disposal["Volume"]*(disposal["AvgPrice"]-bids[crypto][0]["AvgPrice"])
                    newBidsVolume = bids[crypto][0]["Volume"]-disposal["Volume"]
                    if newBidsVolume != 0:
                        bids[crypto][0]["Volume"] = bids[crypto][0]["Volume"]-disposal["Volume"] #reduce the costbase volume down to reflect what was not included in the costbase just used
                    else:
                        del bids[crypto][0]

                    #taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)] = taxableIncome

                else:

                    temp = [] #initalize a list that we will use populate with bought items that filled up the volume
                    tempCostbase = 0
                    count = 0 #this is count of the number of items that make up the volume
                    cumDisposalVolume = 0 #this is the volume of the buys that we want a cumulative total for

                    while True: #if the disposal volume is higher than first cost base add more units till it isnt

                        cumDisposalVolume = cumDisposalVolume + bids[crypto][count]["Volume"]
                        temp.append(dict(bids[crypto][count]))

                        if cumDisposalVolume <= disposal["Volume"]:
                            count += 1

                        if cumDisposalVolume > disposal["Volume"]:
                            temp[len(temp)-1]["Volume"] = bids[crypto][len(temp)-1]["Volume"]-(cumDisposalVolume - disposal["Volume"]) #reduce the volume of last point in temp to match disposal volume

                        for tempdisposal in temp:
                            tempCostbase = tempCostbase + tempdisposal["Volume"]*tempdisposal["AvgPrice"]

                        taxableIncome = disposal["Volume"]*disposal["AvgPrice"] - tempCostbase

                        #del Bch_Offers[0]

                        for i in range(count):
                            del bids[crypto][0] # as you delete it becomes the 0th element so always delete the 0th element

                        bids[crypto][0]["Volume"] = cumDisposalVolume - disposal["Volume"] #change the bids volume in original list to match the difference in the temp list

                        taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)] = taxableIncome

                        break

                #add the taxable income to the list
                taxableIncomeList[crypto]["CGTevent"+str(cgtEventCount)] = {"taxableIncome":taxableIncome, "date": disposal["CreatedTimestampUtc"]}

        #add cummulative and crypto totals
        cummulativeTotal = 0
        for crypto in taxableIncomeList:
            total = 0
            for CGTevent in taxableIncomeList[crypto]:
                total += taxableIncomeList[crypto][CGTevent]["taxableIncome"]
                cummulativeTotal += taxableIncomeList[crypto][CGTevent]["taxableIncome"]

            taxableIncomeList[crypto]["Total"] = total

        taxableIncomeList = {"taxEvents":taxableIncomeList}
        taxableIncomeList["cummulativeTotal"] = cummulativeTotal


        return taxableIncomeList

if __name__ == "__main__":
    a = Cryptotax()
    #print(a.cryptoList)
    print(a.calculateCGT(data))
    #print(a.offersStart)
    #print(a.bidsStart)
    #print(a.offers)
    #print(a.bids)
