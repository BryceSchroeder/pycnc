#!/usr/bin/python
# coding: utf-8

import os

from pycnc import gcode_generator as gcg


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
f = open(gcg.get_filepath(dir_=directory, filename=gcode_file_name), 'w')

f.write(gcg.start_gcode())
    

f.write(gcg.drill(-8.5, -8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(8.5, -8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(8.5, 8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(-8.5, 8.5, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))

f.write(gcg.drill(-19.0, -19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(19.0, -19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(19.0, 19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(-19.0, 19.0, -PLATE_THICKNESS-1.0, SAFETY_HEIGHT, PLUNGE_RATE))

f.write(gcg.drill(-19.0, 0.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(0.0, -19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(19.0, 0.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
f.write(gcg.drill(0.0, 19.0, -PLATE_THICKNESS - 1.0, SAFETY_HEIGHT, PLUNGE_RATE))
    
f.write(gcg.end_gcode())
f.close()
# END OF DRILLING CYCLE


# SQUARE POCKET AND CUT
gcode_file_name = 'B_ExamplePlate_x1_y1_mill6.0_s16000'
f = open(gcg.get_filepath(dir_=directory, filename=gcode_file_name), 'w')

f.write(gcg.start_gcode())

f.write(gcg.square_pocket(0.0, 0.0, 25.1, 25.1, TOOL_DIAMETER, FEED_RATE, PLUNGE_RATE, 0.0, -1.5, DEPTH_OF_CUT,
                          SAFETY_HEIGHT))

f.write(gcg.rectangle_rounded_corners(0.0, 0.0, 50.0, 50.0, 3.0, TOOL_DIAMETER, FEED_RATE, PLUNGE_RATE, 0.0,
                                      -PLATE_THICKNESS, DEPTH_OF_CUT, SAFETY_HEIGHT))
    
f.write(gcg.end_gcode())
f.close()
