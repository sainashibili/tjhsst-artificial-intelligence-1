import sys; args = sys.argv[1:]

boardSize = 8

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
    mainMethod(args)

#main method
def mainMethod(arg):
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

    #make the moves
    if not checkedPos: 
        setPossMoves = possMoves(board, token)
        if not setPossMoves: return print('No moves possible') #no possible moves case

    makeFirstMove(board, token, setPossMoves)
    makeSeveralMoves(move, board, token, setPossMoves)

#prints the board out
def printBoard(board):
    print('\n'.join([''.join(board[i * boardSize : i * boardSize + boardSize]) for i in range(boardSize)]))

#returns all possible moves
def possMoves(board, token):
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

    return posLoc

def flipTokens(board, flipTok, token):
    flippedBoard = [tok for tok in board]
    for i in flipTok: 
        if board[i] != token: flippedBoard[i] = token
    return flippedBoard

def makeFirstMove(board, token, possibleMoves):
    boardStr = [(board[i], '*')[i in possibleMoves] for i in range(boardSize ** 2)]

    printBoard(''.join(boardStr))
    print('\n')
    print(f"{''.join(board)} {boardStr.count('x')}/{boardStr.count('o')}")
    noBracketsPossMoves = ", ".join(str(pos) for pos in possibleMoves)
    print(f"Possible moves for {token}: {noBracketsPossMoves}")

#makes a list of moves, given the list of moves, the original board, and the original possMoves
def makeSeveralMoves(listOfMoves, board, token, possibleMoves):

    if listOfMoves == None: return

    for move in listOfMoves:
        if move != None and move[0].lower() in "abcdefgh":
            move = (int(move[1]) - 1) * boardSize + letterMove[move[0].lower()]

        if int(move) < 0: continue
        possibleMoves, board, token = makeMove(move, board, token, possibleMoves)

        if not possibleMoves: return

#makes a move given a move, board, and token
def makeMove(move, board, token, possibleMoves):

    if move == '55':
        print()

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

    boardStr = [(board[i], '*')[i in possibleMoves] for i in range(boardSize ** 2)]

    printBoard(''.join(boardStr))
    print('\n')
    print(f"{''.join(board)} {boardStr.count('x')}/{boardStr.count('o')}")
    if not possibleMoves:
        return [], [], []
    noBracketsPossMoves = ", ".join(str(pos) for pos in possibleMoves)
    print(f"Possible moves for {token}: {noBracketsPossMoves}\n")

    return possibleMoves, board, token

#makes a move given a move, board, and token and doesn't print out the change in the board
def makeMoveNoPrint(move, board, token, possibleMoves):
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
        possibleMoves2, board2, token2 = makeMoveNoPrint(move, board, token, possibleMoves)
        if len(possibleMoves2) == 0: return move
        else: listOppMoves.append((len(possibleMoves2), move))
    return min(listOppMoves)[1]
    #maxVal = max((len(possibleMoves[i]), i) for i in possibleMoves)[1]

    return maxVal

if __name__ == '__main__': main()

#Saina Shibili, 6, 2023 
