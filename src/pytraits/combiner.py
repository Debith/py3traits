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

from pytraits.trait_composer import add_traits


def combine_class(class_name, *traits, **resolved_conflicts):
    """
    This function composes new class out of any number of traits.

    >>> class One:
    ...     def first(self): return 1
    ...
    >>> class Two:
    ...     def second(self): return 2
    ...
    >>> class Three:
    ...     def third(self): return 3
    ...
    >>> Combination = combine_class("Combination", One, Two, Three)
    >>> instance = Combination()
    >>> instance.first(), instance.second(), instance.third()
    (1, 2, 3)

    >>> instance.__class__.__name__
    'Combination'
    """
    NewClass = type(class_name, (object,), {})
    add_traits(NewClass, *traits)
    return NewClass


if __name__ == '__main__':
    import doctest
    doctest.testmod()
