# coding: utf-8

r"""Exceptions for the pycnc package"""


class RootException(Exception):
    pass


class MissingParameterError(RootException):
    pass


class WrongParameterError(RootException):
    pass


class GcodeParameterError(RootException):
    pass
