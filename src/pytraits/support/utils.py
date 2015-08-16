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


def is_sysname(name: str):
    """ Quick check if name is system specific.

    When doing lot of introspection with functions and attributes, very often
    arises a situation to check, if attribute name is following pattern used
    by Python for system attributes. This simple function allows to identify
    them in simple fashion without need to write same pattern everywhere.

    >>> is_sysname("test")
    False
    >>> is_sysname("__test")
    False
    >>> is_sysname("__test__")
    True
    >>> is_sysname("_test_")
    False
    """
    return name.startswith('__') and name.endswith('__')


def is_container(obj):
    """ Checks whether the object is container or not.

    Container is considered an object, which includes other objects,
    thus string is not qualified, even it implments iterator protocol.

    >>> is_container("text")
    False

    >>> is_container(tuple())
    True
    """
    if isinstance(obj, str):
        return False

    return hasattr(obj, '__iter__')


def has_dict_protocol(obj):
    """ Checks whether object supports dict protocol. """
    return hasattr(obj, "__getitem__") and hasattr(obj, "__setitem__")


def flatten(items):
    """ Flatten the nested arrays into single one.

    Example about list of lists.
    >>> list(flatten([[1, 2], [3, 4]]))
    [1, 2, 3, 4]

    Example of deeply nested irregular list:
    >>> list(flatten([[[1, 2]], [[[3]]], 4, 5, [[6, [7, 8]]]]))
    [1, 2, 3, 4, 5, 6, 7, 8]

    List of strings is handled properly too
    >>> list(flatten(["one", "two", ["three", "four"]]))
    ['one', 'two', 'three', 'four']
    """
    for subitem in items:
        if is_container(subitem):
            for item in flatten(subitem):
                yield item
        else:
            yield subitem


def get_signature(function):
    """ Constructs signature of function.

    >>> def test(arg, *args, **kwargs): pass
    >>> get_signature(test)
    'test(arg, *args, **kwargs)'

    >>> class Test:
    ...     def test(self, arg, *args, **kwargs): pass
    ...
    >>> get_signature(Test.test)
    'Test.test(self, arg, *args, **kwargs)'
    """
    sig = inspect.signature(function)
    return "{}{}".format(get_func_name(function), str(sig))


def get_func_name(routine, fullname=True):
    """ Returns name of the function as a string.

    Full name examples, where we get the __qualname__.
    >>> class Test:
    ...     def test_method(self): pass
    ...
    ...     @classmethod
    ...     def test_classmethod(cls): pass
    ...
    ...     @staticmethod
    ...     def test_staticmethod(): pass
    ...
    >>> get_func_name(Test.test_method)
    'Test.test_method'
    >>> get_func_name(Test.test_classmethod)
    'Test.test_classmethod'
    >>> get_func_name(Test.test_staticmethod)
    'Test.test_staticmethod'

    Examples where we want to have just __name__.
    >>> get_func_name(Test.test_method, fullname=False)
    'test_method'
    >>> get_func_name(Test.test_classmethod, fullname=False)
    'test_classmethod'
    >>> get_func_name(Test.test_staticmethod, fullname=False)
    'test_staticmethod'

    >>> def test_function(): pass
    >>> get_func_name(test_function)
    'test_function'
    >>> get_func_name(test_function, fullname=False)
    'test_function'
    """
    name_attr = '__qualname__' if fullname else '__name__'
    try:
        return getattr(routine, name_attr)
    except AttributeError:
        function = getattr(routine, '__func__', routine)
        return function.__name__

if __name__ == "__main__":
    import doctest
    doctest.testmod()
