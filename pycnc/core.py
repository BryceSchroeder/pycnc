# -*- coding: utf-8 -*-

from __future__ import division

import math

import gcodes
import exceptions


GCODE_EXTENSION = '.ngc'


# GCODE GENERATION


def oval(x_center, y_center, x_width, y_height, tool_diameter, feed_rate, z_feed_rate, from_z, to_z, step_z,  safety_z,
         angle=0.0):
         
    r"""Generate Gcode to cut an oval

    Parameters
    ----------
    ...
    angle : float
        clockwise rotation angle
    ...
    """
    point_center = Point(x_center, y_center)
    gcode = list()
    gcode.append(gcodes.g0_gcode(x=x_center, y=y_center, z=safety_z))

    for h in _generate_heights(from_z, to_z, step_z):
        for d in _generate_excentric(0.00, y_height/2.0, tool_diameter):
            point_n = (Point(0.0, d) + point_center).rotate(point_center, angle)
            point_ne = (Point((x_width - y_height) / 2.0, d) + point_center).rotate(point_center, angle)
            point_e_arc_center = (Point((x_width-y_height)/2.0, 0.0) + point_center).rotate(point_center, angle)
            point_se = (Point((x_width - y_height) / 2.0, -d) + point_center).rotate(point_center, angle)
            point_sw = (Point(-(x_width-y_height)/2.0, -d) + point_center).rotate(point_center, angle)
            point_w_arc_center = (Point(-(x_width - y_height)/2.0, 0.0) + point_center).rotate(point_center, angle)
            point_nw = (Point(-(x_width - y_height)/2.0, d) + point_center).rotate(point_center, angle)
            
            gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
            gcode.append(gcodes.g1_gcode(x=point_n.x, y=point_n.y, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=point_ne.x, y=point_ne.y, feedrate=feed_rate))
            gcode.append(gcodes.g2_gcode(x_end_point=point_se.x, y_end_point=point_se.y, spiral_end_altitude=h,
                                         x_center_offset=(point_e_arc_center - point_ne).x,
                                         y_center_offset=(point_e_arc_center - point_ne).y, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=point_sw.x, y=point_sw.y, feedrate=feed_rate))
            gcode.append(gcodes.g2_gcode(x_end_point=point_nw.x, y_end_point=point_nw.y, spiral_end_altitude=h,
                                         x_center_offset=(point_w_arc_center - point_sw).x,
                                         y_center_offset=(point_w_arc_center - point_sw).y, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=point_n.x, y=point_n.y, feedrate=feed_rate))

    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    return ''.join(gcode)


def path(path_to_follow, feed_rate, z_feed_rate, from_z, to_z, step_z, safety_z):
    r"""Generate Gcode to follow a path (an array of 2D (X,Y) arrays)"""
    
    gcode = list()
    gcode.append(gcodes.g0_gcode(x=0, y=0, z=safety_z))
    gcode.append(gcodes.g0_gcode(x=path_to_follow[0][0], y=path_to_follow[0][1]))
    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
        for point in path_to_follow:
            gcode.append(gcodes.g1_gcode(x=point[0], y=point[1], feedrate=feed_rate))
    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    return ''.join(gcode)


def rectangle(x_dimension, y_dimension, x_mini, y_mini, tool_diameter, feed_rate, z_feed_rate, from_z, to_z, step_z,
              safety_z):
    r"""Generate Gcode to cut a rectangle

    Parameters
    ----------
    x_dimension : positive float
        The dimension of the rectangle along the x axis
    y_dimension : positive float
        The dimension of the rectangle along the y axis
    feed_rate : positive float
        Feed rate in mm/min

    Note
    ----
    The milling head travels CCW around the rectangle
    
    """
    
    gcode = list()
    gcode.append(gcodes.g0_gcode(x=0, y=0, z=safety_z))
    gcode.append(gcodes.g0_gcode(x=x_mini - tool_diameter / 2, y=y_mini - tool_diameter / 2))

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
        gcode.append(gcodes.g1_gcode(x=x_mini + x_dimension + tool_diameter / 2, feedrate=feed_rate))
        gcode.append(gcodes.g1_gcode(y=y_mini + y_dimension + tool_diameter / 2, feedrate=feed_rate))
        gcode.append(gcodes.g1_gcode(x=x_mini-tool_diameter / 2, feedrate=feed_rate))
        gcode.append(gcodes.g1_gcode(y=y_mini-tool_diameter / 2, feedrate=feed_rate))

    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    
    return ''.join(gcode)


def rectangle_rounded_corners(x_center, y_center, x_dimension, y_dimension, corner_radius, tool_diameter, feed_rate,
                              z_feed_rate, from_z, to_z, step_z, safety_z):
    r"""Generate Gcode to cut a rectangle with rounded corners

    Parameters
    ----------
    x_dimension : positive float
        The dimension of the rectangle along the x axis
    y_dimension : positive float
        The dimension of the rectangle along the y axis
    feed_rate : positive float
        Feed rate in mm/min

    Note
    ----
    The milling head travels CCW around the rectangle
    
    """
    
    gcode = list()
    gcode.append(gcodes.g0_gcode(x=0, y=0, z=safety_z))
    # go to start point (LOWER LEFT CORNER)
    gcode.append(gcodes.g0_gcode(x=x_center - x_dimension / 2 + corner_radius,
                                 y=y_center - y_dimension / 2 - tool_diameter / 2))

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
        # LOWER EDGE
        gcode.append(gcodes.g1_gcode(x=x_center + x_dimension / 2 - corner_radius, feedrate=feed_rate))
        # BOTTOM RIGHT CORNER
        gcode.append(gcodes.g3_gcode(x_end_point=x_center + x_dimension / 2 + tool_diameter / 2,
                                     y_end_point=y_center - y_dimension / 2 + corner_radius,
                                     x_center_offset=0.0, y_center_offset=corner_radius + tool_diameter / 2,
                                     spiral_end_altitude=h, feedrate=feed_rate))
        # RIGHT EDGE
        gcode.append(gcodes.g1_gcode(y=y_center + y_dimension / 2 - corner_radius, feedrate=feed_rate))
        # UPPER RIGHT CORNER
        gcode.append(gcodes.g3_gcode(x_end_point=x_center + x_dimension / 2 - corner_radius,
                                     y_end_point=y_center + y_dimension / 2 + tool_diameter / 2,
                                     x_center_offset=-corner_radius - tool_diameter / 2,
                                     y_center_offset=0.0, spiral_end_altitude=h, feedrate=feed_rate))
        # TOP EDGE
        gcode.append(gcodes.g1_gcode(x=x_center - x_dimension / 2 + corner_radius, feedrate=feed_rate))
        gcode.append(gcodes.g3_gcode(x_end_point=x_center - x_dimension / 2 - tool_diameter / 2,
                                     y_end_point=y_center + y_dimension / 2 - corner_radius,
                                     x_center_offset=0.0, y_center_offset=-corner_radius - tool_diameter / 2,
                                     spiral_end_altitude=h, feedrate=feed_rate))
        gcode.append(gcodes.g1_gcode(y=y_center - y_dimension / 2 + corner_radius, feedrate=feed_rate))
        gcode.append(gcodes.g3_gcode(x_end_point=x_center - x_dimension / 2 + corner_radius,
                                     y_end_point=y_center - y_dimension / 2 - tool_diameter / 2,
                                     x_center_offset=corner_radius + tool_diameter / 2, y_center_offset=0.0,
                                     spiral_end_altitude=h, feedrate=feed_rate))

    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    
    return ''.join(gcode)


def thin_from_center(x_dimension, y_dimension, x_center, y_center, tool_diameter, feed_rate, z_feed_rate, from_z, to_z,
                     step_z, safety_z):
    r"""Generate Gcode to remove some material from a region around the center of the region

    It is intended to be used to make the stock thinner over a region
    before cutting a part from the thinned region
    
    """
    return thin(x_dimension, y_dimension, x_center - x_dimension / 2.0, y_center - y_dimension / 2.0, tool_diameter,
                feed_rate, z_feed_rate, from_z, to_z, step_z, safety_z)


def thin(x_dimension, y_dimension, x_mini, y_mini, tool_diameter, feed_rate, z_feed_rate, from_z, to_z, step_z,
         safety_z):
    r"""Generate Gcode to remove some material from a region defined by the bottom left point
    of a rectangle and its dimensions

    It is intended to be used to make the stock thinner over a region
    before cutting a part from the thinned region
    
    """
    
    x_center = x_mini + x_dimension / 2
    y_center = y_mini+y_dimension / 2
    gcode = list()
    gcode.append(gcodes.g0_gcode(x=0, y=0, z=safety_z))
    gcode.append(gcodes.g0_gcode(x=x_center, y=y_center))

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g1_gcode(x=x_center, y=y_center, feedrate=feed_rate))
        gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
        
        nb_turns = 0.00
        # correction bug 25 SEP 2012 - parcours du perimètre exterieur sans prendre de matière
        # division par 2 de y_dimension dans l expression de la boucle while
        # while nb_turns/2*tool_diameter < x_dimension/2 or nb_turns/2*tool_diameter < y_dimension:
        while nb_turns / 2 * tool_diameter < x_dimension/2 or nb_turns / 2* tool_diameter < y_dimension / 2:
            gcode.append(gcodes.g1_gcode(y=min(y_center + (nb_turns / 2 + 0.5) * tool_diameter,
                                               y_mini + y_dimension - tool_diameter / 2), feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=min(x_center + (nb_turns / 2 + 0.5) * tool_diameter,
                                               x_mini + x_dimension - tool_diameter / 2), feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(y=max(y_center - (nb_turns / 2 + 0.5) * tool_diameter,
                                               y_mini + tool_diameter / 2), feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=max(x_center - (nb_turns / 2 + 0.5) * tool_diameter,
                                               x_mini + tool_diameter / 2), feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(y=min(y_center + (nb_turns / 2 + 0.5) * tool_diameter,
                                               y_mini + y_dimension - tool_diameter / 2), feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=x_center, feedrate=feed_rate))
            
            nb_turns += 1.00

    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    return ''.join(gcode)


# def hole(x_center, y_center, hole_diameter, tool_diameter, feed_rate, z_feed_rate, from_z, to_z, step_z, safety_z):
def hole(x_center, y_center, hole_diameter, tool_diameter, feed_rate, from_z, to_z, step_z, safety_z):
    r"""Generate Gcode to cut a hole

    Note
    ----
    If the hole diameter is bigger than 2 x tool_diameter the material in the center is not removed
    
    """
    if hole_diameter < tool_diameter:
        raise exceptions.WrongParameterError('Cannot make a hole smaller than the tool')
    gcode = list()
    gcode.append(gcodes.g0_gcode(z=safety_z))
    gcode.append(gcodes.g0_gcode(x=x_center - hole_diameter / 2 + tool_diameter / 2, y=y_center))

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g2_gcode(x_center_offset=hole_diameter / 2 - tool_diameter / 2, y_center_offset=0,
                                     spiral_end_altitude=h, feedrate=feed_rate))
        
    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    
    return ''.join(gcode)


def full_hole(x_center, y_center, hole_diameter, tool_diameter, feed_rate, z_feed_rate, from_z, to_z, step_z, safety_z,
              center_diameter=0.0):
    r"""Generate Gcode to cut a hole and remove the middle material

    If the hole diameter is bigger than 2 x tool_diameter the material in the center is removed
    
    """
    if hole_diameter < tool_diameter:
        raise exceptions.WrongParameterError('Cannot make a hole smaller than the tool')
    gcode = list()
    gcode.append(gcodes.g0_gcode(z=safety_z))
    # gcode.append(_g0_gcode(x=x_center-tool_diameter/2,y=y_center))
    gcode.append(gcodes.g0_gcode(x=x_center - tool_diameter / 2, y=y_center))

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
        for e in _generate_excentric(start=center_diameter/2.0, end=hole_diameter / 2, tool_diameter=tool_diameter):
            gcode.append(gcodes.g1_gcode(x=x_center-e, y=y_center, feedrate=feed_rate))
            gcode.append(gcodes.g2_gcode(x_center_offset=e, y_center_offset=0, spiral_end_altitude=h,
                                         feedrate=feed_rate))
        
    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    return ''.join(gcode)


def square_pocket(x_center, y_center, x_dimension, y_dimension, tool_diameter, feed_rate, z_feed_rate, from_z, to_z,
                  step_z, safety_z):
    r"""Generate Gcode to dig a square and remove the middle material"""
    
    if x_dimension < tool_diameter or y_dimension < tool_diameter:
        raise exceptions.WrongParameterError('Cannot make a square pocket smaller than the tool')

    gcode = list()
    gcode.append(gcodes.g0_gcode(x=0, y=0, z=safety_z))
    gcode.append(gcodes.g0_gcode(x=x_center, y=y_center))
    
    x_absolute_maximum = x_center + x_dimension / 2
    x_absolute_minimum = x_center - x_dimension / 2
    
    x_maximum = x_absolute_maximum - tool_diameter / 2
    x_minimum = x_absolute_minimum + tool_diameter / 2
    
    y_maximum = y_center + y_dimension / 2 - tool_diameter / 2
    y_minimum = y_center - y_dimension / 2 + tool_diameter / 2
    
    path_to_follow = list()

    point1 = [x_center, y_maximum]
    point2 = [x_absolute_maximum, y_maximum]
    point3 = [x_maximum, y_maximum]
    point4 = [x_maximum, y_minimum]
    point5 = [x_absolute_maximum, y_minimum]
    point6 = [x_absolute_minimum, y_minimum]
    point7 = [x_minimum, y_minimum]
    point8 = [x_minimum, y_maximum]
    point9 = [x_absolute_minimum, y_maximum]

    path_to_follow.append(point1)
    path_to_follow.append(point2)
    path_to_follow.append(point3)
    path_to_follow.append(point4)
    path_to_follow.append(point5)
    path_to_follow.append(point6)
    path_to_follow.append(point7)
    path_to_follow.append(point8)
    path_to_follow.append(point9)
    path_to_follow.append(point1)

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g1_gcode(x=x_center, y=y_center, feedrate=feed_rate))
        gcode.append(gcodes.g1_gcode(z=h, feedrate=z_feed_rate))
        
        nb_turns = 0.00
        
        while nb_turns / 2 * tool_diameter < x_dimension / 2 or nb_turns / 2 * tool_diameter < y_dimension / 2.0:
            y_maxi = min(y_center + (nb_turns / 2 + 0.5) * tool_diameter,
                         y_center + y_dimension / 2 - tool_diameter / 2)
            x_maxi = min(x_center + (nb_turns / 2 + 0.5) * tool_diameter,
                         x_center + x_dimension / 2 - tool_diameter / 2)
            y_mini = max(y_center - (nb_turns / 2 + 0.5) * tool_diameter,
                         y_center - y_dimension / 2 + tool_diameter / 2)
            x_mini = max(x_center - (nb_turns / 2 + 0.5) * tool_diameter,
                         x_center - x_dimension / 2 + tool_diameter / 2)

            gcode.append(gcodes.g1_gcode(y=y_maxi, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=x_maxi, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(y=y_mini, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=x_mini, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(y=y_maxi, feedrate=feed_rate))
            gcode.append(gcodes.g1_gcode(x=x_center, feedrate=feed_rate))
            
            nb_turns += 1.00
            
        # Cut the corners
        for point in path_to_follow:
            gcode.append(gcodes.g1_gcode(x=point[0], y=point[1], feedrate=feed_rate))

    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    return ''.join(gcode)


# def cylinder(x_center, y_center, cylinder_diameter, tool_diameter, feed_rate, z_feed_rate, from_z, to_z, step_z,
#              safety_z
def cylinder(x_center, y_center, cylinder_diameter, tool_diameter, feed_rate, from_z, to_z, step_z, safety_z):
    r"""Generate Gcode to cut a cylinder"""
    gcode = list()
    gcode.append(gcodes.g0_gcode(z=safety_z))
    gcode.append(gcodes.g0_gcode(x=x_center - (cylinder_diameter + tool_diameter) / 2 + tool_diameter / 2, y=y_center))

    for h in _generate_heights(from_z, to_z, step_z):
        gcode.append(gcodes.g3_gcode(x_center_offset=(cylinder_diameter + tool_diameter) / 2 - tool_diameter / 2,
                                     y_center_offset=0, spiral_end_altitude=h, feedrate=feed_rate))

    gcode.append(gcodes.g1_gcode(z=safety_z, feedrate=feed_rate))
    return ''.join(gcode)


def two_concentric_holes(x_center, y_center, hole_diameter_1, hole_diameter_2, tool_diameter, feed_rate, z_feed_rate,
                         from_z_1, to_z_1, to_z_2, step_z, safety_z):
    r"""Generate Gcode to cut two concentric holes

    Parameters
    ----------
    ...
    to_z_1 : float
        end of 1st hole height, start of 2nd
    ...
    """
    
    if hole_diameter_2 > hole_diameter_1:
        raise exceptions.WrongParameterError('hole number 2 has to be smaller than hole number 1')
    gcode = list()
    gcode.append(full_hole(x_center, y_center, hole_diameter_1, tool_diameter, feed_rate, z_feed_rate, from_z_1, to_z_1,
                           step_z, safety_z))
    gcode.append(full_hole(x_center, y_center, hole_diameter_2, tool_diameter, feed_rate, z_feed_rate, to_z_1, to_z_2,
                           step_z, safety_z))
    return ''.join(gcode)


def drill(x, y, depth, safety_height, feedrate):
    r"""Generate Gcode to drill at x,y"""
    gcode = list()
    # gcode.append('G98\n')
    gcode.append(gcodes.g0_gcode(z=safety_height))
    gcode.append(gcodes.g0_gcode(x=x, y=y))
    gcode.append(gcodes.g81_gcode(z=depth, r=safety_height, feedrate=feedrate))
    return ''.join(gcode)


def drill_g73(x, y, depth, depth_increment, safety_height, feedrate):
    r"""Generate Gcode to drill at x,y with chip breaking"""
    gcode = list()
    # gcode.append('G98\n')
    gcode.append(gcodes.g0_gcode(z=safety_height))
    gcode.append(gcodes.g0_gcode(x=x, y=y))
    gcode.append(gcodes.g73_gcode(z=depth, r=safety_height, q=depth_increment, feedrate=feedrate))
    return ''.join(gcode)


def drill_g83(x, y, depth, depth_increment, safety_height, feedrate):
    r"""Generate Gcode to peck drill at x,y"""
    gcode = list()
    # gcode.append('G98\n')
    gcode.append(gcodes.g0_gcode(z=safety_height))
    gcode.append(gcodes.g0_gcode(x=x, y=y))
    gcode.append(gcodes.g83_gcode(z=depth, r=safety_height, q=depth_increment, feedrate=feedrate))
    return ''.join(gcode)


def start_gcode():
    r"""Returns the codes that should be at the beginning of every NC file"""
    start_code = ['G21\n',  # millimeters G20:inches
                  'G17\n',  # XY plane selection
                  'G90\n',  # absolute distance mode G91: incremental distance mode
                  'G54\n',  # first coordinate system
                  'G40\n',  # cancel cutter radius compensation
                  'G49\n',  # cancel tool length offset
                  'G61\n',  # exact path mode G61.1: exact stop mode G64: continuous mode with optional path tolerance
                  'G94\n']  # units per minute feed rate G93: inverse time feed rate G95: units per revolution
    return ''.join(start_code)


def end_gcode():
    r"""Returns the codes that should be at the end of every NC file"""
    end_code = ['M2\n']  # end program
    return ''.join(end_code)


def _generate_heights(from_z=0.0, to_z=-1.0, step=-0.10):
    """Generator of Z heights, intended to be used in a for loop to mill down in steps.

    Parameters
    ----------
    from_z : float, default: 0.0
        starting height
    to_z : float, default: -1.0
        end height (has to be below from_z)
    step : negative float, default: -0.1
        the step by which the milling head goes from from_z to to_z

    """
    if to_z is None or from_z is None or step is None:
        raise exceptions.MissingParameterError('Missing parameter')

    if from_z < to_z:
        raise exceptions.WrongParameterError('we are supposed to mill down - altitude problem')
    
    if step >= 0:
        raise exceptions.WrongParameterError('we are supposed to mill down - step problem')

    cur = float(from_z)
    
    while cur > to_z:
        yield cur
        cur += step
        
    yield to_z


def _generate_excentric(start=0.0, end=1.0, tool_diameter=3.0):
    """Generator of Z excentric values, This function is intended 
    to be used in a for loop to mill outwards in steps of tool_diameter/2

    Parameters
    ----------
    start : float, default: 0.0
        start position
    end : float, default: 1.0
        end position
    tool_diameter : positive float, default: 3.0
        tool diameter in mm

    """
    if end < tool_diameter / 2.0:
        raise exceptions.WrongParameterError('cannot generate excentric dimensions')
    
    value = float(start) + float(tool_diameter / 2.0)
    
    while value < end-tool_diameter/2.0:
        yield value 
        value += tool_diameter / 2.0
        
    yield end - tool_diameter / 2.0


class Point:
    r"""Simple class that stores 2D coordinates for a point"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        r"""Addition operation definition"""
        return Point(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        r"""Substraction operation definition"""
        return Point(self.x - other.x, self.y - other.y)
        
    def offset(self, x, y):
        return Point(self.x + x, self.y + y)
        
    def rotate_around_origin(self, degs):
        rads = math.radians(degs)
        return Point(self.x * math.cos(rads) - self.y * math.sin(rads),
                     self.x * math.sin(rads) + self.y * math.cos(rads))
    
    def rotate(self, center, degs):
        rads = math.radians(degs)
        displacement = self - center
        point = Point(0, 0)
        point.x = displacement.x * math.cos(rads) + displacement.y * math.sin(rads)
        point.y = displacement.y * math.cos(rads) - displacement.x * math.sin(rads)
        point = point + center
        return point
