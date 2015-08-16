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

from pytraits.support import flatten, type_converted
from pytraits.support.errors import (FirstTraitArgumentError,
                                     TraitArgumentTypeError)
from pytraits.core import TraitFactory

TraitSource = TraitFactory["TraitSourceInspector"]
Resolutions = TraitFactory["Resolutions"]


@TraitFactory.register
class Traits:
    """ This class encapsulates handling of multiple traits. """
    def __init__(self, traits):
        self.__traits = traits

    @classmethod
    def create(cls, traits):
        instance = cls(traits)

        # In case object and strings are given, we need to do some extra work
        # to get desired traits out.
        if instance.needs_preprocessing():
            instance.preprocess()
        return instance

    def needs_preprocessing(self):
        """ Identifies need to resolve attributes for string arguments within trait source.

        In order to support following syntax:
            add_traits(Target, Source, "all", "its", "required", "attributes")
        we need to turn those strings to objects. This function is to used to
        identify that need.
        """
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

    def preprocess(self):
        obj = self.__traits[0]
        names = self.__traits[1:]
        self.__traits = [getattr(obj, name) for name in names]

    def __iter__(self):
        """ Walk through each given trait.

        Any class source is walked through for its contents.
        """
        for trait in flatten(map(TraitSource, self.__traits)):
            yield trait

    @type_converted
    def compose(self, target, resolutions: Resolutions):
        """ Compose trait sources to target using composer. """
        for source in self:
            TraitFactory["Composer"](target, source).compose(resolutions)
