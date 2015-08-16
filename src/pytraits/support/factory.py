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

from pytraits.support import Singleton
from pytraits.support.errors import (FactoryError,
                                     FactoryRegisterError,
                                     FactoryClassMissingError)

__all__ = ["Factory"]


class FactoryType(Singleton):
    """ Convenience type for factory to allow dictionary type access to objects."""
    def __getitem__(cls, name):
        return cls()[name]

    def __call__(cls, *args, **kwargs):
        if cls is Factory:
            raise FactoryError()
        return super().__call__(*args, **kwargs)


class Factory(metaclass=FactoryType):
    """ Simple factory to register and create objects.

    This class contains multiple ways to hold and create instances of classes.
    This class also works as a container for all those classes that are
    registered in and can those classes can be accessed from anywhere by simply
    importing that factory.

    The main mechanism in python to create and initialize objects are __new__
    and __init__ functions. It is also a good habit to avoid any conditional
    logic inside class constructor, thus writing own create classmethod is
    recommended and also supported by this factory. By using own class method
    for creating the object, it makes far more easier to setup and test classes
    you write since the __init__ method is left for simple assignments.

    NOTE: This factory is abstract thus anyone using it must inherit own
          version before instantiating it.

    >>> class ExampleFactory(Factory):
    ...     pass
    ...
    >>> @ExampleFactory.register
    ... class ExampleObject:
    ...     def __init__(self, name, **kwargs):
    ...         self.name = name
    ...
    ...     @classmethod
    ...     def create(cls, *args, **kwargs):
    ...         return cls(*args, **kwargs)
    ...
    >>> example_instance = ExampleFactory["ExampleObject"]("MyObject")
    >>> example_instance.name
    'MyObject'
    """
    def __init__(self, override_duplicates=False):
        self.__methods = {}
        self.__classes = {}
        self.__override_duplicates = override_duplicates

    @classmethod
    def register(cls, *classes, override=False, autoinit=True):
        """ Decorator function to register classes to this factory. """
        assert classes, "No classes provided!"

        # This is singleton, so we can get the singleton instance directly
        # here and start filling it.
        self = cls()
        for clazz in classes:
            self.__register(clazz, override=override, autoinit=autoinit)

        # When single class is registered, return it too so that
        # this function can act as a class decorator.
        if len(classes) == 1:
            return classes[0]

    def __register(self, clazz, override, autoinit):
        assert inspect.isclass(clazz)

        # Make sure duplicates are not registered. By default, raise error
        # in order to avoid weird debugging errors. Duplicates, if tolerated,
        # can be
        override |= self.__override_duplicates
        if self.exists(clazz) and not override:
            # TODO: Record traceback for each registered object.
            msg = "Name '{}' already found from factory"
            raise FactoryRegisterError(msg.format(clazz.__name__))

        # Keep a list of classes in case there is a need to override them.
        self.__classes[clazz.__name__] = clazz

        # In case the clazz defines __call__ function, it is considered
        # as subfactory, which means we try to initialize the clazz
        # and use it's instance as a factory method. Setting autoinit to
        # False will of course prevent that behavior.
        if "__call__" in dir(clazz) and autoinit:
            self.__methods[clazz.__name__] = getattr(clazz, 'create', clazz)()
        else:
            self.__methods[clazz.__name__] = getattr(clazz, 'create', clazz)

        return clazz

    def __access(self, collection, name):
        try:
            return collection[name]
        except KeyError:
            msg = "Name '{}' is not in registered list: {}"
            msg = msg.format(name, self.registered_classes)
            raise FactoryClassMissingError(msg)

    def __getitem__(self, name):
        """ Returns factory method of registered object.

        @see constructor
        """
        return self.__access(self.__methods, name)

    def exists(self, clazz):
        """ Convenience function to check if class is already exists. """
        return clazz.__name__ in self.__classes

    def original_class(self, name):
        """ Retrieves the original registered class. """
        return self.__access(self.__classes, name)

    @classmethod
    def reset(cls):
        """ Removes all registered classes. """
        cls().__methods.clear()
        cls().__classes.clear()

    @property
    def registered_classes(self):
        return list(self.__classes.keys())


if __name__ == "__main__":
    import doctest
    doctest.testmod()
