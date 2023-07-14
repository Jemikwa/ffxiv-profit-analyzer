#!/usr/bin/env/python3

import urllib3
import csv

itemapi = "https://universalis.app/api/v2/"
world = "73" # Adamantoise
dc = "Aether"
region = "North-America"

class Item:
    def __init__(self, name, itemid, sell):
        self.name = name 
        self.itemid = itemid
        self.sell = sell

class TokenItem(Item):    
    def __init__(self, name, itemid, tokencost, tokentype, sell):
        super().__init__(name, itemid, sell)
        self.tokencost = tokencost
        self.tokentype = tokentype
        self.pertoken = '%.2f'%(sell / tokencost)

def getUniversalisData(http, itemlist):
    print("placeholder")

def main(_event, _context):
    http = urllib3.PoolManager()
    itemlist = {}

    with open('price calculator.csv', newline='') as csvfile:
        sheet = csv.DictReader(csvfile)

    getUniversalisData(http, itemlist)


if __name__ == "__main__":
    main(None, None)
