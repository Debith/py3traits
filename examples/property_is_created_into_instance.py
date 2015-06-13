#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import setproperty


# Let's start by creating a simple class with some values. It contains
# only instance variables. Added property will have access to all
# these variables.
class ExampleClass(object):
    def __init__(self):
        self.public = 42
        self._hidden = 43
        self.__private = 44

    def set_all(self, values):
        self.public, self._hidden, self.__private = values

    def get_all(self):
        return self.public, self._hidden, self.__private

    def del_all(self):
        self.public, self._hidden, self.__private = (42, 43, 44)

# Create new instances for each situation
example1 = ExampleClass()
example2 = ExampleClass()
example3 = ExampleClass()
example4 = ExampleClass()

# Use functions from class
setproperty(example1, ExampleClass.get_all,
                      ExampleClass.set_all,
                      ExampleClass.del_all, name="all")

# Create property using functions from other instance
setproperty(example1, example1.get_all,
                      example1.set_all,
                      example1.del_all, name="all")

# Create property for current instance
setproperty(example2, "get_all", "set_all", name="all")

# Create property referring functions in other instance
setproperty(example3, "get_all", "set_all", "del_all", example1, name="all")

# All instances have their own independent properties
example1.all = 1, 2, 3
example2.all = 10, 20, 30
example3.all = 100, 200, 300
example4.all = 1000, 2000, 3000

# Demonstrate that each instance is modified properly
assert example1.all == (1, 2, 3), "Values were %d, %d, %d" % example1.all
assert example2.all == (10, 20, 30), "Values were %d, %d, %d" % example2.all
assert example3.all == (100, 200, 300), "Values were %d, %d, %d" % example3.all
assert example4.all == (1000, 2000, 3000), "Values were %d, %d, %d" % example4.all

# And deleting works also for properties independently
del example1.all
del example4.all

# Verify that only touched instances are handled and rest remains intact.
assert example1.all == (42, 43, 44), "Values were %d, %d, %d" % example1.all
assert example2.all == (10, 20, 30), "Values were %d, %d, %d" % example2.all
assert example3.all == (100, 200, 300), "Values were %d, %d, %d" % example3.all
assert example4.all == (42, 43, 44), "Values were %d, %d, %d" % example4.all
