#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-08-10 13:56
# Last modified: 2017-09-10 15:23
# Filename: exceptions.py
# Description:


class TorchToolsException(Exception):
    pass


class HookTypeError(TorchToolsException):
    pass


class HookCheckError(TorchToolsException):
    pass


class TrainerTerminated(TorchToolsException):
    pass


class MeterNotFoundError(TorchToolsException):
    pass


class MeterNoValueError(TorchToolsException):
    pass


class LogTypeError(TorchToolsException):
    pass
