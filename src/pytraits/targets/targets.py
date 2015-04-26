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

from pytraits.core.errors import UnextendableObjectError
from pytraits.core.magic import type_safe
from pytraits.sources import Traits


class TraitTarget:
    """
    Creates trait target object.
    """
    def __new__(self, obj):
        if getattr(obj, '__module__', '') == 'builtins':
            raise UnextendableObjectError('Built-in objects can not be extended!')

        elif inspect.isroutine(obj):
            raise UnextendableObjectError('Function objects can not be extended!')

        elif not isinstance(obj, type):
            return Target(obj, "for_instance")

        elif inspect.isclass(obj):
            return Target(obj, "for_class")

        else:
            raise UnextendableObjectError('Properties can not be extended!')


class Target:
    """
    Encapsulates target object composition for classes and class instances.
    """
    def __init__(self, target, function_typename):
        self._target = target
        self._function_typename = function_typename

    def add_traits(self, traits, resolutions):
        traits = Traits(traits, resolutions)
        for trait in traits:
            getattr(trait, self._function_typename)(self._target)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
