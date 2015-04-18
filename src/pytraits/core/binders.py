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


def bind_method_to_class(clazz, method, name=None):
    """
    Binds a single method into class.

    This can be very useful in situation, where your trait properties
    are dynamic, and you first need to construct your trait in some
    fashion and after the trait is ready, you can transfer the qualities
    to some class (You don't have always full control to creation
    process).

    @param clazz: Class to be extended
    @param method: Method that is added as a trait into class
    @param name: New name for the method. When omitted, original is used.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._value = 42
    ...
    >>> class MyTrait(object):
    ...     def __init__(self):
    ...         self._value = 0
    ...
    ...     def trait_method(self):
    ...         return self.__class__.__name__, self._value
    ...
    >>> my_trait = MyTrait()
    >>> bind_method_to_class(MyClass, my_trait.trait_method)
    >>> MyClass().trait_method()
    ('MyClass', 42)

    >>> my_trait.trait_method()
    ('MyTrait', 0)
    """
    # Rip out the original function from the class and set it also
    # as member of our new class.
    clazz_function = method.__self__.__class__.__dict__[method.__name__]
    setattr(clazz, name or method.__name__, clazz_function)


def bind_function_to_class(clazz, function, name=None):
    """
    Binds a single function into class.

    In practice this method turns any function as a unbound method into
    class.

    @param clazz: Class to be extended
    @param function: Function that is added as a trait into class
    @param name: New name for the method. When omitted, original is used.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._value = 42
    ...
    >>> def trait_function(self):
    ...     return self.__class__.__name__, self._value
    ...
    >>> bind_function_to_class(MyClass, trait_function)
    >>> MyClass().trait_function()
    ('MyClass', 42)
    """
    setattr(clazz, name or function.__name__, function)


def bind_property_to_class(clazz, prop, name):
    """
    Binds a single property into class.

    @param clazz: Class to be extended
    @param prop: Property that is added as a trait into class
    @param name: New name for the property. Mandatory for properties.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._value = 42
    ...
    >>> class MyTrait(object):
    ...     def __init__(self):
    ...         self._value = 0
    ...
    ...     @property
    ...     def value(self):
    ...         return self.__class__.__name__, self._value
    ...
    >>> bind_property_to_class(MyClass, MyTrait.value, 'value')
    >>> MyClass().value
    ('MyClass', 42)
    """
    setattr(clazz, name, prop)


def bind_method_to_instance(instance, method, name=None):
    """
    @param instance: Instance to be extended.
    @param name: New name for the method. When omitted, original is used.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._value = 327
    ...
    >>> class MyTrait(object):
    ...     def __init__(self):
    ...         self._value = 331
    ...
    ...     def method(self):
    ...         return self.__class__.__name__, self._value
    ...
    >>> instance = MyClass()
    >>> trait = MyTrait()
    >>> bind_method_to_instance(instance, trait.method)
    >>> instance.method()
    ('MyClass', 327)

    >>> trait.method()
    ('MyTrait', 331)
    """
    clazz_function = method.__self__.__class__.__dict__[method.__name__]
    bound_method = clazz_function.__get__(instance, instance.__class__)
    instance.__dict__[name or method.__name__] = bound_method


def bind_function_to_instance(instance, function, name=None):
    """

    @param instance: Instance to be extended.
    @param name: New name for the method. When omitted, original is used.

    >>> class MyClass(object):
    ...     def __init__(self):
    ...         self._value = 42
    ...
    >>> def trait_function(self):
    ...     return self.__class__.__name__, self._value
    ...
    >>> my_instance = MyClass()
    >>> bind_function_to_instance(my_instance, trait_function)
    >>> my_instance.trait_function()
    ('MyClass', 42)

    >>> 'trait_function' in vars(MyClass)
    False
    """
    # Functions are always descriptors. Here, we are getting
    # class trait which contains a functions we desire to transfer.
    # Inside class.__dict__, function is stored as type function, so
    # idea here is to get the function out from the class, bind it
    # to new instance and store it there.
    #
    # See more: http://users.rcn.com/python/download/Descriptor.htm
    new_function = function.__get__(instance, instance.__class__)
    instance.__dict__[name or function.__name__] = new_function


def bind_property_to_instance(instance, trait, name=None):
    """

    @param instance: Instance to be extended.
    @param name: New name for the method. When omitted, original is used.

    >>> class MyClass:
    ...    def __init__(self):
    ...        self._value = 42
    ...
    >>> class MyTrait:
    ...     @property
    ...     def value(self):
    ...         return self._value
    ...
    >>> my_instance = MyClass()
    >>> bind_property_to_instance(my_instance, MyTrait.value, 'value')
    >>> my_instance.value
    42
    """
    setattr(instance.__class__, name, trait)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
