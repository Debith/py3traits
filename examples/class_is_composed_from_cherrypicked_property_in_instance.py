#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# only instance variables. Composed property will have access to all
# these variables.
@extendable
class ExampleClass(object):
    def __init__(self):
        self.public = 42
        self._hidden = 43
        self.__private = 44


# Then we create a class which contains different types of methods that will be
# transferred as a part of the class above. Note that ExampleTrait requires target
# object to contain instance variables, thus it won't work as a stand-alone object.
class ExampleTrait(object):
    @property
    def trait_property(self):
        return self.public, self._hidden, self.__private


# Create instance out of the trait class. Now we need to notice that we need
# to refer to instance's class to get the property and transfer it to new
# location. Using directly my_trait_instance.trait_property would naturally
# invoke retrieval of the values (which in this case would not even exist and
# and would raise an error).
my_trait_instance = ExampleTrait()
ExampleClass.add_traits(my_trait_instance.__class__.trait_property)


# Here are the proofs that composed property works as part of new class.
# Also we show that there is no inheritance done for ExampleClass instance.
assert ExampleClass.__bases__ == (object, ), "Inheritance has occurred!"
assert ExampleClass().trait_property == (42, 43, 44),\
    "Cherry-picked property not working in new class!"
