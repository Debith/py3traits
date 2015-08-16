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

from pytraits.support import get_func_name
from .trait_object import TraitObject


class FunctionObject(TraitObject):
    """ This class encapsulates handling of function objects.

    Generally, there's no functions in terms of traits. Functions are turned to
    something else since they behave differently depending on the context, like
    pure functions for class should be staticmethods since they are not likely to
    do any modifications to class (or instance) itself.
    """
    @classmethod
    def hook_into(cls, inspector):
        if inspector.TYPE == 'source':
            inspector.add_hook('function', cls.check)

    @staticmethod
    def check(object):
        args = object.__code__.co_varnames

        # Functions without arguments are considered to be static
        # methods.
        if len(args) == 0:
            return StaticMethodObject(object)

        # Function, that has first argument 'self', wants to be method.
        elif args[0] == 'self':
            return MethodObject(object)

        # Function, that has first argument 'cls', wants to be classmethod.
        elif args[0] == 'cls':
            return ClassMethodObject(object)

        # Other functions are to be static methods.
        else:
            return StaticMethodObject(object)


class RoutineObject(TraitObject):
    @property
    def name(self):
        return get_func_name(self._object, False)

    @property
    def compile_target(self):
        return self._object

    def recompile(self, target, name):
        return self._compiler.recompile(self.compile_target, target.compile_target, name)


class MethodObject(RoutineObject):
    """ This class encapsulates handling of methods.
    """
    INSPECTORS = ('source',)

    def rebind(self, target, source):
        # TODO: Can this be made prettier?
        if target.compile_target == target.bind_target:
            return source.__get__(None, target.compile_target)
        return source.__get__(target.bind_target, target.compile_target)


class ClassMethodObject(RoutineObject):
    """ This class encapsulates handling of classmethods.

    This class is able handle functions that are decorated with classmethod
    and pure functions that have 'cls' as a first argument.
    """
    INSPECTORS = ('source',)

    @property
    def compile_target(self):
        return getattr(self._object, '__func__', self._object)

    def rebind(self, target, source):
        return source.__get__(target.bind_target, target.bind_target)


class StaticMethodObject(RoutineObject):
    """ This class encapsulates handling of staticmethods.
    """
    INSPECTORS = ('source',)

    @property
    def compile_target(self):
        return getattr(self._object, '__func__', self._object)

    def rebind(self, target, source):
        return source.__get__(None, target.compile_target)


# TODO: where to go?
def wrap_builtin(builtin_func):
    def wrapper(self, *args, **kwargs):
        return builtin_func(*args, **kwargs)
    return wrapper


class BuiltinObject(MethodObject):
    """ This class encapsulates handling of builtin functions. """
    INSPECTORS = ('source',)

    def recompile(self, target, name):
        return lambda *args, **kwargs: self._object(*args[1:], **kwargs)
