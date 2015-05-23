#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import combine_class


# In the beginning, we don't have own object even, we just have traits.
class FirstExampleTrait(object):
    @staticmethod
    def static_method():
        return 1, 2, 3


class SecondExampleTrait(object):
    @classmethod
    def class_method(cls):
        return cls.PUBLIC, cls._HIDDEN, cls.__PRIVATE

    def instance_method(self):
        return self.public, self._hidden, self.__private


class ThirdExampleTrait(object):
    @property
    def value(self):
        return self.public, self._hidden, self.__private

    @value.setter
    def value(self, new_values):
        self.public, self._hidden, self.__private = new_values


# Now, we create completely new class out of the traits.
ExampleClass = combine_class("ExampleClass", FirstExampleTrait,
                                             SecondExampleTrait,
                                             ThirdExampleTrait)

# Create new instance and update its values
example_instance = ExampleClass()
example_instance.value = (42, 43, 44)

# Also fill in the class variables.
ExampleClass.PUBLIC = 24
ExampleClass._HIDDEN = 25
ExampleClass._ExampleClass__PRIVATE = 26


# Here are the proofs that composed methods work as part of new class. Also we show
# that there is no inheritance done for ExampleClass.
assert ExampleClass.__bases__ == (object, ), "Inheritance has occurred!"
assert ExampleClass.__name__ == "ExampleClass"
assert ExampleClass.static_method() == (1, 2, 3),\
    "Class composition fails with static method!"
assert ExampleClass.class_method() == (24, 25, 26),\
    "Class composition fails with classmethod!"
assert example_instance.class_method() == (24, 25, 26),\
    "Class composition fails with classmethod in instance!"
assert example_instance.instance_method() == (42, 43, 44),\
    "Class composition fails with instance method!"
assert example_instance.value == (42, 43, 44),\
    "Class composition fails with property!"
