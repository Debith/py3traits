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
import itertools

from pytraits.core import flatten
from pytraits.core.errors import FirstTraitArgumentError, TraitArgumentTypeError
from pytraits.sources.factory import TraitSource


class Traits(object):
    def __init__(self, traits, resolutions):
        self.__traits = traits
        self.__resolutions = resolutions

    def needs_preprocessing(self):
        # Calculate number of string arguments so that we can give bit more
        # detailed error messages in case of some weird combinations are found.
        string_arg_count = 0
        for arg in self.__traits:
            if isinstance(arg, str):
                string_arg_count += 1

        # No string arguments means that all of the traits are objects, who
        # can be composed directly.
        if not string_arg_count:
            return False

        # First trait argument must be an object (instance or class), otherwise
        # none of this makes any sense.
        if isinstance(self.__traits[0], str) or inspect.isroutine(self.__traits[0]):
            raise FirstTraitArgumentError()

        # In case string arguments are provided, all of them have to be strings.
        if len(self.__traits[1:]) != string_arg_count:
            raise TraitArgumentTypeError()

        return True

    @classmethod
    def create(cls, traits, resolutions):
        instance = cls(traits, itertools.repeat(resolutions))

        # In case object and strings are given, we need to do some extra work
        # to get desired traits out.
        if instance.needs_preprocessing():
            obj = instance.__traits[0]
            names = instance.__traits[1:]
            instance.__traits = [getattr(obj, name) for name in names]
        return instance

    def __iter__(self):
        for trait in flatten(map(TraitSource, self.__traits, self.__resolutions)):
            yield trait
