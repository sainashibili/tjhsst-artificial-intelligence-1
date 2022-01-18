import sys; args = sys.argv[1:]
#Saina Shibili
LIMIT_NM = 11

import time

boardSize = 8
negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0

possMovesLookup, negaMaxCache = {}, {}

rowConstraintSet = [{*range(i, i + 8)} for i in range(0, 64, 8)]
colConstraintSet = [{*range(i, 64, 8)} for i in range(8)]
posRowConstraintSet = {i:i//8 for i in range(64)}
posColConstraintSet = {i:i%8 for i in range(64)}

firstDiagonalConstraintSet = [{56}, {48, 57}, {40, 49, 58}, {32, 41, 50, 59}, {24, 33, 42, 51, 60}, {16, 25, 34, 43, 52, 61}, {8, 17, 26, 35, 44, 53, 62}, {0, 9, 18, 27, 36, 45, 54, 63}, {1, 10, 19, 28, 37, 46, 55}, {2, 11, 20, 29, 38, 47}, {3, 12, 21, 30, 39}, {4, 13, 22, 31}, {5, 14, 23}, {6, 15}, {7}]
secondDiagonalConstraintSet = [{0}, {1, 8}, {2, 9, 16}, {3, 10, 17, 24}, {4, 11, 18, 25, 32}, {5, 12, 19, 26, 33, 40}, {6, 13, 20, 27, 34, 41, 48}, {7, 14, 21, 28, 35, 42, 49, 56}, {15, 22, 29, 36, 43, 50, 57}, {23, 30, 37, 44, 51, 58}, {31, 38, 45, 52, 59}, {39, 46, 53, 60}, {47, 54, 61}, {55, 62}, {63}]
posFirstDiagonalConstraintSet = {0:7, 1:8, 2:9, 3:10, 4:11, 5:12, 6:13, 7:14, 8:6, 9:7, 10:8, 11:9, 12:10, 13:11, 14:12, 15:13, 16:5, 17:6, 18:7, 19:8, 20:9, 21:10, 22:11, 23:12, 24:4, 25:5, 26:6, 27:7, 28:8, 29:9, 30:10, 31:11, 32:3, 33:4, 34:5, 35:6, 36:7, 37:8, 38:9, 39:10, 40:2, 41:3, 42:4, 43:5, 44:6, 45:7, 46:8, 47:9, 48:1, 49:2, 50:3, 51:4, 52:5, 53:6, 54:7, 55:8, 56:0, 57:1, 58:2, 59:3, 60:4, 61:5, 62:6, 63:7}
posSecondDiagonalConstraintSet = {0:0, 1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:1, 9:2, 10:3, 11:4, 12:5, 13:6, 14:7, 15:8, 16:2, 17:3, 18:4, 19:5, 20:6, 21:7, 22:8, 23:9, 24:3, 25:4, 26:5, 27:6, 28:7, 29:8, 30:9, 31:10, 32:4, 33:5, 34:6, 35:7, 36:8, 37:9, 38:10, 39:11, 40:5, 41:6, 42:7, 43:8, 44:9, 45:10, 46:11, 47:12, 48:6, 49:7, 50:8, 51:9, 52:10, 53:11, 54:12, 55:13, 56:7, 57:8, 58:9, 59:10, 60:11, 61:12, 62:13, 63:14}

possPaths = [-1, 1, -9, 9, -7, 7, -8, 8]  #left, right, right-up, left-down, left-up, right-down, up, down
row1Border = [0, 1, 2, 3, 4, 5, 6, 7]
col1Border = [0, 8, 16, 24, 32, 40, 48, 56]
col2Border = [7, 15, 23, 31, 39, 47, 55, 63]
row2Border = [56, 57, 58, 59, 60, 61, 62, 63]
border = {0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 39, 47, 55, 63, 58, 59, 60, 61, 62}

cornerSquares = {0, 7, 56, 63}
cornerXSquares = {0:{1, 8, 9}, 7:{6, 14, 15}, 56:{48, 49, 57}, 63:{54, 55, 62}}
letterMove = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

#if it is long --> board, if is 'x' or 'o' --> token, if contains a digit --> move

#main
def main():
    if args:
        #initialize board, token, listOfMoves if given
        board, token, listOfMoves = parseArgs(args)

        #Othello 3
        if listOfMoves != None:
            for move in listOfMoves:
                mv = int(move)
                if mv < 0: continue
                if not possMoves(board, token): token = 'xo'[token == 'x']
                #printBoard(board)
                board = makeMove(mv, board, token, possMoves(board, token))
                token = 'xo'[token == 'x']

        #Othello 4
        if not possMoves(board, token): token = 'xo'[token == 'x']
        printBoard(board)
        print(f"My preferred move is {quickMove(board, token)}")

        #Othello 5
        if board.count('.') < LIMIT_NM:
            optimal = negaMax(board, token) 
            print(f"min score: {optimal[0]} list of moves: {optimal[1:]}")
    else:
        runTournament()


#othello 3 --> parsing through the arguments
def parseArgs(arg):
    #initialize board and the token
    board, token, move = None, None, None
    if len(arg) >= 3:
        #first index 
        if arg[0] in 'xXoO': token = arg[0].lower()
        elif len(arg[0]) == 64: board = arg[0].lower()
        else: move = arg

        #second index
        if arg[1] in 'xXoO': token = arg[1].lower()
        elif len(arg[1]) == 64: board = arg[1].lower()
        elif move == None: move = arg[1:]

        #third index
        if move == None: move = arg[2:]

    if len(arg) == 2:
        #first index 
        if arg[0] in 'xXoO': token = arg[0].lower()
        elif len(arg[0]) == 64: board = arg[0].lower()
        else: move = arg

        #second index
        if arg[1] in 'xXoO': token = arg[1].lower()
        elif len(arg[1]) == 64: board = arg[1].lower()
        else: move = arg[1:]

    elif len(arg) == 1:
        #first index 
        if arg[0] in 'xXoO': token = arg[0].lower()
        elif len(arg[0]) == 64: board = arg[0].lower()
        else: move = arg

    setPossMoves, checkedPos = set(), False
    if board == None: board = '.' * 27 + 'ox......xo' + '.' * 27    #default board
    if token == None:   #default token
        '''
        ************************************************
        DOESN'T CHECK FOR END CASE --> IF BOTH ARE EMPTY
        ************************************************
        '''
        possX = possMoves(board, 'x')
        possO = possMoves(board, 'o')
        if possX and possO:
            numX, numO = board.count('x'), board.count('o')
            if numX % 2 == numO % 2: token = 'x'
            else: token = 'o'
        elif possX and not possO: token, setPossMoves, checkedPos = 'x', possX, True
        else: token, setPossMoves, checkedPos = 'o', possO, True

    return board, token, move

#prints the board out
def printBoard(board):
    print('\n'.join([''.join(board[i * boardSize : i * boardSize + boardSize]) for i in range(boardSize)]))

#returns all possible moves
def possMoves(board, token):
    global possibleMovesCount, negaMaxLookUpCount

    if (board, token) in possMovesLookup: return possMovesLookup[(board, token)]

    possibleMovesCount += 1

    #sets up all the player locs and opposite player locs
    if token == 'x': posTokens, oppLoc = {i for i in range(boardSize ** 2) if board[i] == 'x'}, {i for i in range(boardSize ** 2) if board[i] == 'o'}
    else: oppLoc, posTokens = {i for i in range(boardSize ** 2) if board[i] == 'x'}, {i for i in range(boardSize ** 2) if board[i] == 'o'}

    #posLoc, flipTok = set(), set()
    posLoc = {}

    for myTok in posTokens:
        for direct in possPaths:
            iter = myTok + direct

            while iter >= 0 and iter < 64:
                if iter not in oppLoc: break
                if iter in border:
                    if not (iter in row1Border and myTok in row1Border) and not (iter in row2Border and myTok in row2Border) and not (iter in col1Border and myTok in col1Border) and not (iter in col2Border and myTok in col2Border): break
                    if (direct == 1 or direct == -1) and (not (iter in row1Border and myTok in row1Border) and not (iter in row2Border and myTok in row2Border)): break
                    if (direct == 8 or direct == -8) and (not (iter in col1Border and myTok in col1Border) and not (iter in col2Border and myTok in col2Border)): break
                    if (direct == 9 or direct == -9 or direct == 7 or direct == -7) and (((iter in col1Border and myTok in col1Border) or (iter in col2Border and myTok in col2Border)) or ((iter in row1Border and myTok in row1Border) or (iter in row2Border and myTok in row2Border))) or (iter in col1Border and myTok in col2Border and iter == myTok + direct) or (iter in col2Border and myTok in col1Border and iter == myTok + direct): break
                
                iter += direct
                if iter < 0 or iter >= 64: break

                if iter in col2Border and direct == -1: break
                if iter in col1Border and direct == 1: break

                if board[iter] == '.': 
                    temp = iter
                    while temp != myTok:
                        temp -= direct
                        if iter in posLoc: posLoc[iter].add(temp)
                        else: posLoc[iter] = {temp}
                    break

    possMovesLookup[(board, token)] = posLoc
    return posLoc

def flipTokens(board, flipTok, token):
    flippedBoard = [tok for tok in board]
    for i in flipTok: 
        if board[i] != token: flippedBoard[i] = token
    return flippedBoard

#makes a move given a move, board, and token, then returns the new board
def makeMove(move, board, token, possibleMoves):
    flippedBoard = flipTokens(board, possibleMoves[int(move)], token)
    return ''.join(flippedBoard[:int(move)] + [token] + flippedBoard[int(move) + 1:])

#special makeMove for othello 4 call
def qmMakeMove(move, board, token, possibleMoves):
    #if there is no move, end here
    if move == None: return 
    #if the move isn't valid
    if int(move) not in possibleMoves: 
        print('Move not possible')
        return [], [], []

    #otherwise:
    print(token, "plays to", move)

    flippedBoard = flipTokens(board, possibleMoves[int(move)], token)
    board = flippedBoard[:int(move)] + [token] + flippedBoard[int(move) + 1:]
    if token == 'x': token = 'o'
    else: token = 'x'

    possibleMoves = possMoves(board, token)
    if not possibleMoves:
        p = possMoves(board, ('o', 'x')[token == 'o'])
        if p:
            token = ('o', 'x')[token == 'o']
            possibleMoves = p
    
    return possibleMoves, board, token
#returns the ideal position for the token
def quickMove(board, token):
    possibleMoves = possMoves(board, token)

    for i in cornerSquares:
        if i in possibleMoves: return i
        if board[i] != token: 
            for j in cornerXSquares[i]:
                if j in possibleMoves and len(possibleMoves) > 1: possibleMoves.pop(j)
        else:
            for j in cornerXSquares[i]:
                if j in possibleMoves: return j

    for move in possibleMoves:
        isSafe = True
        for i in rowConstraintSet[posRowConstraintSet[move]]:
            if board[i] == '.' and i != move:
                isSafe = False
                break
        if isSafe: return move
        for i in colConstraintSet[posColConstraintSet[move]]:
            if board[i] == '.' and i != move:
                isSafe = False
                break
        if isSafe: return move
        for i in firstDiagonalConstraintSet[posFirstDiagonalConstraintSet[move]]:
            if board[i] == '.' and i != move:
                isSafe = False
                break
        if isSafe: return move
        for i in secondDiagonalConstraintSet[posSecondDiagonalConstraintSet[move]]:
            if board[i] == '.' and i != move:
                isSafe = False
                break
        if isSafe: return move

    listOppMoves = []
    for move in possibleMoves:
        possibleMoves2, board2, token2 = qmMakeMove(move, board, token, possibleMoves)
        if len(possibleMoves2) == 0: return move
        else: listOppMoves.append((len(possibleMoves2), move))
    return min(listOppMoves)[1]

#runs negamax to determine the optimal move
def negaMax(board, token):
    global negaMaxCount, negaMaxCache, negaMaxLookUpCount
    negaMaxCount += 1

    key = (board, token)
    if key in negaMaxCache: 
        negaMaxLookUpCount += 1
        return negaMaxCache[key]

    eTkn = ('x', 'o')[token == 'x'] #establishes opponent token
    possibleMoves = possMoves(board, token) #possibleMoves

    if '.' not in board or (not possibleMoves and not possMoves(board, eTkn)): 
        returnVal = [board.count(token) - board.count(eTkn)]  #if the game is over, return the score
        negaMaxCache[key] = returnVal
        return returnVal

    elif board.count('.') == 1:   #if there is only one empty space
        for move in possibleMoves: 
            finalBoard = makeMove(move, board, token, possibleMoves) #determines the final board
            returnVal = [finalBoard.count(token) - finalBoard.count(eTkn), move] #returns the score and the final move
            negaMaxCache[key] = returnVal
            return returnVal
    
    if not possibleMoves: best = negaMax(board, eTkn) + [-1]    #if there are no possibleMoves, move to next token and return a pass(-1)
    else: best = min(negaMax(makeMove(move, board, token, possibleMoves), eTkn) + [move] for move in possibleMoves)  #otherwise return the min score of all the possibleMoves
    returnVal = [-best[0]] + best[1:]    #return the best score followed by the best move sequence
    negaMaxCache[key] = returnVal

    return returnVal

def runTournament():
    print()

if __name__ == "main": main()

main()

# print(quickMove('xxxxxxo.xxxoxo.oxxxxooooxoxxoox.xxoxxxxxxxxxoxxoxxxxxxx.xxxxxxx.', 'o'))
# print("Empty spaces:", 'xxxxxxo.xxxoxo.oxxxxooooxoxxoox.xxoxxxxxxxxxoxxoxxxxxxx.xxxxxxx.'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()
# print(quickMove('xxxxxxo.xxxxxo..xxooooooxoxxooooxoxxooooxxxoxoooxxo.oxooxooooooo', 'x'))
# print("Empty spaces:", 'xxxxxxo.xxxxxo..xxooooooxoxxooooxoxxooooxxxoxoooxxo.oxooxooooooo'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()
# print(quickMove('oooxx.x.oxoxx.xx.xxxoxx.oxooxoxo.xoxoxx.xoxoxxx.oooooxxo.oooooxx', 'o'))
# print("Empty spaces:", 'oooxx.x.oxoxx.xx.xxxoxx.oxooxoxo.xoxoxx.xoxoxxx.oooooxxo.oooooxx'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()
# print(quickMove('oooo.ooo.ooooooo.ooooxoooooxoo.oooxxxoo.oooxxxx.oooooxx.ooooo...', 'x'))
# print("Empty spaces:", 'oooo.ooo.ooooooo.ooooxoooooxoo.oooxxxoo.oooxxxx.oooooxx.ooooo...'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()
# print(quickMove('.xoo..xo.xoo.xx.xxxxxoooxxxxooooxxooxoxoxxxxoxxooxxoooxo.x.o.oxx', 'o'))
# print("Empty spaces:", '.xoo..xo.xoo.xx.xxxxxoooxxxxooooxxooxoxoxxxxoxxooxxoooxo.x.o.oxx'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()
# print(quickMove('xxxooo..xxxxoo..xoxoxo.xxxxxxxxoooxoxoooooo.ox.ooooooooooxx.oooo', 'x'))
# print("Empty spaces:", 'xxxooo..xxxxoo..xoxoxo.xxxxxxxxoooxoxoooooo.ox.ooooooooooxx.oooo'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()
# print(quickMove('.xoooo.oxoo.oooxoxooxox.ooxxoxoooooooxoo.oooxx.o.ooooxxo.oooxxxx', 'x'))
# print("Empty spaces:", '.xoooo.oxoo.oooxoxooxox.ooxxoxoooooooxoo.oooxx.o.ooooxxo.oooxxxx'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()

# print(quickMove('....x..oxxoxx.ooxxooxoooxxooxooo.xooxxoxxxxoxoxxxxxooxxxx.xoo.xx', 'x'))
# print("Empty spaces:", 'xxxxxxo.xxxoxo.oxxxxooooxoxxoox.xxoxxxxxxxxxoxxoxxxxxxx.xxxxxxx.'.count('.'), "\nNegamax count:", negaMaxCount, "\nPossible moves count:", possibleMovesCount, "\nNegamax lookup count:", negaMaxLookUpCount)
# negaMaxCount, possibleMovesCount, negaMaxLookUpCount = 0, 0, 0
# print()

#************************************************************
# min score: -48 list of moves: [7, -1, 14, 31, 63, 55]
# Empty spaces: 5 
# Negamax count: 45 
# Possible moves count: 58

# min score: 18 list of moves: [15, -1, 7, -1, 14, -1, 51]
# Empty spaces: 4 
# Negamax count: 28 
# Possible moves count: 36

# min score: 14 list of moves: [16, 32, 39, 23, 13, 47, 5, 56, 7]
# Empty spaces: 9 
# Negamax count: 58202 
# Possible moves count: 60762

# min score: -30 list of moves: [4, -1, 8, 63, 16, 62, 55, 47, 39, 30, 61]
# Empty spaces: 10 
# Negamax count: 617749 
# Possible moves count: 678229

# min score: -6 list of moves: [0, 5, 60, 58, 56, 15, 8, 12, 4]
# Empty spaces: 9 
# Negamax count: 87689 
# Possible moves count: 94962

# min score: -9 list of moves: [6, 14, 22, 15, 46, 43, 59]
# Empty spaces: 8 
# Negamax count: 16046 
# Possible moves count: 16752

# min score: 24 list of moves: [6, -1, 48, -1, 56, -1, 23, 11, 40, 46, 0]
# Empty spaces: 8 
# Negamax count: 26888 
# Possible moves count: 28944
#************************************************************


#Saina Shibili, 6, 2023 
