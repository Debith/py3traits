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

from pytraits.sources.routine import RoutineSource
from pytraits.sources.prop import PropertySource


class ClassSource(object):
    """

    """
    def __init__(self, clazz, resolutions):
        self._class = clazz
        self.__resolutions = resolutions

    def __iter__(self):
        for item in inspect.classify_class_attrs(self._class):
            # We don't copy stuff from builtin object. We are only interested
            # on things user has typed to class.
            if item.defining_class == object:
                continue

            if item.name.startswith('__') and item.name.endswith('__') and item.kind == "data":
                continue  # Ignore more builtin stuff

            if item.kind == "class method":
                yield RoutineSource(item.object.__func__)
            elif item.kind == "static method":
                yield RoutineSource(item.object.__func__)
            elif item.kind == "data":
                pass  # no support yet
            elif item.kind == "method":
                yield RoutineSource(item.object)
            elif item.kind == "property":
                yield PropertySource(item.object, self.__resolutions)
            else:
                raise TypeError("We do not recognize this item: %s" % item)
