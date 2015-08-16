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


class InstanceObject(TraitObject):
    INSPECTORS = ('source', 'target')

    def __iter__(self):
        """ Yields each element in the class. """
        for name, object in self.items():
            sub = TraitFactory["TraitSourceInspector"](object)
            if sub:
                yield sub

    def __dir__(self):
        return [i[0] for i in self.items()]

    def __getitem__(self, name):
        try:
            return self._object.__class__.__dict__[name]
        except KeyError:
            return self._object.__dict__[name]

    def __setitem__(self, key, value):
        self._object.__dict__[key] = value

    @property
    def compile_target(self):
        return self._object.__class__

    @property
    def bind_target(self):
        return self._object

    def items(self):
        items = dict()
        items.update(self._object.__class__.__dict__)
        items.update(self._object.__dict__)  # Makes sure that instance values override class values.
        return ((k, v) for (k, v) in items.items() if not is_sysname(k))

    def forge(self):
        """ Modifies instance's class to be unique.

        This method creates a clone of instance's class and replaces the
        original class with the clone. By doing this, it allows modifying
        instance in a manner that no changes are reflected to other instances
        of the same class.

        This is mainly needed to make properties and other descriptors work
        so that they can be instance specific. They normally work only on classes

        """
        # In case the object's class is already forged, no need to do it again.
        if not hasattr(self._object, '__instance_forged'):
            # Retrieve the class of the object and create new class inherited
            # from it. It can be used on this instance again.
            original_class = self._object.__class__
            new_class = type(original_class.__name__, (original_class, ), {})
            new_class.__instance_forged = True

            # Replace the class with forged class.
            self._object.__class__ = new_class
