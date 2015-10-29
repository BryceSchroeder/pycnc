#!/usr/bin/python
# coding: utf-8

import os

import pycnc.core


def get_filepath(dir_='C:/', filename='gcode', extension='.ngc'):
    return os.path.join(os.path.realpath(dir_), filename + extension)

# A : 6k RPM - 3mm drilling bit
# B : 16k RPM - 6mm 1 dent

TOOL_DIAMETER = 6.000
DEPTH_OF_CUT = -1.0
FEED_RATE = 640.000
PLUNGE_RATE = 200.0

PLATE_THICKNESS = 3.000
SAFETY_HEIGHT = 10.000

directory = os.path.abspath(os.path.dirname(__file__))  # create files in the same directory as this script
gcode_file_name = 'A_ExamplePlate_x1_y1_drill3.0_s7000'
f = open(get_filepath(dir_=directory, filename=gcode_file_name), 'w')

f.write(pycnc.core.start_gcode())
    

f.write(pycnc.core.drill(-8.5, -8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(8.5, -8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(8.5, 8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(-8.5, 8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))

f.write(pycnc.core.drill(-19.0, -19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(19.0, -19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(19.0, 19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(-19.0, 19.0, -PLATE_THICKNESS-1.0, SAFETY_HEIGHT, PLUNGE_RATE))

f.write(pycnc.core.drill(-19.0, 0.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(0.0, -19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(19.0, 0.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(pycnc.core.drill(0.0, 19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
    
f.write(pycnc.core.end_gcode())
f.close()
# END OF DRILLING CYCLE


# SQUARE POCKET AND CUT
gcode_file_name = 'B_ExamplePlate_x1_y1_mill6.0_s16000'
f = open(get_filepath(dir_=directory, filename=gcode_file_name), 'w')

f.write(pycnc.core.start_gcode())

f.write(pycnc.core.square_pocket(0.0, 0.0, 25.1, 25.1, TOOL_DIAMETER, FEED_RATE, PLUNGE_RATE, 0.0, -1.5, DEPTH_OF_CUT,
                          SAFETY_HEIGHT))

f.write(pycnc.core.rectangle_rounded_corners(0.0, 0.0, 50.0, 50.0, 3.0, TOOL_DIAMETER, FEED_RATE, PLUNGE_RATE, 0.0,
                                      -PLATE_THICKNESS, DEPTH_OF_CUT, SAFETY_HEIGHT))
    
f.write(pycnc.core.end_gcode())
f.close()
