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

from pytraits.core import TraitFactory


@TraitFactory.register
class Resolutions:
    """ Container of resolutions for possible conflicts during composition.

    During composition process, function or property names can collide and
    every situation should be handled by user at the same time the traits
    are composed. That will guarantee that class or instance will behave
    as expected in every situation.
    """
    def __init__(self, resolutions):
        self.__resolutions = resolutions

    def resolve(self, name):
        """ Resolves name that shall be used for trait being composed.

        NOTE: Currently it is possible to rename traits but collisions are
              not checked.

        Returns:
            (string) name of the trait
            (NoneType) nothing is returned in case trait should be ignored

        Raises:
            Error if there is a conflict but no resolution.
        """
        return self.__resolutions.get(name, name)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
