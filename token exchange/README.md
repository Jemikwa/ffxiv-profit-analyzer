# Token Exchanges

Used to calculate how much gil per token you can get for vendor items.
Any token type is supported, so long as the format of the csv meets the requirements:
* Item Name
* Item ID
* Token Type
* Token Cost (how many tokens buying the item requires)
You could even put every item/token in a single spreadsheet. The script will handle multiple token types per item and over 100 item queries without any issue. 

All files in project/inputs/ will be read and processed one at a time. For each file read, a new file will be created/updated in project/outputs/. 
I opted to put the outputs in a different directory, but it would be trivial to make the script overwrite the input file too.
