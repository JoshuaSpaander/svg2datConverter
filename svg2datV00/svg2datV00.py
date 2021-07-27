'''
Author: Joshua Spaander
Year: 2021
Version: 0.0

Discription:
This program opens a simple .svg file and converts it to a simple .dat file. The purpose was to convert 2D patterns from a CAD file to a .dat file for use in
a hotwire cutter. In this version, it simply looks at the points which act as origins of lines and arcs and records those as points. The resulting coordinates
are recorded in a .dat file.
'''
import matplotlib.pyplot as plt
import numpy as np

#### Opening and Reading svg file ####
svgFileName = 'Elevator_central rib.svg'    #File name of svg file.

svgFile = open(svgFileName,'r')             #Opening svg file.
svgContLines = svgFile.read().split('\n')   #Reading file content and splitting by line.
svgFile.close()                             #Closing file

#### Start taking appart the svg file ####
strLine = ''
indxM = 0
indxL = 0
indxA = 0
indxx = 0
indxy = 0
indxEnd = 0
xStr = ''
yStr = ''
datPoints = []
datPointsx = []
datPointsy = []

for line in range(len(svgContLines)):
    if svgContLines[line].find('<path') != -1:
        indxM = svgContLines[line].find('d=\"M ') + 5
        indxL = svgContLines[line].find(' L ')
        indxA = svgContLines[line].find(' A ')

        if indxL != -1 and (indxL < indxA or indxA == -1):
            strLine = svgContLines[line][indxM:indxL]
            xStr , yStr = strLine.split(' ')
            datPoints.append([float(xStr),float(yStr)])
            datPointsx.append(float(xStr))
            datPointsy.append(float(yStr))

        elif indxA != -1 and (indxA < indxL or indxL == -1):
            strLine = svgContLines[line][indxM:indxA]
            xStr , yStr = strLine.split(' ')
            datPoints.append([float(xStr),float(yStr)])
            datPointsx.append(float(xStr))
            datPointsy.append(float(yStr))

        else:
            pass

#### .dat file writing. ####
datContLines = 'Auto-generated .dat file from .svg file by the name of ' + svgFileName + '\n'

for line in range(len(datPoints)):
    datContLines += '  ' + str(datPoints[line][0])[0:8] + '  ' + str(datPoints[line][1])[0:8] + '\n'

datFileName = svgFileName
datFileName = datFileName.replace('svg','dat')
datFileName = datFileName.replace(' ','_')
datFileName = datFileName.replace('_','')
datFile = open(datFileName,'w')
datFile.write(datContLines)
datFile.close()

#### .dat file for selig format. ####
xmin = min(datPointsx)
xmax = max(datPointsx)
xavr = sum(datPointsx)/len(datPointsx)
ymin = min(datPointsy)
ymax = max(datPointsy)
yavr = sum(datPointsy)/len(datPointsy)

for line in range(len(datPoints)):
    datPoints[line] = [(datPoints[line][0]-xmin)/(xmax-xmin),(datPoints[line][1]-yavr)/(xmax-xmin)]
    datPointsx[line] = (datPointsx[line]-xmin)/(xmax-xmin)
    datPointsy[line] = (datPointsy[line]-yavr)/(xmax-xmin)

datPointsTop = np.array([[0,0]])
datPointsBottom = np.array([[0,0]])

datPoints = np.array(datPoints)
print(datPoints)

for line in range(len(datPoints)):
    if datPoints[line][1] >= 0:
        datPointsTop = np.vstack((datPointsTop,datPoints[line]))
    elif datPoints[line][1] < 0:
        datPointsBottom = np.vstack((datPointsBottom,datPoints[line]))
    else:
        pass

'''
datPointsTop = np.sort(datPointsTop,axis=0)
datPointsTop = np.flip(datPointsTop,axis=0)
datPointsBottom = np.sort(datPointsBottom,axis=0)
datPointsBottom = np.flip(datPointsBottom,axis=0)
datPoints = np.vstack((datPointsTop,datPointsBottom))
'''
#datPoints = datPoints[np.argsort(datPoints[:,0])]

datPointsTop = datPointsTop[np.argsort(datPointsTop[:,0])]
datPointsTop = np.flip(datPointsTop,axis=0)
datPointsBottom = datPointsBottom[np.argsort(datPointsBottom[:,0])]
#datPointsBottom = np.flip(datPointsBottom,axis=0)
datPoints = np.vstack((datPointsTop,datPointsBottom))


print('All points')
print(datPoints)
print('Top half')
print(datPointsTop)
print('Bottom half')
print(datPointsBottom)

print(len(datPoints))

plt.plot(datPoints[:,0],datPoints[:,1])#, 'o')
plt.show()

datContLines = '' #'Auto-generated .dat file from .svg file by the name of ' + svgFileName + '\n'

for line in range(len(datPoints)):
    datContLines += '  ' + str(datPoints[line][0])[0:8] + '  ' + str(datPoints[line][1])[0:8] + '\n'

datFileName = 'Selig' + svgFileName
datFileName = datFileName.replace('svg','dat')
datFileName = datFileName.replace(' ','_')
datFileName = datFileName.replace('_','')

datFile = open(datFileName,'w')
datFile.write(datContLines)
datFile.close()