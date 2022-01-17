import sys; args = sys.argv[1:]

#Saina Shibili, 6, 2023

import tkinter as tk
import time

from math import pi , acos , sin , cos
from queue import PriorityQueue

START_TIME = time.process_time()

LOCATIONFILE = "/Users/saina/Documents/School/AI Code/Railroads/rrNodes.txt"
EDGEFILE = "/Users/saina/Documents/School/AI Code/Railroads/rrEdges.txt"
CITIESFILE = "/Users/saina/Documents/School/AI Code/Railroads/rrNodeCity.txt"


gLatLong = {}
gNeighbors = {}
gNames = {}

#tKinter drawings
root = tk.Tk()    #window
bg = tk.PhotoImage(file="/Users/saina/Documents/School/AI Code/Railroads/NorthAmerica.png") #bg image

canvas = tk.Canvas(root, height=1687, width=1159, bg='white')   #set canvas, height, width, bg color
canvas.create_image(0, 0, image = bg, anchor="nw")  #add bg image to canvas

canvas.update()
cWidth = canvas.winfo_reqwidth() / 90   #width scale
cHeight = canvas.winfo_reqheight() / 85 #height scale

#aStar to find the path
def aStar(start, goal):
    count = 0

    if start == goal: return [start]
    
    openSet = PriorityQueue() #priority Queue, (fVal, station)
    openSet.put((callEstimateDist(start, goal), start))
    closedSet = {}  #station : level

    while not openSet.empty():

        count += 1
        if count == 50:
            canvas.update()
            count = 0

        fVal, station = openSet.get() 

        if station in closedSet: continue
        closedSet[station] = fVal - callEstimateDist(station, goal) #fVal - 3d distance of pzl to goal == gVal
        drawClosedSetPoint(station)

        if station == goal: 
            return buildPath(closedSet, start, goal) 

        for nbr in neighbors(station): 
            if nbr in closedSet: continue
            openSet.put((closedSet[station] + callEstimateDist(station, nbr) + callEstimateDist(nbr, goal), nbr)) #3d distance of nbr to goal
            drawOpenSetLine(station, nbr)

def drawOpenSetLine(station, nbr):
    canvas.create_line(latLong(station), latLong(nbr), fill="red")

def drawClosedSetPoint(station):
    lat, long = latLong(station)
    canvas.create_oval(lat - 1, long - 1, lat + 1, long + 1, fill="blue", width=0)

#reconstructs path based on closedSet values
def buildPath(closedSet, start, goal):
    path = [goal]

    station = goal

    while station != start:
        for nbr in neighbors(station):
            if nbr == start or (nbr in closedSet and closedSet[nbr] < closedSet[station]):
                station = nbr
                path.append(nbr)
    
    return path[::-1]

#reads in neighbors file
def readNeighbors(fileName):    
    global gNeighbors
    for station in open(fileName, 'r').read().splitlines():
        listStation = station.split(" ")
        if listStation[0] in gNeighbors:
            gNeighbors[listStation[0]].append(listStation[1])
        else:
            gNeighbors[listStation[0]] = [listStation[1]]
        if listStation[1] in gNeighbors:
            gNeighbors[listStation[1]].append(listStation[0])
        else:
            gNeighbors[listStation[1]] = [listStation[0]]

#reads in latitude and longitude information
def readLatLong(fileName):  
    global gLatLong
    for station in open(fileName, 'r').read().splitlines():
        listStation = station.split(" ")
        gLatLong[listStation[0]] = [listStation[1], listStation[2]]

#reads in the city names
def readCityNames(fileName):    
    global gNames
    for station in open(fileName, 'r').read().splitlines():
        listStation = station.split(" ")
        gNames[listStation[1]] = listStation[0]


#returns neighbors, if station has any
def neighbors(station):
    global gNeighbors
    if station in gNeighbors: return gNeighbors[station]
    return []

#calls heuristic using two stations
def callEstimateDist(val1, val2):
    global gLatLong
    lat1, long1 = gLatLong[val1]
    lat2, long2 = gLatLong[val2]
    return estimateDist(lat1, long1, lat2, long2)

#hVal, 3d distance of point A to point B
def estimateDist(lat1, long1, lat2, long2): 

    lat1  = float(lat1) * (pi/180.0)
    long1  = float(long1) * (pi/180.0)
    lat2  = float(lat2) * (pi/180.0)
    long2  = float(long2) * (pi/180.0)

    R   = 3958.76

    return acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(long1-long2)) * R

#find x and y coordinate on map based on lat long
def latLong(station):   
    lat, long = gLatLong[station]
    return (cWidth * (140 + float(long)), cHeight * (60 - float(lat)))

#draws path for aStar
def makePath(path): 
    for i in range(len(path) - 1):
        canvas.create_line(latLong(path[i]), latLong(path[i + 1]), fill="black", width=5)
        if i % 5 == 0: canvas.update()
    canvas.update()

def main(args):

    readLatLong(LOCATIONFILE)
    readNeighbors(EDGEFILE)
    readCityNames(CITIESFILE)

    if args[0] in gNames: start = gNames[args[0]]
    else: start = args[0]
    if args[1] in gNames: end = gNames[args[1]]
    else: end = args[1]

    canvas.pack(fill = "both", expand = True)
    path = aStar(start, end)
    root.update()

    makePath(path)

    print("Path length:", len(path))
    print(callEstimateDist(path[0], path[-1]))

    print(time.process_time() - START_TIME)

#main(args)
main(["Chicago", "Vancouver"])

root.mainloop()




