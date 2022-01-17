import sys; args = sys.argv[1:]
pzls = open(args[0], 'r').read().splitlines()
#pzls = open("/Users/saina/Documents/School/AI Code/Sudoku/puzzles.txt").read().splitlines()


import math, time


gSide, gHeight, gWidth = 9, 3, 3

gSymbolSet = {}

#reads in puzzles and calls solve puzzle on each of them
def readFile(pzls):
    global gSymbolSet

    setDimensions(pzls[0])

    for i, pzl in enumerate(pzls):
        start_time = time.process_time()
        solvedPzl = solvePuzzle(pzl)
        print(i + 1,":", pzl)
        print("".join([" "] * len(str(i + 1))), " ", solvedPzl, checkSum(solvedPzl), time.process_time() - start_time)

#solves the puzzle
def solvePuzzle(pzl):
    makeSymbolSet(pzl)
    return bruteForce(pzl)

#sets global side dimension and the height and width of the sub block
def setDimensions(pzl):
    global gSide
    gSide = int(math.sqrt(len(pzl)))

#finds factors of len(puzzle)
def factors(puzzle):    
    return {i : len(puzzle) / i for i in range(1, int(len(puzzle)**0.5)+1) if len(puzzle) % i == 0}

#sets the possible symbols of the puzzle
def makeSymbolSet(pzl):
    global gSymbolSet
    gSymbolSet = {*"123456789"}
    gSymbolSet.update(*pzl.replace(".", ""))

#checks the sum of ascii vals for each char - len(pzl) * ascii val of min char
def checkSum(pzl):
    asciiVals = [ord(ch) for ch in pzl]
    return sum(asciiVals) - len(pzl) * min(asciiVals)

#returns a list with all the rows
def makeRows(pzl):
    return [pzl[i * gSide : i * gSide + gSide] for i in range(gSide)]

#returns a list with all the cols
def makeColumns(pzl):
    col = [""] * gSide
    for i in range(gSide):
        for j in range(gSide):
            col[i] += pzl[i + j * gSide]
    return col

#returns a list with all the sub-blocks
def makeSubBlocks(pzl):
    subBlocks = [
        pzl[:3] + pzl[9:12] + pzl[18:21],
        pzl[3:6] + pzl[12:15] + pzl[21:24],
        pzl[6:9] + pzl[15:18] + pzl[24:27],
        pzl[27:30] + pzl[36:39] + pzl[45:48],
        pzl[30:33] + pzl[39:42] + pzl[48:51],
        pzl[33:36] + pzl[42:45] + pzl[51:54],
        pzl[54:57] + pzl[63:66] + pzl[72:75],
        pzl[57:60] + pzl[66:69] + pzl[75:78],
        pzl[60:63] + pzl[69:72] + pzl[78:81]
    ]
    return(subBlocks)

#determines if the sudoku cannot be solved
def isImpossible(pzl):
    for row in makeRows(pzl):
        if len({*row.replace(".", "")}) < len(row.replace(".", "")):
            return True
    for col in makeColumns(pzl):
        if len({*col.replace(".", "")}) < len(col.replace(".", "")):
            return True
    for block in makeSubBlocks(pzl):
        if len({*block.replace(".", "")}) < len(block.replace(".", "")):
            return True
    return False

#return solved puzzle or empty string on failure
def bruteForce(pzl):
    if isImpossible(pzl): return "" #if puzzle fails, return an empty string
    if pzl.find(".") == -1: return pzl #if puzzle is filled out(and correc), return the pzl

    for ch in gSymbolSet: #all possible symbols
        subPzl = pzl[:pzl.find('.')] + ch + pzl[pzl.find('.') + 1:] #replaces first period with char
        bF = bruteForce(subPzl) #recursive call with subpzl
        if bF: return bF #if the recursive call is not empty, return the pzl
    return "" #if parses through every possibility and still fails

#prints out puzzle 
def printPuzzle(pzl):  
    row = [""] * gHeight

    for i in range(len(pzl)//gSide):
        for j in range(len(pzl)//gSide):
            row[i % 3] += pzl[i * gSide + j]
            if (j + 1) % 3 == 0:
                row[i % 3] += " "
        if (i + 1) % 3 == 0:
            print("\n".join(row) + "\n")
            row = [""] * gHeight
    

readFile(pzls)

#Saina Shibili, 6, 2023