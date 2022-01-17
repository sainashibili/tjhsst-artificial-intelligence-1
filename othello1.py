import sys; args = sys.argv[1:]

'''
***************
WORKING VERSION
***************
'''
boardSize = 8

rowConstraintSet = [{*range(i, i + 8)} for i in range(0, 64, 8)]
colConstraintSet = [{*range(i, 64, 8)} for i in range(8)]

possPaths = [-1, 1, -9, 9, -7, 7, -8, 8]  #left, right, right-up, left-down, left-up, right-down, up, down
row1Border = [0, 1, 2, 3, 4, 5, 6, 7]
col1Border = [0, 8, 16, 24, 32, 40, 48, 56]
col2Border = [7, 15, 23, 31, 39, 47, 55, 63]
row2Border = [56, 57, 58, 59, 60, 61, 62, 63]
border = {0, 1, 2, 3, 4, 5, 6, 7, 8, 16, 24, 32, 40, 48, 56, 15, 23, 31, 39, 47, 55, 63, 58, 59, 60, 61, 62}

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

    for myTok in posTokens:
        for direct in possPaths:
            iter = myTok + direct

            if myTok == 57 and direct == -1:
                print()

            while iter >= 0 and iter < 64:
                if iter not in oppLoc: break
                if iter in border:
                    if not (iter in row1Border and myTok in row1Border) and not (iter in row2Border and myTok in row2Border) and not (iter in col1Border and myTok in col1Border) and not (iter in col2Border and myTok in col2Border): break
        
                    if (direct == 1 or direct == -1) and (not (iter in row1Border and myTok in row1Border) and not (iter in row2Border and myTok in row2Border)): break
                    if (direct == 8 or direct == -8) and (not (iter in col1Border and myTok in col1Border) and not (iter in col2Border and myTok in col2Border)): break
                    if (direct == 9 or direct == -9 or direct == 7 or direct == -7) and ((not (iter in col1Border and myTok in col2Border) and not (iter in col1Border and myTok in col2Border))): break
                iter += direct
                if iter < 0 or iter >= 64: break

                if iter in col2Border and direct == -1: break
                if iter in col1Border and direct == 1: break
                
                # if iter in border:
                #     if not (iter in row1Border and myTok in row1Border) and not (iter in row2Border and myTok in row2Border) and not (iter in col1Border and myTok in col1Border) and not (iter in col2Border and myTok in col2Border): break
                #     if (direct == 1 or direct == -1) and (not (iter in row1Border and myTok in row1Border) and not (iter in row2Border and myTok in row2Border)): break
                #     if (direct == 8 or direct == -8) and (not (iter in col1Border and myTok in col1Border) and not (iter in col2Border and myTok in col2Border)): break
                #     if (direct == 9 or direct == -9 or direct == 7 or direct == -7) and ((not (iter in col1Border and myTok in col2Border) and not (iter in col1Border and myTok in col2Border))): break
                if board[iter] == '.': 
                    posLoc.add(iter)
                    break

    return posLoc

main(args)
#Saina Shibili, 6, 2023 