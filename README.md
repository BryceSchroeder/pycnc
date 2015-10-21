# pycnc

[![Build Status](https://travis-ci.org/floatingpointstack/pycnc.svg)](https://travis-ci.org/floatingpointstack/pycnc)
[![Coverage Status](https://coveralls.io/repos/floatingpointstack/pycnc/badge.svg?branch=master&service=github)](https://coveralls.io/github/floatingpointstack/pycnc?branch=master)
[![GPL v2](http://img.shields.io/badge/license-GPL v2-blue.svg)](https://www.gnu.org/copyleft/gpl.html)

A set of 2.5D CNC Python routines to generate GCode for simple geometries.

## Install

1. unzip / untar
2. cd into new directory
3. python setup.py install

## Use

Please see the examples folder for possible uses.

For complex 2D and 3D shapes, Pycam is a very good alternative.

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
