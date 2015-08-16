#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
from pytraits import extendable


# Using decorator to add trait support for objects is the recommended way
# to do. Here we add add_traits function to our example object.
@extendable
class MyExample:
    pass

assert hasattr(MyExample, 'add_traits'), "Failed to add 'add_traits' function to MyExample"


# Here we define a trait class, that we use to cherry-pick some functions
# to our new object.
class Traits:
    def for_all_classes(self):
        pass

    def for_single_instance(self):
        pass


# Here we add the method into MyExample CLASS.
MyExample.add_traits(Traits.for_all_classes)

# Here is the proof that new method is there.
assert hasattr(MyExample, 'for_all_classes')


# In this second case, we add new method into INSTANCE of MyExample class.
instance = MyExample()
instance.add_traits(Traits.for_single_instance)

# Here is the proofs that method is found from the instance and not from class.
assert hasattr(instance, 'for_single_instance')
assert not hasattr(MyExample, 'for_single_instance')
