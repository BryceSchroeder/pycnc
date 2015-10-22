# pycnc

[![Ready](http://img.shields.io/badge/Status-ready-669900.svg)](https://github.com/floatingpointstack)
[![Build Status](https://travis-ci.org/floatingpointstack/pycnc.svg)](https://travis-ci.org/floatingpointstack/pycnc)
[![Coverage Status](https://coveralls.io/repos/floatingpointstack/pycnc/badge.svg?branch=master&service=github)](https://coveralls.io/github/floatingpointstack/pycnc?branch=master)
[![GPL v2](http://img.shields.io/badge/license-GPL v2-blue.svg)](https://www.gnu.org/copyleft/gpl.html)
[![OS](http://img.shields.io/badge/OS-Windows Linux OSX-660099.svg)](https://www.python.org/downloads/)
[![Python 2.7 3.*](http://img.shields.io/badge/Python-2.7 3.*-ff3366.svg)](https://www.python.org/downloads/)
[![PEP8](http://img.shields.io/badge/PEP8-OK-00CC00.svg)](https://www.python.org/dev/peps/pep-0008/)

A set of 2.5D CNC Python routines to generate GCode for simple geometries machining on a 3 axis mill or router.


##Getting started

### Install

1. unzip dist/pycnc-0.1.zip (windows) or dist/untar pycnc-0.1.tar.gz (linux)
2. cd into new directory (where setup.py is located)
3. python setup.py install

Copying gcode_generator.py to the same folder as your client scripts is also okay (and simpler) ....

### Use

Please see the examples folder for possible uses. The intended use of pycnc is from another Python script, similar to example_plate.py.

The generated GCode can be visualized and simulated in an open source GCode viewer like [CAMotics](http://camotics.org/download.html)

![example_plate.py generated gcode simulation](images/example_plate_simulation.png)

## Known limitations

pycnc is limited to simple 2.5D shapes. For complex 2D and 3D shapes, [Pycam](http://pycam.sourceforge.net/) is a good free alternative.

## Available GCode generators

To be completed ...

## GCode best practices

[see also](http://linuxcnc.org/docs/html/gcode_overview.html)

- 3 digits after decimal when milling in millimeters, 4 in inches
- consistent white space
- use center-format arcs
- put important modal settings at the top of the file e.g. G17 G20 G40 G49 G54 G80 G90 G94 
- not too many things on a line
- don't set and use a parameter on the same line
- don't use line numbers
- when moving more than one coordinate system, consider inverse time feed mode (G93)
