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

from pytraits.core.errors import  UnextendableObjectError
from pytraits.targets.clazz import ClassTarget
from pytraits.targets.instance import InstanceTarget

class TraitTarget(object):
    """
    Creates trait target object.
    """
    def __new__(self, obj):
        if getattr(obj, '__module__', '') == 'builtins':
            raise UnextendableObjectError('Built-in objects can not be extended!')
        elif inspect.isroutine(obj):
            raise UnextendableObjectError('Function objects can not be extended!')
        elif not isinstance(obj, type):
            return InstanceTarget(obj)
        elif inspect.isclass(obj):
            return ClassTarget(obj)
        else:
            raise UnextendableObjectError('Properties can not be extended!')