#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Let's start by creating a simple class with some values. It contains
# only instance variables. Composed property will have access to all
# these variables.
@extendable
class ExampleClass:
    def __init__(self):
        self.public = 42
        self._hidden = 43
        self.__private = 44


# Then we create a class which contains different types of methods that will be
# transferred as a part of the class above. Note that ExampleTrait requires target
# object to contain instance variables, thus it won't work as a stand-alone object.
class ExampleTrait:
    @property
    def trait_property(self):
        return self.public, self._hidden, self.__private

    @trait_property.setter
    def trait_property(self, new_value):
        self.public, self._hidden, self.__private = new_value

    @trait_property.deleter
    def trait_property(self):
        self.public, self._hidden, self.__private = (42, 43, 44)


# Create instance out of the trait class. Now we need to notice that we need
# to refer to instance's class to get the property and transfer it to new
# location. Using directly my_trait_instance.trait_property would naturally
# invoke retrieval of the values (which in this case would not even exist and
# and would raise an error).
example_instance = ExampleClass()
my_trait_instance = ExampleTrait()
example_instance.add_traits(my_trait_instance.__class__.trait_property)


# Here are the proofs that composed property works as part of new class.
# Also we show that there is no inheritance done for ExampleClass instance.
assert example_instance.trait_property == (42, 43, 44),\
    "Cherry-picked property not working in new class!"

# We also demonstrate that we can alter the values through the property
example_instance.trait_property = (142, 143, 144)
assert example_instance.trait_property == (142, 143, 144),\
    "Cherry-picked property's setter not working in new class!"

# Finally, we can delete property's content
del example_instance.trait_property
assert example_instance.trait_property == (42, 43, 44),\
    "Cherry-picked property's deleter not working in new class!"

# And finally, original class is still unaffected.
assert not hasattr(ExampleClass, "trait_property"),\
    "Cherry-picked property has leaked into class!"
