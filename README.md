# ffxiv-profit-analyzer

Tools to assess profits of various input items. Uses data from https://universalis.app API. 

Supply your own items and item IDs from a csv.

## Flipping
Buy on one server, sell on your home server. Pulls buy and sell data (latest single value only) from Universalis. 
Provides % profit for determining ideal margins on your own. 

#### Requirements:
* Input columns: "Item Name", "Item ID"
* Input file `price calculator.csv` in the same directory as the python script
* Update global variables for your server/dc/region
  * `mainWorldId` = [your server ID](https://github.com/xivapi/ffxiv-datamining/blob/master/csv/World.csv)
  * `dc` = your datacenter name
  * `region` = your geographic region name

## Tokens
Convert tokens to items for selling. Token type doesn't matter in the calculator. 

#### Requirements:
* Input columns: "Item Name", "Item ID"
