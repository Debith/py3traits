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

from pytraits.core.compiler import Compiler


class PropertySource:
    def __init__(self, prop, resolutions):
        self.__compiler = Compiler()
        self._property = prop
        self._resolutions = resolutions

    def __recompile_property_func(self, func_name, clazz, new_name):
        func = getattr(self._property, func_name, None)
        if func:
            return self.__compiler.recompile(func, clazz, new_name)

    def for_class(self, clazz):
        name = self._resolutions.get(self._property.fget.__name__, None)
        name = name or self._property.fget.__name__

        getter = self.__recompile_property_func('fget', clazz, name)
        setter = self.__recompile_property_func('fset', clazz, name)
        deleter = self.__recompile_property_func('fdel', clazz, name)

        setattr(clazz, name, property(getter, setter, deleter))

    def for_instance(self, instance):
        self.for_class(instance.__class__)
