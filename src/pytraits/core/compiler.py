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

import types
import inspect
import collections

__all__ = ['Compiler']


class Compiler:
    """
    Compiler to transfer the function to other class or instance.

    This class works as a heart of the whole system. To make function to be fully
    part of other class or instance, it needs to be recompiled on top of target
    object, as if it was written there in the first place. This is because internals
    of the function are read-only and we need to change them in order to access
    private attributes.
    """
    def _clone_function(self, function):
        trait = collections.OrderedDict()

        trait["co_argcount"] = function.__code__.co_argcount
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

    def _transfer_names(self, trait, clazz):
        items = []
        for item in trait["co_names"]:
            if "__" not in item or item.startswith('__') and item.endswith('__'):
                items.append(item)
            else:
                items.append("_%s%s" % (clazz.__name__, item[item.index('__'):]))
        trait["co_names"] = tuple(items)

    def _compile_trait(self, trait, globs):
        return types.FunctionType(types.CodeType(*trait.values()), globs)

    def recompile(self, function, target, name: str=""):
        """
        Recompile function on target object.

        @param function: Function to be recompiled
        @param target: Target class or instance
        @param {str} name: New name for the target
        """
        trait = self._clone_function(function)
        self._transfer_names(trait, target)
        trait["co_name"] = name or trait["co_name"].strip('<>')

        return self._compile_trait(trait, function.__globals__)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
