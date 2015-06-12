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


def setproperty(target, fget=None, fset=None, fdel=None, source=None, **kwargs):
    """
    Convinience function that dynamically creates property to an object.
    (If you have property created, just use 'add_traits')

    @param {object or type} target: Target object, which can be any instance or class.
    @param {str or function} fget: Getter function or its name
    @param {str or function} fset: Setter function or its name
    @param {str or function} fdel: Deleter function or its name

    NOTE: This function has different behavior depending on the target object,
          whether it is an instance or a class. If target is an instance the
          property is being set only for that instance. In case the object is
          a class, the property will be added to it normally.

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
    >>> setproperty(instance, "value", "set_value", "del_value", value="my_property")
    >>> instance.my_property
    42
    """
    if all([isinstance(arg, str) for arg in (fget, fset, fdel)]):
        owner = source or target
        new_property = property(getattr(owner, fget, None),
                                getattr(owner, fset, None),
                                getattr(owner, fdel, None))
    elif all([inspect.isroutine(arg) for arg in (fget, fset, fdel)]):
        new_property = property(fget, fset, fdel)
    else:
        raise TypeError("Unsupported setup for property functions!")

    add_traits(target, new_property, **kwargs)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
