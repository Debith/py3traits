#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# class variables and instance variables. Composed methods will have
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


# Then we create a class which contains different types of methods that will be
# transferred as a part of the class above. Note that ExampleTrait requires target 
# object to contain class variables and instance variables, thus it won't work as a 
# stand-alone object.
class ExampleTrait(object):
    @staticmethod
    def static_method():
        return 1, 2, 3

    @classmethod
    def class_method(cls):
        return cls.PUBLIC, cls._HIDDEN, cls.__PRIVATE

    def instance_method(self):
        return self.public, self._hidden, self.__private

    @property
    def value(self):
        return self.public, self._hidden, self.__private


# Compose new methods and property from ExampleTrait instance into ExampleClass.
ExampleClass.add_traits(ExampleTrait())


# Here are the proofs that composed methods work as part of new class. Also we show
# that there is no inheritance done for ExampleClass.
assert ExampleClass.__bases__ == (object, ), "Inheritance has occurred!"
assert ExampleClass.static_method() == (1, 2, 3), "Class composition fails with static method!"
assert ExampleClass.class_method() == (24, 25, 26), "Class composition fails with class method!"
assert ExampleClass().class_method() == (24, 25, 26), "Class composition fails with class method in instance!"
assert ExampleClass().instance_method() == (42, 43, 44), "Class composition fails with instance method!"
assert ExampleClass().value == (42, 43, 44), "Class composition fails with property!"
