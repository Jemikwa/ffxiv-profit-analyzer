#!/usr/bin/env/python3

import urllib3
import csv
import os
import time

itemApi = "https://universalis.app/api/v2/"
mainWorldId = "73" # Adamantoise

# Can handle as many token types per item in a single sheet as you like.
# Will only query each item once per sheet import, as the sell price does not depeend on how many tokens an item can be bought with

class Item:
    def __init__(self, name:str, itemid:int, sell:int):
        self.name = name 
        self.itemid = itemid
        self.sell = sell

class TokenItem(Item):    
    def __init__(self, name:str, itemid:int, tokencostbase:int, tokentypebase:str, sell:int):
        super().__init__(name, itemid, sell)
        # Defines base key pair of token type : token cost
        # Further additions can be added with item.tokens[tokentype] = tokencost
        self.tokens = { tokentypebase: tokencostbase }

    def arrayrow(self):
        # Returns all tokens in multiple array rows to be split up later when writing to a file
        returnblock = {}
        # `i` is an arbitrary value for array keypair
        i = 0
        for token in self.tokens:
            pertoken = '%.2f'%(self.sell / self.tokens[token])
            returnblock[i] = [self.name, self.itemid, self.tokens[token], token, self.sell, pertoken]
            i += 1
        return returnblock


def parsedata(http, itemlist):
    # Processing items to query Universalis
    # Universalis handles up to 100 items in a single query
    querystring = ""
    index = 1
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
    # Only updates sell values in this token script
    for itemid, item in response.json()['items'].items():
        for listing in item['listings']:
            itemlist[itemid].sell = listing['pricePerUnit']


def main():
    http = urllib3.PoolManager()
    # Handles multiple files located in ./project/inputs
    for root, dirs, files in os.walk(f"{os.getcwd()}/inputs"):
        for file in files:
            itemlist = {}
            print(f"Reading file {file}")
            with open(f"inputs/{file}", newline='') as inputcsv:
                sheet = csv.DictReader(inputcsv)
                for row in sheet:
                    if row['Item ID'] in itemlist:
                        # If item already exists in itemlist, update the tokens dict to store the new token keypair
                        itemlist[row['Item ID']].tokens[row['Token Type']] = int(row['Token Cost'])
                    else:
                        # Brand-new item, create object and store in itemlist
                        itemlist[row['Item ID']] = TokenItem(row['Item Name'], int(row['Item ID']),
                                                             int(row['Token Cost']), row['Token Type'], 1)
                parsedata(http, itemlist)
                # Safety measure to keep from reaching Universalis' API limits
                time.sleep(1)
                inputcsv.close()

            # Writes itemlist dict entries to csv
            with open(f"outputs/Output - {file}", 'w', newline='') as outputcsv:
                print(f"Writing to file Output - {file}")
                sheet = csv.writer(outputcsv, delimiter=',')
                sheet.writerow(['Item Name', 'Item ID', 'Token Cost', 'Token Type',
                              'Sell Price', 'Gil Per Token'])
                # Iterates through itemlist, then each item's token keypair
                for row in itemlist:
                    array = itemlist[row].arrayrow()
                    for index in array:
                        sheet.writerow(array[index])
                outputcsv.close()


if __name__ == "__main__":
    main()
