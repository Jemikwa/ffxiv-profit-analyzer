#!/usr/bin/env/python3

import urllib3
import csv

itemApi = "https://universalis.app/api/v2"
mainWorldId = "73"
mainWorldName = "Adamantoise"
dc = "Aether"
region = "North-America"
itemlist = {}

class Item:
    def __init__(self, name, itemid, sell):
        self.name = name 
        self.itemid = itemid
        self.sell = sell

class FlipItem(Item):    
    def __init__(self, name, itemid, buy, buyserver, sell):
        super().__init__(name, itemid, sell)
        self.buy = buy
        self.buyserver = buyserver

    def __str__(self): 
        profit = (self.sell - self.buy)
        profitpct = '%.2f'%((profit / self.buy)*100)
        return f"{self.name},{self.itemid},{self.buy},{self.buyserver},{self.sell},{profit},{profitpct}%"

    def arrayrow(self):
        profit = (self.sell - self.buy)
        profitpct = '%.2f'%((profit / self.buy)*100)
        return [self.name, self.itemid, self.buy, self.buyserver, self.sell, profit, f"{profitpct}%"]

def parseQuery(http):
    querystring = ""
    index = 1
    for itemids in itemlist:
        if ((index % 100) != 0):
            querystring += f"{itemids}"
            index +=1 
            if ((index % 100) != 0) and ((index - 1) < len(itemlist)):
                querystring += ","
        else:
            getUniversalisData(http, querystring, dc)
            querystring = ""
    dcApiReq = getUniversalisData(http, querystring, dc)
    servApiReq = getUniversalisData(http, querystring, mainWorldId)

    for id, item in dcApiReq.json()['items'].items():
        for listing in item['listings']:
            itemlist[id].buy = listing['pricePerUnit']
            itemlist[id].buyserver = listing['worldName']

    for id, item in servApiReq.json()['items'].items():
        for listing in item['listings']:
            itemlist[id].sell = listing['pricePerUnit']
    
def getUniversalisData(http, querystring, servdc):
    return http.request(
        "GET",
        f"{itemApi}/{servdc}/{querystring}?listings=1"
    )


def main(_event, _context):
    http = urllib3.PoolManager()
    with open('price calculator.csv', newline='') as inputcsv:
        sheet = csv.DictReader(inputcsv)
        for row in sheet:
            itemlist[row['Item ID']] = FlipItem(row['Item Name'], row['Item ID'], 1, "", 1)
        parseQuery(http)
    
    with open('output.csv', 'w', newline='') as outputcsv:
        sheet = csv.writer(outputcsv, delimiter=',')
        sheet.writerow(['Item Name', 'Item ID', 'Buy Price', 'Buy Server',
                      'Sell Price', 'Profit', 'Percent Profit'])
        for row in itemlist:
            print(itemlist[row].arrayrow())
            sheet.writerow(itemlist[row].arrayrow())

if __name__ == "__main__":
    main(None, None)
