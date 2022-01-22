import sys; args = sys.argv[1:]
#Saina Shibili
LIMIT_AB = 12

import time, random

specialCaseCount = 0

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
        print()
        eTkn = 'xo'[token == 'x']
        print(f'{board} {board.count(token)}/{board.count(eTkn)}')
        print(f'Possible moves for {token}: {[*possMoves(board, token)]}')
        print(f"My preferred move is {quickMove(board, token)}")

        #Othello 5
        if board.count('.') < LIMIT_AB:
            optimal = alphabeta(board, token, -64, 64) 
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
        possX = possMoves(board, 'x')
        possO = possMoves(board, 'o')
        if possX and possO:
            numX, numO = board.count('x'), board.count('o')
            if numX % 2 == numO % 2: token = 'x'
            else: token = 'o'
        elif possX and not possO: token, setPossMoves, checkedPos = 'x', possX, True
        else: token, setPossMoves, checkedPos = 'o', possO, True
    
    if move != None and len(move) == 1:
        condensedMoves = move[0]
        move = []
        for i in range(0,len(condensedMoves), 2):
            if '_' in (mv := condensedMoves[i: i + 2]): move.append(mv[1])
            else: move.append(mv)
            
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

#flips the tokens given a board, the tokens to flip, and the token in play
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

    flippedBoard = flipTokens(board, possibleMoves[int(move)], token)
    board = ''.join(flippedBoard[:int(move)] + [token] + flippedBoard[int(move) + 1:])
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

#runs alphabeta to determine the optimal move
def alphabeta(brd, tkn, lowerBound, upperBound):
    global specialCaseCount
    possibleMoves, eTkn = possMoves(brd, tkn), 'xo'[tkn == 'x']

    if not possibleMoves:
        if not possMoves(brd, eTkn): return [brd.count(tkn) - brd.count(eTkn)]
        ab = alphabeta(brd, eTkn, -upperBound, -lowerBound) + [-1]
        return [-ab[0], ab[1:]]

    if brd.count('.') == 1:   #if there is only one empty space
        specialCaseCount += 1
        for move in possibleMoves: 
            finalBoard = makeMove(move, brd, tkn, possibleMoves) #determines the final board
            return [finalBoard.count(tkn) - finalBoard.count(eTkn), move] #returns the score and the final move

    best = [lowerBound - 1]
    for move in possibleMoves:
        ab = alphabeta(makeMove(move, brd, tkn, possibleMoves), eTkn, -upperBound, -lowerBound)
        score = -ab[0]
        if score < lowerBound: continue
        if score > upperBound: return [score] 
        best = [score] + ab[1:] + [move]
        lowerBound = score + 1

    return best

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

#runs 100 games, prints out stats
def runTournament():
    STARTTIME = time.process_time()
    scores, tkn, myTkn, totalTkn, numWins = [], 'x', 0, 0, 0
    for i in range(10):
        tempScores = []
        for j in range(10):
            curScore = playGame(tkn)
            tempScores.append(str(curScore[0]))
            scores.append(curScore)
            myTkn += curScore[2].count(tkn)
            totalTkn += len(curScore[2].replace('.', ''))
            if curScore[0] > 0: numWins += 1
            tkn = "xo"[tkn == 'x']
        print(' '.join(tempScores))
        tempScores = []

    print(f'\nMy tokens: {myTkn}; Total tokens: {totalTkn}')
    print(f'Score: {myTkn/totalTkn:.1%}')
    print(f"NM/AB LIMIT: {LIMIT_AB}")

    minScore = min(scores)
    minIndex = scores.index(minScore)
    minTkn = 'xo'[minIndex % 2]
    print(f'Game {minIndex + 1} as {minTkn} => {minScore[0]}:\n {minScore[1]}')

    scores.remove(minScore)
    minScore = min(scores)
    minIndex = scores.index(minScore)
    minTkn = 'xo'[minIndex % 2]
    print(f'Game {minIndex + 1} as {minTkn} => {minScore[0]}:\n {minScore[1]}')

    print(f'Elapsed time: {round(time.process_time() - STARTTIME, 1)}s')

#runs a singular game, returns the score, transcript, and board
def playGame(tkn):
    brd = '.' * 27 + 'ox......xo' + '.' * 27
    curTkn = 'x'
    transcript = []

    while True:
        if not (moves := possMoves(brd, curTkn)):
            curTkn = 'xo'[curTkn == 'x']
            if not(moves := possMoves(brd, curTkn)): break
            transcript.append(-1)
        if curTkn != tkn:
            transcript.append(random.choice([*moves]))
            brd = makeMove(transcript[-1], brd, curTkn, moves)
        else:
            if brd.count('.') < LIMIT_AB: transcript.append(alphabeta(brd, curTkn, -64, 64)[-1])
            else: transcript.append(quickMove(brd, curTkn))
            brd = makeMove(transcript[-1], brd, curTkn, moves)
        curTkn = 'xo'[curTkn == 'x']

    score = brd.count(tkn) - brd.count('xo'[tkn == 'x'])
    xscript = ''.join([f'_{mv}'[-2:] for mv in transcript])

    return (score, xscript, brd)

if __name__ == "__main__": main()
print("Special Case Count: ", specialCaseCount)

#Saina Shibili, 6, 2023 
