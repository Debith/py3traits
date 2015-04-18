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


try:
    # We don't support this yet. Property does not have name, thus we need to
    # support renaming of trait before this can work.
    raise NotImplementedError('')
except NotImplementedError:
    ExampleClass.add_traits(ExampleTrait)

    # Here are the proofs that composed property works as part of new class.
    # Also we show that there is no inheritance done for ExampleClass instance.
    assert ExampleClass.__bases__ == (object, ), "Inheritance has occurred!"
    assert ExampleClass().trait_property == (42, 43, 44), "Cherry-picked property not working in new class!"
