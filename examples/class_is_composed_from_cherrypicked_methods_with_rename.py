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


# Then, here we do the actual composition, where we cherry-pick each method from
# ExampleTrait and compose them into ExampleClass. While we do that, we also
# specify function names as keyword parameters to change the name of the
# functions.
ExampleClass.add_traits(ExampleTrait.instance_method,
                        ExampleTrait.class_method,
                        ExampleTrait.static_method,
                        instance_method="renamed_instance_method",
                        class_method="renamed_class_method",
                        static_method="renamed_static_method")

# Here are the proofs that composed methods work as part of new class.
assert ExampleClass.renamed_static_method() == (1, 2, 3),\
    "Class composition fails with classmethod in class!"
assert ExampleClass.renamed_class_method() == (24, 25, 26),\
    "Class composition fails with class method in class!"
assert ExampleClass().renamed_class_method() == (24, 25, 26), \
    "Class composition fails with class method in instance!"
assert ExampleClass().renamed_instance_method() == (42, 43, 44),\
    "Class composition fails with instance method!"
