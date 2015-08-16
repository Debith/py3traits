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

from pytraits.support import Inspector, Singleton


class TraitInspector(metaclass=Singleton):
    """ Trait specific implementation of Inspector.

    This class is extension to general purpose Inspector. While original
    inspector gives string as a result of inspection, this class provides
    whole class (a.k.a Primitive) to caller. These primitives then provide
    special functionality for given object type.

    This class acts also as a singleton.
    """
    def __init__(self):
        self.__inspector = Inspector()

    def __call__(self, object):
        return self.__inspector.inspect(object)

    @classmethod
    def add_hook(cls, name, hook):
        cls().__inspector.add_hook(name, hook)

    @classmethod
    def add_default_hook(cls, hook):
        cls().__inspector.add_default_hook(hook)


class TraitTargetInspector(TraitInspector):
    """ Inspector used to identify target objects for trait composition. """
    TYPE = "target"


class TraitSourceInspector(TraitInspector):
    """ Inspector used to identify source objects for trait composition """
    TYPE = "source"


if __name__ == "__main__":
    import doctest
    doctest.testmod()
