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

from pytraits.sources.routine import RoutineSource


class PropertySource:
    def __init__(self, prop, resolutions):
        self._property = prop
        self._resolutions = resolutions

    def for_class(self, clazz):
        name = self._resolutions.get(self._property.fget.__name__, self._property.fget.__name__)
        getter = RoutineSource(self._property.fget, name)
        getter.for_class(clazz)
        setattr(clazz, name, property(getattr(clazz, name)))

    def for_instance(self, instance):
        setattr(instance.__class__, self._name, self._property)
