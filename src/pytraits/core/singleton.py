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

from pytraits.core.errors import SingletonError


class Singleton(type):
    """
    Turn the class to immutable singleton.

    >>> class Example(object, metaclass=Singleton):
    ...    pass
    ...
    >>> a = Example()
    >>> b = Example()
    >>> id(a) == id(b)
    True

    Having your instance as a singleton is faster than creating from scratch
    >>> import timeit
    >>> class MySingleton(object, metaclass=Singleton):
    ...    def __init__(self):
    ...        self._store = dict(one=1, two=2, three=3, four=4)
    ...
    >>> class NonSingleton(object):
    ...    def __init__(self):
    ...        self._store = dict(one=1, two=2, three=3, four=4)
    ...
    >>> #timeit.timeit(NonSingleton) > timeit.timeit(MySingleton)
    True

    >>> MySingleton().new_item = False
    Traceback (most recent call last):
    ...
    errors.SingletonError: Singletons are immutable
    """
    def __call__(self, *args, **kwargs):
        try:
            return self.__instance
        except AttributeError:
            def immutable_object(*args):
                raise SingletonError()

            self.__instance = super(Singleton, self).__call__(*args, **kwargs)
            self.__setitem__ = immutable_object
            self.__setattr__ = immutable_object
            return self.__instance
        
if __name__ == "__main__":
    import doctest
    doctest.testmod()