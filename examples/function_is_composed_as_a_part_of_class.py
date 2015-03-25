#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# class variables and instance variables. Composed functions will have
# access to all these variables.
@extendable
class ExampleClass(object):
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


# Compose cherry-picked functions into ExampleClass.
ExampleClass.add_traits(new_method, new_class_function, new_static_function)


# Here are the proofs that composed functions work as part of new class.
assert ExampleClass.new_static_function() == (1, 2, 3), "Class composition fails with class method in class!"
assert ExampleClass.new_class_function() == (24, 25, 26), "Class composition fails with class method in class!"
assert ExampleClass().new_class_function() == (24, 25, 26), "Class composition fails with class method in instance!"
assert ExampleClass().new_method() == (42, 43, 44), "Class composition fails with instance method!"
