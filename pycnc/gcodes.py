#!/usr/bin/python
# coding: utf-8

r"""Gcode formatting"""

import exceptions


def _gcode_format(prefix, x=None, y=None, z=None, i=None, j=None, r=None, q=None, feedrate=None):
    r"""Formats the Gcode line discarding undefined parameters"""
    gcode = list()
    gcode.append(prefix)
    gcode.append(' ')
    if x is not None:
        gcode.append('X%(x)s ' % {'x': x})
    if y is not None:
        gcode.append('Y%(y)s ' % {'y': y})
    if z is not None:
        gcode.append('Z%(z)s ' % {'z': z})
    if i is not None:
        gcode.append('I%(i)s ' % {'i': i})
    if j is not None:
        gcode.append('J%(j)s ' % {'j': j})
    if r is not None:
        gcode.append('R%(r)s ' % {'r': r})
    if q is not None:
        gcode.append('Q%(q)s ' % {'q': q})
    if feedrate is not None:
        gcode.append('F%(f)s ' % {'f': feedrate})
    gcode.append('\n')
    return ''.join(gcode)


def g0_gcode(x=None, y=None, z=None):
    r""" Max speed move Gcode"""
    if x is None and y is None and z is None:
        raise exceptions.GcodeParameterError('G0 parameter error')
    return _gcode_format(prefix='G0', x=x, y=y, z=z)


def g1_gcode(x=None, y=None, z=None, feedrate=None):
    r""" Feed speed move Gcode"""
    if x is None and y is None and z is None:
        raise exceptions.GcodeParameterError('G1 parameter error')
    return _gcode_format(prefix='G1', x=x, y=y, z=z, feedrate=feedrate)


def g2_gcode(x_end_point=None, y_end_point=None, spiral_end_altitude=None, x_center_offset=None, y_center_offset=None,
             feedrate=None):
    r""" Clockwise arc"""
    if x_center_offset is None and y_center_offset is None:
        raise exceptions.GcodeParameterError('G2 parameter error')
    return _gcode_format(prefix='G2', x=x_end_point, y=y_end_point, z=spiral_end_altitude, i=x_center_offset,
                         j=y_center_offset, feedrate=feedrate)


def g3_gcode(x_end_point=None, y_end_point=None, x_center_offset=None, y_center_offset=None, spiral_end_altitude=None,
             feedrate=None):
    r""" Counterclockwise arc"""
    if x_center_offset is None and y_center_offset is None:
        raise exceptions.GcodeParameterError('G3 parameter error')
    return _gcode_format(prefix='G3', x=x_end_point, y=y_end_point, i=x_center_offset, j=y_center_offset,
                         z=spiral_end_altitude, feedrate=feedrate)


def g73_gcode(x=None, y=None, z=None, r=None, q=None, feedrate=None):
    r""" Chip break drill"""
    if z is None or r is None:
        raise exceptions.GcodeParameterError('G73 parameter error')
    if r < z:
        raise exceptions.GcodeParameterError('G73 parameter error - r smaller than z')
    return _gcode_format(prefix='G73 G98', x=x, y=y, z=z, r=r, q=q, feedrate=feedrate)


def g83_gcode(x=None, y=None, z=None, r=None, q=None, feedrate=None):
    r""" Peck drill"""
    if z is None or r is None:
        raise exceptions.GcodeParameterError('G83 parameter error')
    if r < z:
        raise exceptions.GcodeParameterError('G83 parameter error - r smaller than z')
    return _gcode_format(prefix='G83 G98', x=x, y=y, z=z, r=r, q=q, feedrate=feedrate)


def g81_gcode(x=None, y=None, z=None, r=None, feedrate=None):
    r""" Normal drill"""
    if z is None or r is None:
        raise exceptions.GcodeParameterError('G81 parameter error')
    if r < z:
        raise exceptions.GcodeParameterError('G81 parameter error - r smaller than z')
    return _gcode_format(prefix='G81 G98', x=x, y=y, z=z, r=r, feedrate=feedrate)
