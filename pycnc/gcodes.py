# coding: utf-8

r"""Gcode formatting

Summary
-------
Formatting of GCode (G0, G1, G2, G3, G73, G81, G83) instructions

"""

import pycnc.exceptions as exceptions


def _gcode_format(prefix, x=None, y=None, z=None, i=None, j=None, r=None, q=None, feedrate=None):
    r"""Formats the Gcode line discarding undefined parameters

    Parameters
    ----------
    prefix : str
        GCode instruction prefix (e.g. GO)
    x, y, z : float, optional
        x y z position in 3D (default is None, implies the coordinate will be discarded from the GCode instruction)
        Meaning might differ slightly from GCode to GCode
    i : float
        x centre offset for circular arcs
    j : float
        y centre offset for circular arcs
    r : float, optional
        Retract position along the Z axis.
    q : float, optional
        Delta increment along the Z axis.
    feedrate : float
        Feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If the prefix does not start with a capital G

    Examples
    --------
    >>> _gcode_format('G0', x=1.0, y=2.0, z=3.0)
    'G0 X1.0 Y2.0 Z3.0 \n'

    >>> _gcode_format('A0', x=1.0, y=2.0, z=3.0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    GcodeParameterError: What instruction is that?

    """
    if prefix[0] not in ['G', 'M']:
        raise exceptions.GcodeParameterError('What instruction is that?')
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
    r""" Max speed move Gcode

    Parameters
    ----------
    x, y, z : float, optional
        x y z position in 3D (default is None, implies the coordinate will be discarded from the GCode instruction)

    Raises
    ------
    GcodeParameterError
        If all parameters are None

    """
    if x is None and y is None and z is None:
        raise exceptions.GcodeParameterError('G0 parameter error')
    return _gcode_format(prefix='G0', x=x, y=y, z=z)


def g1_gcode(x=None, y=None, z=None, feedrate=None):
    r""" Feed speed move Gcode

    Parameters
    ----------
    x, y, z : float, optional
        x y z position in 3D (default is None, implies the coordinate will be discarded from the GCode instruction)
    feedrate : float
        Feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If x, y and z are None

    """
    if x is None and y is None and z is None:
        raise exceptions.GcodeParameterError('G1 parameter error')
    return _gcode_format(prefix='G1', x=x, y=y, z=z, feedrate=feedrate)


def g2_gcode(x_end_point=None, y_end_point=None, spiral_end_altitude=None, x_center_offset=None, y_center_offset=None,
             feedrate=None):
    r""" Clockwise arc in XY plane (G17)

    Parameters
    ----------
    x_end_point : float, optional
        End X
    y_end_point : float, optional
        End Y
    spiral_end_altitude : float, optional
        helix
    x_center_offset : float, optional
        X offset
    y_center_offset : float, optional
        Y offset
    feedrate : float, optional
        Feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If x_center_offset and y_center_offset are None

    Notes
    -----
    http://linuxcnc.org/docs/html/gcode/g-code.html#_center_format_arcs

    """
    if x_center_offset is None and y_center_offset is None:
        raise exceptions.GcodeParameterError('G2 parameter error')
    return _gcode_format(prefix='G2', x=x_end_point, y=y_end_point, z=spiral_end_altitude, i=x_center_offset,
                         j=y_center_offset, feedrate=feedrate)


def g3_gcode(x_end_point=None, y_end_point=None, x_center_offset=None, y_center_offset=None, spiral_end_altitude=None,
             feedrate=None):
    r""" Counterclockwise arc in XY plane (G17)

    Parameters
    ----------
    x_end_point : float, optional
        End X
    y_end_point : float, optional
        End Y
    x_center_offset : float, optional
        X offset
    y_center_offset : float, optional
        Y offset
    spiral_end_altitude : float, optional
        helix
    feedrate : float, optional
        Feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If x_center_offset and y_center_offset are None

    Notes
    -----
    http://linuxcnc.org/docs/html/gcode/g-code.html#_center_format_arcs

    """
    if x_center_offset is None and y_center_offset is None:
        raise exceptions.GcodeParameterError('G3 parameter error')
    return _gcode_format(prefix='G3', x=x_end_point, y=y_end_point, i=x_center_offset, j=y_center_offset,
                         z=spiral_end_altitude, feedrate=feedrate)


def g73_gcode(x=None, y=None, z=None, r=None, q=None, feedrate=None):
    r""" Chip break drill

    Parameters
    ----------
    x, y, z : float, optional
        x y z position in 3D (default is None, implies the coordinate will be discarded from the GCode instruction)
    r : float, optional
        Retract position along the Z axis.
    q : float, optional
        Delta increment along the Z axis.
    feedrate : float
        Drilling feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If z is None or r is None
        If r is smaller than z
        q is negative or 0

    Notes
    -----
    http://linuxcnc.org/docs/html/gcode/g-code.html#_g73_drilling_cycle_with_chip_breaking

    Examples
    --------
    >>> g73_gcode(x=1.0, z=3.0, r=4.0, q=1.0)
    'G73 G98 X1.0 Z3.0 R4.0 Q1.0 \n'

    >>> g73_gcode(x=1.0, y=2.0, z=3.0, r=4.0, q=-1.0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    GcodeParameterError

    >>> g73_gcode(x=1.0, y=2.0, r=4.0, q=1.0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    GcodeParameterError

    """
    if z is None or r is None:
        raise exceptions.GcodeParameterError('G73 parameter error')
    if r < z:
        raise exceptions.GcodeParameterError('G73 parameter error - r smaller than z')
    if q <= 0:
        raise exceptions.GcodeParameterError('G83 parameter error - q must be strictly positive')
    return _gcode_format(prefix='G73 G98', x=x, y=y, z=z, r=r, q=q, feedrate=feedrate)


def g83_gcode(x=None, y=None, z=None, r=None, q=None, feedrate=None):
    r"""Peck drill

    Parameters
    ----------
    x, y, z : float, optional
        x y z position in 3D (default is None, implies the coordinate will be discarded from the GCode instruction)
    r : float, optional
        Retract position along the Z axis.
    q : float, optional
        Delta increment along the Z axis.
    feedrate : float
        Drilling feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If z is None or r is None
        If r is smaller than z
        q is negative or 0

    Notes
    -----
    http://linuxcnc.org/docs/html/gcode/g-code.html#_g83_peck_drilling_cycle

    Examples
    --------
    >>> g83_gcode(x=1.0, z=3.0, r=4.0, q=1.0)
    'G83 G98 X1.0 Z3.0 R4.0 Q1.0 \n'

    >>> g83_gcode(x=1.0, y=2.0, z=3.0, r=4.0, q=-1.0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    GcodeParameterError

    >>> g83_gcode(x=1.0, y=2.0, r=4.0, q=1.0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    GcodeParameterError

    """
    if z is None or r is None:
        raise exceptions.GcodeParameterError('G83 parameter error')
    if r < z:
        raise exceptions.GcodeParameterError('G83 parameter error - r smaller than z')
    if q <= 0:
        raise exceptions.GcodeParameterError('G83 parameter error - q must be strictly positive')
    return _gcode_format(prefix='G83 G98', x=x, y=y, z=z, r=r, q=q, feedrate=feedrate)


def g81_gcode(x=None, y=None, z=None, r=None, feedrate=None):
    r"""Normal drill

    Parameters
    ----------
    x, y, z : float, optional
        x y z position in 3D (default is None, implies the coordinate will be discarded from the GCode instruction)
    r : float, optional
        Retract position along the Z axis.
    feedrate : float
        Drilling feedrate in mm/mn

    Raises
    ------
    GcodeParameterError
        If z is None or r is None
        If r is smaller than z

    Notes
    -----
    http://linuxcnc.org/docs/html/gcode/g-code.html#_g81_drilling_cycle

    Examples
    --------
    >>> g81_gcode(x=1.0, z=3.0, r=4.0)
    'G81 G98 X1.0 Z3.0 R4.0 \n'
    >>> g81_gcode(x=1.0, y=2.0, z=3.0) # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
    GcodeParameterError

    """
    if z is None or r is None:
        raise exceptions.GcodeParameterError('G81 parameter error')
    if r < z:
        raise exceptions.GcodeParameterError('G81 parameter error - r smaller than z')
    return _gcode_format(prefix='G81 G98', x=x, y=y, z=z, r=r, feedrate=feedrate)
