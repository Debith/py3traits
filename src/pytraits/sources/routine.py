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

from pytraits.core.compiler import Compiler

__all__ = ['RoutineSource']


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
    'StaticMethodSource'

    >>> RoutineSource(Example.class_method).__class__.__name__
    'ClassMethodSource'

    >>> RoutineSource(instance.method).__class__.__name__
    'BoundFunctionSource'
    """
    def __new__(self, routine, name=None):
        try:
            first_arg = inspect.getargspec(routine)[0][0]
        except IndexError:
            first_arg = ""

        compiler = Compiler()

        # Routine is considered method, when:
        #   - it is picked out as class().method
        if inspect.ismethod(routine):
            if inspect.isclass(routine.__self__):
                return ClassMethodSource(compiler, routine, name)
            return BoundFunctionSource(compiler, routine, name)
        else:
            if first_arg == 'self':
                return UnboundFunctionSource(compiler, routine, name)
            elif first_arg == 'cls':
                return ClassMethodSource(compiler, routine, name)
            else:  # static
                return StaticMethodSource(compiler, routine, name)


class BoundFunctionSource:
    def __init__(self, compiler, function, name=None):
        self.__compiler = compiler
        self._function = function
        self._name = name or function.__name__

    def for_class(self, clazz):
        new_method = self.__compiler.recompile(self._function, clazz, self._name)
        setattr(clazz, self._name, new_method.__get__(None, clazz))

    def for_instance(self, instance):
        new_method = self.__compiler.recompile(self._function, instance.__class__, self._name)
        bound_method = new_method.__get__(instance, instance.__class__)
        instance.__dict__[self._name] = bound_method


class ClassMethodSource:
    def __init__(self, compiler, function, name=None):
        self.__compiler = compiler
        self._function = function
        self._name = name or function.__name__

    def for_class(self, clazz):
        new_method = self.__compiler.recompile(self._function, clazz, self._name)
        setattr(clazz, self._name, new_method.__get__(clazz, clazz))

    def for_instance(self, instance):
        new_method = self.__compiler.recompile(self._function, instance.__class__, self._name)
        bound_method = new_method.__get__(instance, instance.__class__)
        instance.__dict__[self._name] = bound_method


class UnboundFunctionSource:
    def __init__(self, compiler, function, name=None):
        self.__compiler = compiler
        self._function = function
        self._name = name or function.__name__

    def for_class(self, clazz):
        setattr(clazz, self._name, self.__compiler.recompile(self._function, clazz, self._name))

    def for_instance(self, instance):
        new_method = self.__compiler.recompile(self._function, instance.__class__, self._name)
        bound_method = new_method.__get__(instance, instance.__class__)
        instance.__dict__[self._name] = bound_method


class StaticMethodSource:
    def __init__(self, compiler, function, name=None):
        self.__compiler = compiler
        self._function = function
        self._name = name or self._function.__name__

    def for_class(self, clazz):
        setattr(clazz, self._name, self.__compiler.recompile(self._function, clazz, self._name))

    def for_instance(self, instance):
        method = self.__compiler.recompile(self._function, instance.__class__, self._name)
        instance.__dict__[self._name] = method


if __name__ == "__main__":
    import doctest
    doctest.testmod()
