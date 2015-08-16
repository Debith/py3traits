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


from pytraits.support import is_sysname
from .trait_object import TraitObject
from ..base import TraitFactory


class ClassObject(TraitObject):
    INSPECTORS = ('source', 'target')

    def __iter__(self):
        """ Yields each element in the class. """
        for name, object in self.items():
            sub = TraitFactory["TraitSourceInspector"](object)
            if sub:
                yield sub

    def __dir__(self):
        return [i[0] for i in self.items()]

    def __getitem__(self, key):
        return self._object.__dict__[key]

    def __setitem__(self, key, value):
        setattr(self._object, key, value)

    def items(self):
        return ((k, v) for (k, v) in self._object.__dict__.items() if not is_sysname(k))

    @property
    def compile_target(self):
        return self._object

    @property
    def bind_target(self):
        return self._object
