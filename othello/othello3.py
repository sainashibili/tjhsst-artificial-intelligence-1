import sys; args = sys.argv[1:]

boardSize = 8

possPaths = [-1, 1, -9, 9, -7, 7, -8, 8]  #left, right, right-up, left-down, left-up, right-down, up, down
row1Border = [0, 1, 2, 3, 4, 5, 6, 7]
col1Border = [0, 8, 16, 24, 32, 40, 48, 56]
col2Border = [7, 15, 23, 31, 39, 47, 55, 63]
row2Border = [56, 57, 58, 59, 60, 61, 62, 63]
border = {0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 39, 47, 55, 63, 58, 59, 60, 61, 62}

letterMove = {'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}

#if it is long --> board, if is 'x' or 'o' --> token, if contains a digit --> move

#main method
def main(arg):
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

main(args)
#Saina Shibili, 6, 2023 
