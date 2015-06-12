#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

import sys


def for_examples(*parameters):
    """
    From StackOverflow:
    http://stackoverflow.com/questions/2798956/python-unittest-generate-multiple-tests-programmatically
    """
    def tuplify(x):
        if not isinstance(x, tuple):
            return (x,)
        return x

    def decorator(method, parameters=parameters):
        for parameter in (tuplify(x) for x in parameters):
            def method_for_parameter(self, method=method, parameter=parameter):
                method(self, *parameter)
            args_for_parameter = ",".join(repr(v) for v in parameter)
            name_for_parameter = method.__name__ + "(" + args_for_parameter + ")"
            frame = sys._getframe(1)
            frame.f_locals[name_for_parameter] = method_for_parameter
        return None
    return decorator
