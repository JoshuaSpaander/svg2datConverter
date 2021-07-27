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


HOW TO USE:
Keep all the referred files in the same folder. In this case, svg2datMain.py, LineSlicer and ArcSlicer must be in the same folder directory.

Python 3.9 and the packages matplotlib and numpy must be installed.

Run "svg2datMain.py" to use the program. This can be done by double clicking the file, which will open the comandline/terminal. Then you can follow the instructions given.
The program can also be run in python interpreters such as IDLE, Spyder, Visual Studio, etc...

The program will promt the use to insert the svg file which is to be converted. This can be its plain name if the figure is in the same folder directory. However, when the
svg file is in a different directory, you are required to type this. For subfolders, it is fine to do as follows:

*folder name*/*svg file name*.svg

The python function used to import the svg file is the "open()" function in python. See the documentation to type in what is required.

IMPROTANT NOTE:
svg files work by defining different geometeries. Currently, only circular Arcs and straight Lines are compatible. The rest will either be ignored, move point recorded or 
the program might thow and error. More geometeries will be available in future! But feel free to suggest some pressing ones!