# coding: utf-8

r"""Exceptions for the pycnc package"""


class RootException(Exception):
    r"""Base exception for the pycnc project"""
    pass


class MissingParameterError(RootException):
    r"""Missing parameter for shapes GCode computation"""
    pass


class WrongParameterError(RootException):
    r"""Wrong parameter for shapes GCode computation"""
    pass


class GcodeParameterError(RootException):
    r"""Missing or wrong parameter for atomic GCode instructions"""
    pass
