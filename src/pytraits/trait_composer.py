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

from pytraits.core import Singleton
from pytraits.targets import TraitTarget
from pytraits.sources import Traits


class TraitComposer:
    """
    Main class that handles composing traits into target object.
    """
    __metaclass__ = Singleton

    def bind_traits(self, obj, *traits):
        """
        Bind new traits to given object.

        @param obj: Object of any type that is going to be extended with traits
        @param traits: Tuple of traits as strings or callables or functions.
        @param resolved_conflicts: dictionary of conflict resolutions to solve
                                   situations where multiple methods of same
                                   name are encountered in traits.

        >>> class ExampleClass:
        ...    def example_method(self):
        ...        return None
        ...
        >>> class ExampleTrait:
        ...    def example_method(self):
        ...        return 42
        ...
        """
        # Return immediately, if no traits provided.
        if not len(traits):
            return

        # Attempt to cretate target context object. Builtins are not supported
        # thus exception is raised.
        target_object = TraitTarget(obj)

        # Compose traits into target object
        target_object.add_traits(Traits(traits))


add_traits = TraitComposer().bind_traits

if __name__ == '__main__':
    import doctest
    doctest.testmod()
