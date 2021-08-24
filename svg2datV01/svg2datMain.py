'''
Author: Joshua Spaander
Year: 2021
Version: 0.1

Discription:
This program opens a simple .svg file and converts it to a simple .dat file. The purpose was to convert 2D patterns from a CAD file to a .dat file for use in
a hotwire cutter. In this version, it simply looks at the points which act as origins of lines and arcs and records those as points. The resulting coordinates
are recorded in a .dat file.

Note: all arcs are treated as cricles.

Version Updates:
User interface through terminal.
Removed packages.
Increased the number of geometeries compatible.
Allows more points to be generated.
Patch:
Fixed bugs and added scaling option for selig files.
'''
import matplotlib.pyplot as plt
import numpy as np
import LineSlicer
import ArcSlicer

#### Startup. ####
print('##################################')
print('\n \n \n')
print('svg2dat: SVG to DAT file converter')
print('\n \n \n')
print('##################################')
print('\n \n \n')

Restart = True
while Restart:
    #### Opening and Reading svg file ####
    print("Which .svg file would you like to convert? (do not include the .svg part)")
    svgFileName = input('File name: ') #'Elevator_central rib'
    svgFileName = svgFileName + '.svg' #'Elevator_central rib.svg'    #File name of svg file.

    Res = int(input('What is your preferred resolution (points per unit length)? '))

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
    indxStart = 0
    indxEnd = 0
    xStr = ''
    yStr = ''
    rxStr = ''
    ryStr = ''
    phiStr = ''
    BigCircleFlagStr = ''
    FlipFlagStr = ''
    datPoints = np.array([[]])
    datPointsx = np.array([[]])
    datPointsy = np.array([[]])
    M = np.array([[]])
    L = np.array([[]])
    A = np.array([[]])

    for line in range(len(svgContLines)):
        if svgContLines[line].find('<path') != -1:
            indxM = svgContLines[line].find('d=\"M ') + 5
            indxL = svgContLines[line].find(' L ')
            indxA = svgContLines[line].find(' A ')

            if indxL != -1 and (indxL < indxA or indxA == -1):
                strLine = svgContLines[line][indxM:indxL]
                xStr , yStr = strLine.split(' ')
                M = np.array([[float(xStr),float(yStr)]])

                indxx = svgContLines[line][indxL+3:-1].find(' ')+indxL+3
                xStr = svgContLines[line][indxL+3:indxx]
                indxy = svgContLines[line][indxx+1:-1].find(' ')+indxx+1
                yStr = svgContLines[line][indxx+1:indxy]
                L = np.array([[float(xStr),float(yStr)]])

                if np.size(datPoints) == 0:
                    datPoints = M
                
                datPoints = np.vstack((datPoints,LineSlicer.SliceLine(M,L,Res)))

            elif indxA != -1 and (indxA < indxL or indxL == -1):
                strLine = svgContLines[line][indxM:indxA]
                xStr , yStr = strLine.split(' ')
                M = np.array([[float(xStr),float(yStr)]])

                indxEnd = svgContLines[line][indxA+3:-1].find(' ')+indxA+3
                rxStr = svgContLines[line][indxA+3:indxEnd]

                indxStart = indxEnd+1
                indxEnd = svgContLines[line][indxStart:-1].find(' ')+indxStart
                ryStr = svgContLines[line][indxStart:indxEnd]

                indxStart = indxEnd+1
                indxEnd = svgContLines[line][indxStart:-1].find(' ')+indxStart
                phiStr = svgContLines[line][indxStart:indxEnd]

                indxStart = indxEnd+1
                indxEnd = svgContLines[line][indxStart:-1].find(' ')+indxStart
                BigCircleFlagStr = svgContLines[line][indxStart:indxEnd]
                
                indxStart = indxEnd+1
                indxEnd = svgContLines[line][indxStart:-1].find(' ')+indxStart
                FlipFlagStr = svgContLines[line][indxStart:indxEnd]
                
                indxStart = indxEnd+1
                indxEnd = svgContLines[line][indxStart:-1].find(' ')+indxStart
                xStr = svgContLines[line][indxStart:indxEnd]
                
                indxStart = indxEnd+1
                indxEnd = svgContLines[line][indxStart:-1].find(' ')+indxStart
                yStr = svgContLines[line][indxStart:indxEnd]
                if yStr.find('\"') != -1:
                    yStr = yStr[0:yStr.find('\"')]
                #rxStr,ryStr,phiStr,BigCircleFlagStr,FlipFlagStr,xStr,yStr = strLine.split(' ')
                ##rx,ry,phi,BigCircleFlag,FlipFlag,A

                A = np.array([[float(xStr),float(yStr)]])
                
                if np.size(datPoints) == 0:
                    datPoints = M

                datPoints = np.vstack((datPoints,ArcSlicer.SliceArc(M,float(rxStr),float(ryStr),float(phiStr),int(BigCircleFlagStr),int(FlipFlagStr),A,Res)))

            else:
                pass

    plt.plot(datPoints[:,0], datPoints[:,1], "o")
    plt.gca().set_aspect('equal')
    plt.show()

    OutputChoice = input('Would you like your .dat file to be in selig format? [y/n]  ')

    #### .dat file writing. ####
    if OutputChoice == 'n' or OutputChoice == 'N':
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
    elif OutputChoice == 'y' or OutputChoice == 'Y':
        yscaling = input('Would you like to scale the y-axis? [y/n]  ')
        if yscaling == 'y' or yscaling == 'Y':
            yscaling = float(input('How much do you wish to scale the y-axis?(float)  '))
        elif yscaling == 'n' or yscaling == 'N':
            yscaling = 1
        else:
            pass
        
        xmin = min(datPoints[:,0])
        xmax = max(datPoints[:,0])
        xavr = sum(datPoints[:,0])/len(datPoints)
        ymin = min(datPoints[:,1])
        ymax = max(datPoints[:,1])
        yavr = sum(datPoints[:,1])/len(datPoints)
        #print(xmin,xmax,ymin,ymax)
        '''
        for line in range(len(datPoints)):
            datPoints[line] = [(datPoints[line][0]-xmin)/(xmax-xmin),(datPoints[line][1]-yavr)/(xmax-xmin)]
            datPointsx[line] = (datPointsx[line]-xmin)/(xmax-xmin)
            datPointsy[line] = (datPointsy[line]-yavr)/(xmax-xmin)
        '''
        datPoints = (datPoints-np.array([[xmin,yavr]]))/np.array([[xmax-xmin,xmax-xmin]])

        datPointsTop = np.array([[0,0]])
        datPointsBottom = np.array([[0,0]])
        
        for line in range(len(datPoints)):
            if datPoints[line][1] >= 0:
                datPointsTop = np.vstack((datPointsTop,datPoints[line]))
            elif datPoints[line][1] < 0:
                datPointsBottom = np.vstack((datPointsBottom,datPoints[line]))
            else:
                pass

        #datPoints = datPoints[np.argsort(datPoints[:,0])]

        datPointsTop = datPointsTop[np.argsort(datPointsTop[:,0])]
        datPointsTop = np.flip(datPointsTop,axis=0)
        datPointsBottom = datPointsBottom[np.argsort(datPointsBottom[:,0])]
        #datPointsBottom = np.flip(datPointsBottom,axis=0)
        datPoints = np.vstack((datPointsTop,datPointsBottom))
        datPoints = np.vstack((np.array([[1.0,0.0]]),datPoints))
        datPoints = np.vstack((datPoints,np.array([[1.0,0.0]])))
        datPoints = np.hstack((np.transpose([datPoints[:,0]]),np.transpose([datPoints[:,1]/yscaling])))

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

    #### Incorrect Input. ####
    else:
        print('Input Error: ', OutputChoice, 'is not a valid response.')

    dummy = True
    while dummy == True:
        print(' ')
        RestartQ = input('Would you like to convert another file? [y/n]')
        if RestartQ == 'y' or RestartQ == 'Y':
            Restart = True
            dummy = False
        elif RestartQ == 'n' or RestartQ == 'N':
            Restart = False
            dummy = False
        else:
            print('Incorrect response detected. Try again! (Not, pressing cntrl+C would end the program.)')
            dummy = True
