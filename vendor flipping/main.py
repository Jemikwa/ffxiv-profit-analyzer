#!/usr/bin/env/python3

import urllib3
import csv

# Global Variables
itemApi = "https://universalis.app/api/v2"
mainWorldId = "73" # Adamantoise - update to your home server

class Item:
    def __init__(self, name:str, itemid:int, sell:int):
        self.name = name
        self.itemid = itemid
        self.sell = sell

# Item that contains additional attributes to store flip values
class VendorFlipItem(Item):
    def __init__(self, name:str, itemid:int, buy:int, sell:int):
        super().__init__(name, itemid, sell)
        self.buy = buy

    # List output of variables, specifically for exporting to csv
    def arrayrow(self):
        vendorprofit = (self.sell - self.buy)
        return [self.name, self.itemid, self.buy, self.sell, vendorprofit]

def parsedata(http, itemlist):
    querystring = ""
    index = 1
    # Processing items to query Universalis
    # Universalis handles up to 100 items in one query
    for itemids in itemlist:
        if (index % 100) != 0:
            querystring += f"{itemids}"
            index += 1
            # If not a multiple of 100 or not at the end of the list, add a comma
            if ((index - 1 % 100) != 0) and ((index - 1) < len(itemlist)):
                querystring += ","
        # Every 100 items, do an API query and update itemlist dict
        else:
            serv_api_req = getuniversalisdata(http, querystring, mainWorldId)
            updateitemlist(serv_api_req, itemlist)
            querystring = ""
            index += 1

    # Final API query and itemlist update
    if querystring != "":
        serv_api_req = getuniversalisdata(http, querystring, mainWorldId)
        updateitemlist(serv_api_req, itemlist)

# API query to Universalis
def getuniversalisdata(http, querystring, servdc):
    # servdc can be a server ID, DC name, or region name
    # Only retrieves 1 for-sale listing to reduce iterations
    return http.request(
        "GET",
        f"{itemApi}/{servdc}/{querystring}?listings=1"
    )

# Processes Universalis API output and updates itemlist dict with the new attributes
def updateitemlist(response, itemlist):
    for itemid, item in response.json()['items'].items():
        for listing in item['listings']:
            itemlist[itemid].sell = int(listing['pricePerUnit'])

def main():
    itemlist = {}
    http = urllib3.PoolManager()
    # Reads csv contents and stores in itemlist dict
    with open('Price Calculators.csv', newline='') as inputcsv:
        sheet = csv.DictReader(inputcsv)
        for row in sheet:
            # name, itemid, buy, sell
            itemlist[row['Item ID']] = VendorFlipItem(row['Item Name'], int(row['Item ID']), int(row['Vendor Price']), 1)
        parsedata(http, itemlist)

    # Writes itemlist dict entries to csv
    with open('Output.csv', 'w', newline='') as outputcsv:
        sheet = csv.writer(outputcsv, delimiter=',')
        sheet.writerow(['Item Name', 'Item ID', 'Vendor Price', 'Sell Price', 'Vendor Profit'])
        for row in itemlist:
            sheet.writerow(itemlist[row].arrayrow())

if __name__ == "__main__":
    main()
