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

from pytraits.core.errors import BuiltinSourceError, PropertySourceError
from pytraits.sources.clazz import ClassSource
from pytraits.sources.instance import InstanceSource
from pytraits.sources.routine import RoutineSource
from pytraits.sources.prop import PropertySource


class TraitSource(object):
    """
    Creates trait source object.
    """
    def __new__(self, obj):
        if getattr(obj, '__module__', '') == 'builtins':
            raise BuiltinSourceError()
        elif inspect.isroutine(obj):
            return RoutineSource(obj)
        elif inspect.isdatadescriptor(obj):
            return PropertySource(obj)
        elif inspect.isclass(obj):
            return ClassSource(obj)
        elif not isinstance(obj, type):
            return InstanceSource(obj)
        else:
            raise PropertySourceError()
