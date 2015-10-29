# -*- coding: utf-8 -*-

#  _ __ _  _ __ _ _  __
# | '_ \ || / _| ' \/ _|
# | .__/\_, \__|_||_\__|
# |_|   |__/
#
# 2.5D CNC Python routines to generate GCode for simple geometries

__version__ = (1, 0, 0, 'final', 0)
__author__ = 'Guillaume Florent (florentsailing@gmail.com)'
__license__ = 'GPL v2'

get_version = lambda: __import__('pycnc.utils.version', fromlist=['get_version']).get_version(__version__)
