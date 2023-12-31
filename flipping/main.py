#!/usr/bin/env/python3

import urllib3
import csv

# Global Variables
itemApi = "https://universalis.app/api/v2"
mainWorldId = "73" # Adamantoise - update to your home server
dc = "Aether"
region = "North-America"
# Placed at a global scope because I'm lazy
itemlist = {}

class Item:
    def __init__(self, name, itemid, sell):
        self.name = name 
        self.itemid = itemid
        self.sell = sell

# Item that contains additional attributes to store flip values
class FlipItem(Item):    
    def __init__(self, name, itemid, buy, buyserver, sell):
        super().__init__(name, itemid, sell)
        self.buy = buy
        self.buyserver = buyserver

    # String output of variables, good for debugging
    def __str__(self): 
        profit = (self.sell - self.buy)
        profitpct = '%.2f'%((profit / self.buy)*100)
        return f"{self.name},{self.itemid},{self.buy},{self.buyserver},{self.sell},{profit},{profitpct}%"

    # List output of variables, specifically for exporting to csv
    def arrayrow(self):
        profit = (self.sell - self.buy)
        profitpct = '%.2f'%((profit / self.buy)*100)
        return [self.name, self.itemid, self.buy, self.buyserver, self.sell, profit, f"{profitpct}%"]

def parsedata(http):
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
            dc_api_req = getuniversalisdata(http, querystring, dc)
            serv_api_req = getuniversalisdata(http, querystring, mainWorldId)
            updateitemlist(dc_api_req,"dc")
            updateitemlist(serv_api_req,"server")
            querystring = ""
            index += 1

    # Final API query and itemlist update
    if querystring != "":
        dc_api_req = getuniversalisdata(http, querystring, dc)
        serv_api_req = getuniversalisdata(http, querystring, mainWorldId)
        updateitemlist(dc_api_req,"dc")
        updateitemlist(serv_api_req,"server")

# API query to Universalis
def getuniversalisdata(http, querystring, servdc):
    # servdc can be a server ID, DC name, or region name
    # Only retrieves 1 for-sale listing to reduce iterations
    return http.request(
        "GET",
        f"{itemApi}/{servdc}/{querystring}?listings=1"
    )

# Processes Universalis API output and updates itemlist dict with the new attributes
def updateitemlist(response, scope):
    # If query was datacenter scoped, update buy listing information
    if scope == "dc":
        for itemid, item in response.json()['items'].items():
            for listing in item['listings']:
                itemlist[itemid].buy = listing['pricePerUnit']
                itemlist[itemid].buyserver = listing['worldName']
    # If query was server scoped, update sell listing information
    else:
        if scope == "server":
            for itemid, item in response.json()['items'].items():
                for listing in item['listings']:
                    itemlist[itemid].sell = listing['pricePerUnit']

def main():
    http = urllib3.PoolManager()
    # Reads csv contents and stores in itemlist dict
    with open('Price Calculators.csv', newline='') as inputcsv:
        sheet = csv.DictReader(inputcsv)
        for row in sheet:
            itemlist[row['Item ID']] = FlipItem(row['Item Name'], row['Item ID'], 1, "", 1)
        parsedata(http)

    # Writes itemlist dict entries to csv
    with open('Output.csv', 'w', newline='') as outputcsv:
        sheet = csv.writer(outputcsv, delimiter=',')
        sheet.writerow(['Item Name', 'Item ID', 'Buy Price', 'Buy Server',
                      'Sell Price', 'Profit', 'Percent Profit'])
        for row in itemlist:
            sheet.writerow(itemlist[row].arrayrow())

if __name__ == "__main__":
    main()
