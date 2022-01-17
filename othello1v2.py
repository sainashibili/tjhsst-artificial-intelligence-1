import sys; args = sys.argv[1:]

boardSize = 8

rowConstraintSet = [{*range(i, i + 8)} for i in range(0, 64, 8)]
colConstraintSet = [{*range(i, 64, 8)} for i in range(8)]

possPaths = [-1, 1, -9, 9, -7, 7, -8, 8]  #left, right, right-up, left-down, left-up, right-down, up, down
row1Border = [0, 1, 2, 3, 4, 5, 6, 7]
col1Border = [8, 16, 24, 32, 40, 48, 56]
col2Border = [15, 23, 31, 39, 47, 55, 63]
row2Border = [57, 58, 58, 60, 61, 62, 63]
border = {0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 39, 47, 55, 63, 58, 58, 60, 61, 62}

#if it is long --> board, if is 'x' or 'o' --> token, if contains a digit --> move

def main(arg):
    #initialize board and the token
    board, token = None, None
    if len(arg) == 2: 
        if arg[0] in 'xXoO': token, board = arg[0].lower(), arg[1].lower()
        else: board, token = arg[0].lower(), arg[1].lower()
    elif len(arg) == 1: 
        if arg[0] in 'xXoO': token = arg[0].lower()
        else:
            board = arg[0].lower()
            # numX, numO = board.count('x'), board.count('o')
            # token = ('o', 'x')[board.count('x') % 2]
    #else: board, token = '.' * 27 + 'ox......xo' + '.' * 27, 'x'
    if board == None: board = '.' * 27 + 'ox......xo' + '.' * 27
    if token == None:
        numX, numO = board.count('x'), board.count('o')
        if numX % 2 == numO % 2: token = 'x'
        else: token = 'o'

    printBoard(board)

    #possible moves method
    setPossMoves = possMoves(board, token)

    #no possible moves case
    if not setPossMoves: return print('No moves possible')

    #replace the board with asterisks
    newBoard = [(board[i], '*')[i in setPossMoves] for i in range(boardSize ** 2)]
    print('Possible moves:', setPossMoves)

def printBoard(board):
    print('\n'.join([board[i * boardSize : i * boardSize + boardSize] for i in range(boardSize)]))

#returns all possible moves
def possMoves(board, token):
    #sets up all the player locs and opposite player locs
    if token == 'x': posTokens, oppLoc = {i for i in range(boardSize ** 2) if board[i] == 'x'}, {i for i in range(boardSize ** 2) if board[i] == 'o'}
    else: oppLoc, posTokens = {i for i in range(boardSize ** 2) if board[i] == 'x'}, {i for i in range(boardSize ** 2) if board[i] == 'o'}

    posLoc = set()

    for myTok in posTokens: #for every possible player position
        for direct in possPaths:  #for every possible path
            addVal = myTok + direct
            valid, isFirst = False, True    #sets the possibility to false, initial closest token to True

            while addVal >= 0 and addVal < 64 and board[addVal] not in border:  #while inbounds
                if addVal not in oppLoc and not isFirst: break  #if the poss token is not the first token and it isn't an opposite token
                isFirst = False #no longer the initial closest token

                if addVal in oppLoc: valid = True   #if path contains an opposing token, is valid
                addVal += direct    #continues the path
                if addVal < 0 or addVal >= 64: break

                if valid and board[addVal] == '.':  #when reaching a dot
                    posLoc.add(addVal)  #add the position
                    break   #break from the loop

    return posLoc


main(args)
#Saina Shibili, 6, 2023 