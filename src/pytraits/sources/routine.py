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

import sys
import types
import inspect
import collections

__all__ = ['RoutineSource']


def clone_function(function):
    trait = collections.OrderedDict()
    trait["co_argcount"] = function.__code__.co_argcount
    if sys.version_info[0] == 3:
        trait["co_kwonlyargcount"] = function.__code__.co_kwonlyargcount
    trait["co_nlocals"] = function.__code__.co_nlocals
    trait["co_stacksize"] = function.__code__.co_stacksize
    trait["co_flags"] = function.__code__.co_flags
    trait["co_code"] = function.__code__.co_code
    trait["co_consts"] = function.__code__.co_consts
    trait["co_names"] = function.__code__.co_names
    trait["co_varnames"] = function.__code__.co_varnames
    trait["co_filename"] = function.__code__.co_filename
    trait["co_name"] = function.__code__.co_name
    trait["co_firstlineno"] = function.__code__.co_firstlineno
    trait["co_lnotab"] = function.__code__.co_lnotab
    return trait


def transfer_names(trait, clazz):
    items = []
    for item in trait["co_names"]:
        if not "__" in item:
            items.append(item)
        else:
            items.append("_%s%s" % (clazz.__name__, item[item.index('__'):]))
    trait["co_names"] = tuple(items)


def compile_trait(trait, globs):
    return types.FunctionType(types.CodeType(*trait.values()), globs)


def recompile(function, target, name):
    trait = clone_function(function)
    transfer_names(trait, target)
    trait["co_name"] = name or trait["co_name"]
    return compile_trait(trait, function.__globals__)    


class RoutineSource(object):
    """
    Identifies given routines

    >>> class Example(object):
    ...     @staticmethod
    ...     def static_method(): pass
    ...
    ...     @classmethod
    ...     def class_method(cls): pass
    ...
    ...     def method(self): pass
    ...
    >>> def self_function(self): pass
    >>> def cls_function(cls): pass
    >>> def function(): pass
    >>> instance = Example()

    >>> RoutineSource(Example.method).__class__.__name__
    'UnboundFunctionSource'

    >>> RoutineSource(instance.method).__class__.__name__
    'BoundFunctionSource'

    >>> RoutineSource(self_function).__class__.__name__
    'UnboundFunctionSource'

    >>> RoutineSource(Example.static_method).__class__.__name__
    'UnboundFunctionSource'

    >>> RoutineSource(Example.class_method).__class__.__name__
    'ClassMethodSource'

    >>> RoutineSource(instance.method).__class__.__name__
    'BoundFunctionSource'

    >>> type(Example.static_method)
    """
    def __new__(self, routine, name=None):
        try:
            first_arg = inspect.getargspec(routine)[0][0]
        except IndexError:
            first_arg = ""

        # Routine is considered method, when:
        #   - it is picked out as class().method
        if inspect.ismethod(routine):
            if inspect.isclass(routine.__self__):
                return ClassMethodSource(routine, name)
            return BoundFunctionSource(routine, name)
        else:            
            if first_arg == 'self':
                return UnboundFunctionSource(routine, name)
            elif first_arg == 'cls':
                return ClassMethodSource(routine, name)
            else: # static
                return StaticMethodSource(routine, name)


class BoundFunctionSource:
    def __init__(self, function, name = None):
        self._function = function
        self._name = name or function.__name__

    def for_class(self, clazz):
        new_method = recompile(self._function, clazz, self._name)
        setattr(clazz, self._name, new_method.__get__(None, clazz))

    def for_instance(self, instance):
        new_method = recompile(self._function, instance.__class__, self._name)  
        bound_method = new_method.__get__(instance, instance.__class__)    
        instance.__dict__[self._name] = bound_method


class ClassMethodSource:
    def __init__(self, function, name = None):
        self._function = function
        self._name = name or function.__name__

    def for_class(self, clazz):
        new_method = recompile(self._function, clazz, self._name)
        setattr(clazz, self._name, new_method.__get__(clazz, clazz))

    def for_instance(self, instance):
        new_method = recompile(self._function, instance.__class__, self._name)  
        bound_method = new_method.__get__(instance, instance.__class__)    
        instance.__dict__[self._name] = bound_method


class UnboundFunctionSource:
    def __init__(self, function, name = None):
        self._function = function
        self._name = name or function.__name__

    def for_class(self, clazz):
        setattr(clazz, self._name, recompile(self._function, clazz, self._name))

    def for_instance(self, instance):
        new_method = recompile(self._function, instance.__class__, self._name)    
        bound_method = new_method.__get__(instance, instance.__class__)  
        instance.__dict__[self._name] = bound_method


class StaticMethodSource:
    def __init__(self, function, name = None):
        self._function = function
        self._name = name or self._function.__name__

    if sys.version_info[0] == 3:
        def for_class(self, clazz):
            setattr(clazz, self._name, recompile(self._function, clazz, self._name))
    else:
        def for_class(self, clazz):
            new_method = recompile(self._function, clazz, self._name)
            setattr(clazz, self._name, staticmethod(new_method))

    def for_instance(self, instance):
        method = recompile(self._function, instance.__class__, self._name)    
        instance.__dict__[self._name] = method


if __name__  == "__main__":
    import doctest
    doctest.testmod()