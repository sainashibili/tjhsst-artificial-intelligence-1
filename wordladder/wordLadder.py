import sys; args = sys.argv[1:]
#wordList = open(args[0], 'r').read().splitlines()

args = ["/Users/saina/Documents/HW/AI Code/wordLadder/dict.txt", "abased", "abases"]
wordList = open(args[0], 'r').read().splitlines()

#wordList = open("/Users/saina/Documents/HW/AI Code/wordLadder/dict.txt", 'r').read().splitlines()
wordList = set(wordList)    #set so it's hash codes --> faster than list

import time

START_TIME = time.process_time()    #marks the start time

def makeGraph(word):
    return {g : neighbors(g) for g in word} #every word : word's neighbors

def neighbors(word):
    temp = {word[:ch] + letter + word[ch + 1:] for ch in range(len(word)) for letter in set("abcdefghijklmnopqrstuvwxyz")}  #every possible combination
    return [i for i in wordList if i in temp and i != word and len(word) == len(i)]

def wordCount():
    return len(wordList)

def edgeCount(graph):
    return sum(len(i) for i in graph.values())//2

def degreeList(graph):
    degrees = {}
    #for all the values in the graph, if there is already a val at that index, count++, else set count to 1
    for i in graph.values(): degrees.update({len(i) : degrees.get(len(i)) + 1}) if len(i) in degrees else degrees.update({len(i) : 1}) 
    temp = []
    #convert dict to a list
    for i in range(max(degrees) + 1): temp.append(0) if not i in degrees else temp.append(degrees.get(i))
    return temp

def secondDegree(graph, deg):
    if deg[-2] != 0: secondDeg = len(deg) - 2
    else:
        for i in range(1, len(deg) - 2):
            if deg[-2 - i] != 0:
                secondDeg = i
                break
    for i in graph:
        if len(graph.get(i)) == secondDeg:
            return i

def findConnectComp(graph):
    seen = dict.fromkeys(graph.keys(), -1)
    connectComp = []
    index = 0
    for i in graph:
        if seen.get(i) == -1:
            connectComp.append([i])
            recurHelper(i, seen, graph, connectComp, index)
            index += 1
    return connectComp
    

def recurHelper(vertex, seen, graph, connectComp, index):
    seen.update({vertex : 1})
    for i in graph.get(vertex):
        if seen.get(i) == -1:
            connectComp[index].append(i)
            recurHelper(i, seen, graph, connectComp, index)

def kN(connectComp, graph):
    count2 = 0
    count3 = 0
    count4 = 0
    for i in connectComp:
        if len(i) == 2:
            if i[0] in graph.get(i[1]):
                count2 += 1
        elif len(i) == 3:
            if i[0] in graph.get(i[1]) and i[0] in graph.get(i[2]) and i[1] in graph.get(i[2]):
                count3 += 1
        elif len(i) == 4:
            if i[0] in graph.get(i[1]) and i[0] in graph.get(i[2]) and i[0] in graph.get(i[3]) and i[1] in graph.get(i[2]) and i[1] in graph.get(i[3]) and i[2] in graph.get(i[3]):
                count4 += 1
    return [count2, count3, count4]

def pathFirstSecond(first, second, graph):
    return BFS(first, second, graph)
    
        
def BFS(start, goal, graph):   #breadth first search methods
    if start == goal: return [start]
    parseMe, seenItems = [start], {start : None}
    for i in parseMe:
        for j in graph.get(i):
            if(not j in seenItems):
                parseMe.append(j)
                seenItems.update({j : i})
                if j == goal:
                    temp = [j]
                    while(j in seenItems and seenItems.get(j) != None):
                        temp.append(j := seenItems.get(j))
                    return temp[::-1]
    return []    

def farthestWord(start, connectComp, graph):
    index = 0
    pathLength = {}
    for i in range(len(connectComp)):
        if start in connectComp[i]:
            index = i
            break
    for i in connectComp[index]:
        pathLength.update({len(BFS(start, i, graph)): i})
    return pathLength.get(max(pathLength))


def makeLadder():
    graph = makeGraph(wordList)
    print("Word count: ", wordCount())
    print("Edge count: ", edgeCount(graph))
    print("Degree list: ", dL := degreeList(graph))
    if len(args) >= 3:
        print("Second degree word: ", secondDegree(graph, dL))
        print("Neighbors: ", graph.get(args[1]))
        connectComp = findConnectComp(graph)
        countCC = {len(i) for i in connectComp}
        print("Connected component size count: ", len(countCC))
        print("Largest component size: ", max(countCC))
        print("K2 count: ", (kSize := kN(connectComp, graph))[0], "\nK3 count: ", kSize[1], "\nK4 count: ", kSize[2])
        print("Path: ", pathFirstSecond(args[1], args[2], graph))
        print("Farthest: ", farthestWord(args[1], connectComp, graph))

makeLadder()

END_TIME  = time.process_time() -  START_TIME
print("Construction Time: {}s".format(f"{END_TIME :.3g}"))

#Saina Shibili, pd 6, 2023

