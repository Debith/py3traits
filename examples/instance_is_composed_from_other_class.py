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


# Create composition from instance of ExampleClass and ExampleTrait class.
example_instance = ExampleClass()
example_instance.add_traits(ExampleTrait)


# Here are the proofs that composed methods work as part of new instance. Also
# we demonstrate that original class is still untouched.
assert example_instance.static_method() == (1, 2, 3),\
    "Class composition fails with static method!"
assert example_instance.class_method() == (24, 25, 26),\
    "Class composition fails with class method!"
assert example_instance.instance_method() == (42, 43, 44),\
    "Class composition fails with instance method!"
assert not hasattr(ExampleClass, "new_static_function"),\
    "Instance composition fails due to class has changed!"
assert not hasattr(ExampleClass, "new_class_function"),\
    "Instance composition fails due to class has changed!"
assert not hasattr(ExampleClass, "new_method"),\
    "Instance composition fails due to class has changed!"
