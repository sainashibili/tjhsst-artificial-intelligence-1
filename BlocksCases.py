import sys; args = sys.argv[1:]

gHeight, gWidth = 0, 0
gRectDim = []

def readInput(input): #reads the file and sets the width, height, and dimensions of all the rectangles
    global gHeight, gWidth
    if 'x' in input[0]: 
        dim, i = input[0], input[0].index('x')
        gHeight, gWidth = int(dim[:i]), int(dim[i + 1:])
        input = input[1:]
    elif 'X' in input[0]: 
        dim, i = input[0], input[0].index('X')
        gHeight, gWidth = int(dim[:i]), int(dim[i + 1:])
        input = input[1:]
    else: 
        gHeight, gWidth = int(input[0]), int(input[1])
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
    

def solvePuzzleCases(pzls): #solves puzzles based on a set of fixed cases
    if gRectDim[0][0] == gWidth and gRectDim[0][1] == gHeight and len(gRectDim) == 1: #Rotation case
        print(f'Decomposition: {gHeight}x{gWidth}')
        return True
    heights, widths = [dim[0] for dim in gRectDim], [dim[1] for dim in gRectDim]
    sumHeights, sumWidths, sameHeights, sameWidths = sum(heights), sum(widths), len({*heights}) == 1, len({*widths}) == 1
    if sumHeights == gWidth and sameWidths: #Basics case
        print(f'Decomposition: {gHeight}x{gRectDim[0][0]} {gHeight}x{gRectDim[1][0]}')
        return False
    print('No solution')
    

readInput(args)
solvePuzzleCases(args)

    

#Saina Shibili, 6, 2023