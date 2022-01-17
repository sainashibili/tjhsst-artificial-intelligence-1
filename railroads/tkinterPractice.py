#Saina Shibili, period 6

import tkinter as tk

path = ['3500060', '3500104', '3500083', '3500103', '3500147', '3500029', '3500108', '3500058', '3500082', '3500074', '3500034', '3500075', '3500057', '0000131', '0800091', '0800090', '0800119', '0800086', '0800265', '0800248', '0800269', '0800270', '0800271', '0800187', '0800087', '0800281', '0800125', '0800100', '0800083', '0800209', '0800307', '0800283', '0800208', '0800197', '0800196', '0800101', '0800126', '0800198', '0800189', '0800127', '0800305', '0800082', '0800304', '0800303', '0800104', '0800230', '0800105', '0800067', '0800065', '0800133', '0800110', '0800138', '0800137', '0800293', '0800286', '0800106', '0800064', '0800112', '0800185', '0800186', '0800054', '0800296', '0800136', '0800200', '0800308', '0800252', '0800005', '0800213', '0800006', '0800003', '0800004', '0800227', '0800228', '0000352', '3100269', '3100142', '3100206', '3100337', '3100119', '3100230', '3100231', '3100295', '3100400', '3100239', '3100238', '3100199', '3100402', '3100233', '3100115', '3100114', '3100250', '0000123', '4600133', '4600087', '4600086', '4600091', '4600056', '4600076', '4600075', '4600060', '4600066', '4600036', '4600127', '4600065', '4600023', '4600089', '4600025', '4600073', '4600026', '4600115', '4600114', '4600113', '4600028', '4600027', '4600092', '4600138', '4600041', '0000360', '3800198', '3800248', '3800197', '3800004', '3800257', '3800258', '3800003', '3800026', '3800024', '3800023', '3800166', '3800022', '0000552', '2700520', '2700344', '2700139', '2700343', '2700345', '2700526', '2700348', '2700145', '2700152', '2700161', '2700350', '2700153', '2700553', '2700504', '2700209', '2700537', '2700225', '2700535', '0009274', '8800449', '8802395', '8802396', '8801746', '8801745', '8801456', '8801457', '8801736', '8801735', '8800443', '8801107', '8801752', '8801732', '8801752']

LOCATIONFILE = "/Users/saina/Documents/School/AI Code/Railroads/rrNodes.txt"
EDGEFILE = "/Users/saina/Documents/School/AI Code/Railroads/rrEdges.txt"
CITIESFILE = "/Users/saina/Documents/School/AI Code/Railroads/rrNodeCity.txt"

gLatLong = {}
gNeighbors = {}
gNames = {}

lines = []

def readNeighbors(fileName):    #reads in neighbors file
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


def readLatLong(fileName):  #reads in latitude and longitude information
    global gLatLong
    for station in open(fileName, 'r').read().splitlines():
        listStation = station.split(" ")
        gLatLong[listStation[0]] = [listStation[1], listStation[2]]

def readCityNames(fileName):    #reads in the city names
    global gNames
    for station in open(fileName, 'r').read().splitlines():
        listStation = station.split(" ")
        gNames[listStation[1]] = listStation[0]

def drawLine(pointA, pointB):
    line = canvas.create_line(pointA, pointB, fill="red", tag="pathline")
    lines.append(line)

def latLong(station):

    # canvas.update()

    # width = canvas.winfo_reqwidth()
    # height = canvas.winfo_reqheight()

    lat, long = gLatLong[station]

    print(cWidth * (140 + float(long)), cHeight * (60 - float(lat)))
    return (cWidth * (140 + float(long)), cHeight * (60 - float(lat)))

    # print((width/90) * (140 + float(long)), (height/40) * (60 - float(lat)))
    # return ((width/90) * (140 + float(long)), (height/40) * (60 - float(lat)))

def make_red(r, c): #makes all the lines red
	for line in lines:
		c.itemconfig(line, fill="red") #changes color of one line to red
		r.update() #update frame
		#time.sleep(0.1)

readLatLong(LOCATIONFILE)
readNeighbors(EDGEFILE)
readCityNames(CITIESFILE)

root = tk.Tk()    #window

bg = tk.PhotoImage(file="/Users/saina/Documents/School/AI Code/Railroads/NorthAmerica.png")

canvas = tk.Canvas(root, height=1687, width=1159, bg='white')

canvas.create_image(0, 0, image = bg, anchor="nw")

canvas.update()

cWidth = canvas.winfo_reqwidth() / 90
cHeight = canvas.winfo_reqheight() / 85

for i in range(len(path) - 1):
    drawLine((latLong(path[i])), latLong(path[i + 1]))

canvas.pack(fill = "both", expand = True)

#make_red(root, canvas)

root.mainloop()