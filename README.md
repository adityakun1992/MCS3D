# MCS3D
This is a repository containing my (Aditya Kundety) thesis source code.
This is a software package to serve scientists in the Nanostructures Laboratory at the University of Houston, to assist in printing patterns for Lithography. 

It provides a Scripting environment to design and visualize the patterns. With built in drivers to control the scanner and shutter hardware, software enables the user to automatically print the design.

Due to an arcing problem seen during the operation of the Atom Beam Lithograph, the the serial COM port would intermittently lose communication with the scanner. The 'restartcom.bat' script resets the serial port to restart communication. Detection and reconnection is handled automatically.

The program also includes a small web server using CherryPy, using which the progress can be visuaized and monitored remotely over a mobile device.

A companion [mobile app](https://github.com/adityakun1992/AtomBeamMonitor) can be used to remotely monitor prints.
