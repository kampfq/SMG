Written in python 2.7.3 32-bit.

Installation and packaging
--------------------------
App is frozen to .exe with pyinstaller.
Read more about freezing applications on www.pyinstaller.org
Obviously needs python 2.7.3 32-bit installed.

Requirements
------------
PySide python qt bindings (or pyqt4, with some minimal changes you can convert pyside to pyqt 4)
[https://pypi.python.org/pypi/PySide](more information on pyside)

Pywin32
[http://sourceforge.net/projects/pywin32/](download)
These are the bindings for the win32api to python. 

The rest of the libs used are builtins.

General workings of the program
-------------------------------
Guiv2 has everything associated with the graphical user interface.
Core has everything associated with making the program do what it's supposed to do.
Every program it supports is called a 'token'. 
A token has to be:

- A function inside a programtoken sub-class. (Webbrowser, Webapp, Program or Misc)

- Referenced inside of one of the four dicts at the bottom of the Programtoken class

- Referenced inside of the ITEMS variable in Constants.py. Key = name you want to have shown in the program, value = the name of the token (the function)

The main class has the examine window method, which is the most important method of everything. It analyzes the data gotten through the win32api to determine window titles and classes.

Most of the program is commented, some places a little better than at others, but the comments are there and I hope they're a little helpful at least.

Other
-----
Icon is from http://www.happyiconstudio.com/