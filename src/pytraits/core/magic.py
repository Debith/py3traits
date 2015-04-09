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
import functools
import itertools

class type_converted:
    """
    Decorator to enforce types and do auto conversion to values.

    >>> @type_converted
    ... def convert(value: int, answer: bool):
    ...     return value, answer
    ...
    >>> convert("12", "false")
    (12, False)

    >>> class Example:
    ...     @type_converted
    ...     def convert(self, value: int, answer: bool):
    ...       return value, answer
    ...
    >>> Example().convert("12", 0)
    (12, False)
    """
    def __init__(self, function):
        self.__function = function
        self.__self = None
        self.__converters = {bool: self.boolean_conversion}

    def convert(self, arg_type, arg_name, arg_value):
        """
        Converts argument to given type.
        """
        # If no type required, return value as is.
        if arg_type is None:
          return arg_value

        try:
          try:
            return self.__converters[arg_type](arg_value)
          except KeyError:
            return arg_type(arg_value)
        except:
          msg = "While calling %s, offered value for argument '%s' was '%s', which cannot be converted to %s!"
          params = (self.function_signature(), arg_name, arg_value, arg_type)
          raise TypeError(msg % params)

    def boolean_conversion(self, value):
        """
        Convert given value to boolean.

        >>> conv = type_converted(None)
        >>> conv.boolean_conversion("True"), conv.boolean_conversion("false")
        (True, False)

        >>> conv.boolean_conversion(1), conv.boolean_conversion(0)
        (True, False)
        """
        if isinstance(value, bool):
          return value

        elif isinstance(value, str):
          if value.lower() == "true":
            return True
          if value.lower() == "false":
            return False

        elif isinstance(value, int):
          if not value:
            return False
          if value == 1:
            return True

        raise TypeError()

    def __get__(self, instance, clazz):
        """
        Stores calling instances and returns this decorator object as function.
        """
        # In Python, every function is a property. Before Python invokes function,
        # it must access the funtion using __get__, where it can deliver the calling
        # object. After the __get__, function is ready for being invoked by __call__.
        self.__self = instance
        return self

    def iter_positional_args(self, args):
        """
        Yields type, name, value combination of function arguments.
        """
        specs = inspect.getfullargspec(self.__function)

        # Methods require instance of the class to be first argument. We
        # stored it in __get__ and now add it to argument list so that
        # function can be invoked correctly.
        if self.__self:
          args = (self.__self, ) + args

        for spec, arg in itertools.zip_longest(specs.args, args, fillvalue=None):
          yield self.__function.__annotations__.get(spec, None), spec, arg

    def function_signature(self):
        """
        Returns signature and class of currently invoked function.

        >>> @type_converted
        ... def test(value: int, answer: bool): pass
        >>> test.function_signature()
        'test(value:int, answer:bool)'
        """
        sig = str(inspect.signature(self.__function))
        name = self.__function.__name__
        if self.__self:
          return "%s.%s%s" % (self.__self.__class__.__name__, name, sig)
        else:
          return "%s%s" % (name, sig)

    def __call__(self, *args, **kwargs):
        """
        Converts annotated types into proper type and calls original function.
        """
        new_args = []
        for arg_type, arg_name, arg_value in self.iter_positional_args(args):
          new_args.append(self.convert(arg_type, arg_name, arg_value))
        return self.__function(*new_args, **kwargs)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
