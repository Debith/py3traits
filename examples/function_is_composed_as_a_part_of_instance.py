#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# class variables and instance variables. Composed functions will have
# access to all these variables.
@extendable
class ExampleClass:
    PUBLIC = 24
    _HIDDEN = 25
    __PRIVATE = 26

    def __init__(self):
        self.public = 42
        self._hidden = 43
        self.__private = 44


def new_method(self):
    return self.public, self._hidden, self.__private


def new_class_function(cls):
    return cls.PUBLIC, cls._HIDDEN, cls.__PRIVATE


def new_static_function():
    return 1, 2, 3


# Create instance of ExampleClass and compose cherry-picked functions into it.
example_instance = ExampleClass()
example_instance.add_traits(new_method, new_class_function, new_static_function)


# Here are the proofs that composed functions work as part of new instance. Also
# we demonstrate that original class is still untouched.
assert example_instance.new_static_function() == (1, 2, 3),\
    "Instance composition fails with static method in instance!"
assert example_instance.new_class_function() == (24, 25, 26),\
    "Instance composition fails with class method in instance!"
assert example_instance.new_method() == (42, 43, 44),\
    "Instance composition fails with instance method!"
assert not hasattr(ExampleClass, "new_static_function"),\
    "Instance composition fails due to class has changed!"
assert not hasattr(ExampleClass, "new_class_function"),\
    "Instance composition fails due to class has changed!"
assert not hasattr(ExampleClass, "new_method"),\
    "Instance composition fails due to class has changed!"
