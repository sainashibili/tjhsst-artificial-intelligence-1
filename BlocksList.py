import sys; args = sys.argv[1:]

gHeight, gWidth = 0, 0
gRectDim = []

gAreas, gIsReversed = {}, {}

def readInput(input): #reads the file and sets the width, height, and dimensions of all the rectangles
    global gHeight, gWidth
    if 'x' in input[0]: 
        dim, i = input[0], input[0].index('x')
        gWidth, gHeight = int(dim[:i]), int(dim[i + 1:])
        input = input[1:]
    elif 'X' in input[0]: 
        dim, i = input[0], input[0].index('X')
        gWidth, gHeight = int(dim[:i]), int(dim[i + 1:])
        input = input[1:]
    else: 
        gWidth, gHeight = int(input[0]), int(input[1])
        input = input[2:]
    i = 0
    while i < len(input):
        dim = input[i]
        if 'x' in dim: 
            dim, ind = input[i], input[i].index('x')
            gRectDim.append((int(dim[:ind]), int(dim[ind + 1:])))
            i += 1
            continue
        gRectDim.append((int(dim), int(input[i + 1])))
        i += 2

def solvePuzzle(arg):   #main method
    readInput(arg)
    if solvePuzzleCases(arg): return
    makeAreas(), isReversed()
    pzlSolved = bruteForce([['.' for i in range(gWidth)] for i in range(gHeight)], gRectDim)
    if not pzlSolved: return print("No solution")
    for i in pzlSolved: print(' '.join(i))
    decompose(pzlSolved)

def makeAreas():    #calculates the areas for each rectangle
    global gAreas
    gAreas = {dim : dim[0] * dim[1] for dim in gRectDim}

def isReversed():
    global gIsReversed
    gIsReversed = {dim : False for dim in gRectDim}

def solvePuzzleCases(pzls): #solves puzzles based on a set of fixed cases
    if gRectDim[0][0] == gHeight and gRectDim[0][1] == gWidth and len(gRectDim) == 1: #Rotation case
        print(f'Decomposition: {gWidth}x{gHeight}')
        return True
    heights, widths = [dim[0] for dim in gRectDim], [dim[1] for dim in gRectDim]
    sumHeights, sumWidths, sameHeights, sameWidths = sum(heights), sum(widths), len({*heights}) == 1, len({*widths}) == 1
    if sumHeights == gHeight and sameWidths: #Basics case
        print(f'Decomposition: {gWidth}x{gRectDim[0][0]} {gWidth}x{gRectDim[1][0]}')
        return True
    if sum(gAreas.values()) > gWidth * gHeight:
        print('No solution')
        return True

#returns solved puzzle or empty list on an impossible
def bruteForce(pzl, rect):
    if not rect: return pzl #if there are no more rectangles to fill up the puzzle

    maxVal, maxInd, bestRect = -1, -1, None
    for i, dim in enumerate(rect): 
        if gAreas[dim] > maxVal: maxVal, maxInd, bestRect = gAreas[dim], i, dim  #sets up the max value and the dimensions of the best rect

    for pos in possibleChoices(pzl, bestRect): #all possible positions for the best rectangle
        gIsReversed[bestRect] = pos[2]
        newPzl = addBlock(pzl, bestRect, pos)
        bF = bruteForce(newPzl, rect[:maxInd] + rect[maxInd + 1:]) #recursive call with the newpzl and the rectangle set without the most recently used one
        if bF: return bF #if the recursive call is not empty, return the pzl
    return [] #if parses through every possibility and still fails

#returns all the possible positions of the puzzle
def possibleChoices(pzl, bestRect):
    possChoices = []
    for rowInd, row in enumerate(pzl): #for every row
        for i in range(gWidth): #for every pos
            if row[i] != '.': continue #if the pos is filled --> ignore it
            if i + bestRect[0] <= gWidth and rowInd + bestRect[1] <= gHeight:  #height x width
                isPoss = True
                for j in range(bestRect[1]): #for every column in the possible rect
                    if "".join(pzl[rowInd + j][i: i + bestRect[0]]) != '.' * bestRect[0]:
                        isPoss = False #makes it not possible --> break out of the loop
                        break  
                if isPoss: possChoices.append((rowInd, i, False))  #rowInd, rowPos, isReversed
            if i + bestRect[1] <= gWidth and rowInd + bestRect[0] <= gHeight:  #width x height
                isPoss = True
                for j in range(bestRect[0]): #for every column in the possible rect
                    if ''.join(pzl[rowInd + j][i: i + bestRect[1]]) != '.' * bestRect[1]:
                        isPoss = False #makes it not possible --> break out of the loop
                        break  
                if isPoss: possChoices.append((rowInd, i, True))   #rowInd, rowPos, isReversed
    return possChoices

def addBlock(pzl, rect, pos):   #adds a block onto a puzzle given a position and rectangle
    newPzl, row, rowPos, reverse = [row for row in pzl], pos[0], pos[1], pos[2]
    if reverse:
        for i in range(rect[0]): newPzl[row + i] = newPzl[row + i][:rowPos] + [str(rect[0]) + 'x' + str(rect[1])] * rect[1] + newPzl[row + i][rowPos + rect[1]:]
        return newPzl
    for i in range(rect[1]): newPzl[row + i] = newPzl[row + i][:rowPos] + [str(rect[1]) + 'x' + str(rect[0])] * rect[0] + newPzl[row + i][rowPos + rect[0]:]
    return newPzl

def decompose(pzl):
    seenPos, seenDots, decomposed, s = [], [], [], ''
    for row, val in enumerate(pzl):
        for pos, posVal in enumerate(val):
            if posVal == '.':  #for dots
                if (row, pos) in seenDots: continue
                width, height, done = 1, 1, False
                for x in range(pos + 1, gWidth): #finds width of dot
                    if val[x] == '.': 
                        width += 1
                        seenDots.append((row, x))
                    else: break
                for y in range(row+1, gHeight):   #finds height of dot
                    for w in range(width):
                        if (y, pos + w) != '.': 
                            done = True
                            break
                        seenDots.append(y, pos + w)
                    if not done: height +=1
                    else: break
                decomposed.append(str(height) + 'x' + str(width))
                continue

            if (row, pos) in seenPos: continue
            decomposed.append(posVal)
            height, width = int(posVal[:posVal.index('x')]), int(posVal[posVal.index('x') + 1:])
            for y in range(height):
                for w in range(width):
                    seenPos.append((row + y, pos + w))

            # for rect in gLetters: 
            #     if gLetters[rect] == pos: 
            #         if gIsReversed[rect]: decomposed.append((rect[1], rect[0]))
            #         else: decomposed.append(rect)
            #         seenLetters.append(pos)
            #         break
    print("Decomposition: " + ' '.join(decomposed))

#solvePuzzle(['11X12', '3x6', '2x5', '4x10', '7x9', '1x1'])
solvePuzzle(args)

#Saina Shibili, 6, 2023  