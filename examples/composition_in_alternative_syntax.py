#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# class variables and instance variables. Composed methods will have
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


# Then we create a class which contains different types of methods that will be
# transferred as a part of the class above. Note that ExampleTrait requires target
# object to contain class variables and instance variables, thus it won't work as a
# stand-alone object.
class ExampleTrait:
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


def modify_instance(self, public, hidden, private):
    self.public, self._hidden, self.__private = public, hidden, private


# Instead of giving directly the function or class object, we can also give
# refer to objects by their name.
example_instance1 = ExampleClass()
example_instance1.add_traits(ExampleTrait, "value", "class_method", "instance_method")
example_instance1.add_traits(modify_instance)

# Modify the content for both instances
example_instance1.modify_instance(10, 20, 30)

# Here are the proofs that composed methods work as part of new instances.
assert hasattr(example_instance1, "value"),\
    "Failed to copy 'value' property"
assert hasattr(example_instance1, "class_method"),\
    "Failed to copy 'class_method' function"
assert hasattr(example_instance1, "instance_method"),\
    "Failed to copy 'class_method' function"
assert example_instance1.instance_method() == (10, 20, 30)
