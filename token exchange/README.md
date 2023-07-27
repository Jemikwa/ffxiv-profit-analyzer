Token Exchanges

Used to calculate how much gil per token you can get for vendor items.
Any token type is supported, so long as the format of the csv meets the requirements:
* Item Name
* Item ID
* Token Type
* Token Cost (how many tokens buying the item requires)
* Sell Price (on your home server)
* Gil Per Token (no values required, will be filled by the script)

I opted to put the outputs in a different directory, but it would be trivial to make the script overwrite the input file too. 