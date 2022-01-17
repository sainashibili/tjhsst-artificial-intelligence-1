coinCache = {}  #key = (amount, *coinList)

def numChange(amount, coinList):
    key = (amount, *coinList)
    if key in coinCache: return coinCache[key]
    if amount < 0: returnVal = 0
    elif amount == 0: returnVal = 1
    elif not coinList: returnVal = 0
    else: returnVal = numChange(amount - coinList[0], coinList) + numChange(amount, coinList[1:])

    coinCache[key] = returnVal
    return returnVal

print(numChange(10000, [100, 50, 25, 10, 5, 1]))

#Saina Shibili, 2023
