import sys; args = sys.argv[:1]
import random
from moveFastD import findMoves, makeMove, getDefaultMove as findBestMove

def show2D(brd, tkn, mv, findMovesFunc):
    #Display a snapshot:
    #Move played, 2D board, 1D board w. score, psbl moves
    #brd is a string, tkn just moved to mv
    next = 'xo'[tkn=="x"]
    psblMv = findMovesFunc(brd, next)
    if not psblMv:
        psblMv = findMovesFunc(brd, (next:=tkn))
    brdL = [*brd]
    for m in psblMv: brdL[m] = "*"
    brdL[mv] = brdL[mv].upper()
    b2 = "".join(brdL)
    print(f"'{tkn}' played to {mv}")
    print("\n".join([b2[rs:rs+8] for rs in range(0,len(b2),8)]))
    print(f"\n{brd} {brd.count('x')}/{brd.count('o')}")
    if psblMv:          # If game not over, show possible moves
        print(f"Possible moves for '{next}': {sorted([*psblMv])}\n")

def playGame(findBestMove, findMoves, makeMove, token):
    # plays a game between findBestMove and Random
    # findMove(brd, tkn)
    # findBestMove(brd, tkn, psblMoves)
    # makeMove(brd, tkn, mv, psblMoves)
    # Csaba Gabor, 10 Dec 2021

    brd = '.'*27+'ox......xo'+'.'*27    # Starting board
    tknToPlay = 'x'
    transcript = [] # Transcript of the game

    while True:
        if not (moves:=findMoves(brd, tknToPlay)):
            tknToPlay = 'xo'[tknToPlay=='x']    # Swap players if pass
            if not (moves:=findMoves(brd, tknToPlay)): break
            transcript.append(-1)   # Note the pass
        if tknToPlay != token:  # if it's Random's turn:
            transcript.append(random.choice([*moves]))
            brd = makeMove(brd, tknToPlay, transcript[-1], moves)
            show2D(brd, tknToPlay, transcript[-1], findMoves)
        else:   # else it's Our turn
            transcript.append(findBestMove(brd, tknToPlay, moves))
            brd = makeMove(brd, tknToPlay, transcript[-1], moves)
            show2D(brd, tknToPlay, transcript[-1], findMoves)
            brd = brd.lower()   # Just in case
            tknToPlay = 'xo'[tknToPlay=='x']    #Switch to the other side
    
    # Game is over
    tknCt = brd.count(token)
    enemy = len(brd) - tknCt - brd.count('.')
    print(f"\nScore: Me as {token=}: {tknCt} vs Enemy: {enemy}\n")
    xscript = [f"_{mv}"[-2:] for mv in transcript]
    print(f"Game transcript: {''.join(xscript)}")

playGame(findBestMove, findMoves, makeMove, args[0])
   
    
 