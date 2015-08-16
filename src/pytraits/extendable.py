#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
'''
   Copyright 2014-2015 Teppo Perä

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

from pytraits.trait_composer import add_traits


def extendable(target):
    """
    Decorator that adds function for object to be extended using traits.

    NOTE: The 'add_traits' function this extendable decorator adds contains
          behavior that differs from usual function behavior. This method
          alters its behavior depending is the function called on a class
          or on an instance. If the function is invoked on class, then the
          class gets updated by the traits, affecting all new instances
          created from the class. On the other hand, if the function is invoked
          on an instance, only that instance gets the update, NOT whole class.

          See complete example from:
          pytraits/examples/extendable_function_class_vs_instance.py

    >>> @extendable
    ... class ExampleClass:
    ...     pass
    ...
    >>> hasattr(ExampleClass, 'add_traits')
    True

    >>> class InstanceExample:
    ...     pass
    ...
    >>> instance_example = InstanceExample()
    >>> _ = extendable(instance_example)
    >>> hasattr(instance_example, 'add_traits')
    True
    """
    class TypeFunction:
        def __init__(self):
            self._target_object = None

        def __call__(self, *args, **kwargs):
            add_traits(self._target_object, *args, **kwargs)

        def __get__(self, instance, clazz):
            self._target_object = instance or clazz
            return self

    target.add_traits = TypeFunction()
    return target


if __name__ == '__main__':
    import doctest
    doctest.testmod()
