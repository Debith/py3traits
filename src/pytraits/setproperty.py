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

import inspect

from pytraits.trait_composer import add_traits

__all__ = ["setproperty"]


def setproperty(target, fget=None, fset=None, fdel=None, source=None, name=None):
    """
    Convinience function that dynamically creates property to an object.
    (If you have property created, just use 'add_traits')

    This function has different behavior depending on the target object,
    whether it is an instance or a class. If target is an instance the
    property is being set only for that instance. In case the object is
    a class, the property will be added to it normally to class.

    Args:
        target (object or type): Target object, which can be any instance or class.
        fget (str or function): Getter function or its name
        fset (str or function): Setter function or its name
        fdel (str or function): Deleter function or its name
        source (object or type): Source object in case fget, fset and fdel are strings.

    Keyword args:
        name (str): Name of the property
        name of fget (str): Name of the property

    Example, where new property is added dynamically into instance:

    >>> class Example:
    ...     def __init__(self):
    ...         self.__value = 42
    ...
    ...     def set_value(self, new_value):
    ...         self.__value = new_value
    ...
    ...     def value(self):
    ...         return self.__value
    ...
    ...     def del_value(self):
    ...         self.__value = 42
    ...
    >>> instance = Example()
    >>> setproperty(instance, "value", "set_value", "del_value", name="my_property")
    >>> instance.my_property
    42
    """
    resolutions = {}

    # If some arguments are left out, skip them from test.
    args = [arg for arg in (fget, fset, fdel) if arg]

    # There must be at least one argument
    if not args:
        raise TypeError("Property needs to have at least one function.")

    # Handle case, when all provided arguments are strings.
    elif all(isinstance(arg, str) for arg in args):
        owner = source or target
        resolutions[fget] = name

        new_property = property(getattr(owner, fget or "", None),
                                getattr(owner, fset or "", None),
                                getattr(owner, fdel or "", None))

    # It is also possible to provide functions.
    elif all(inspect.isroutine(arg) for arg in args):
        resolutions[fget.__name__] = name
        new_property = property(fget, fset, fdel)

    # Other conditions are not supported.
    else:
        raise TypeError("Unsupported setup for property functions!")

    add_traits(target, new_property, **resolutions)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
