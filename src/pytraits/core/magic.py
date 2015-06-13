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
import itertools

from pytraits.core.errors import TypeConversionError


__all__ = ["type_safe", "type_converted"]


class ErrorMessage:
    """
    Encapsulates building of error message.
    """
    def __init__(self, main_msg, repeat_msg, get_func_name):
        self.__errors = []
        self.__get_func_name = get_func_name
        self.__main_msg = main_msg
        self.__repeat_msg = repeat_msg

    def __bool__(self):
        return bool(self.__errors)

    def __str__(self):
        msg = [self.__main_msg.format(self.__get_func_name())]
        for error in self.__errors:
            msg.append("   - " + self.__repeat_msg.format(**error))
        return "\n".join(msg)

    def set_main_messsage(self, msg):
        self.__main_msg = msg

    def set_repeat_message(self, msg):
        self.__repeat_msg = msg

    def add(self, **kwargs):
        self.__errors.append(kwargs)

    def reset(self):
        self.__errors = []


class type_safe:
    """
    Decorator to enforce type safety. It certainly kills some ducks
    but allows us also to fail fast.

    >>> @type_safe
    ... def check(value: int, answer: bool, anything):
    ...     return value, answer, anything
    ...

    >>> check("12", "false", True)
    Traceback (most recent call last):
    ...
    TypeError: While calling check(value:int, answer:bool, anything):
       - parameter 'value' had value '12' of type 'str'
       - parameter 'answer' had value 'false' of type 'str'

    >>> check(1000, True)
    Traceback (most recent call last):
    ...
    TypeError: check() missing 1 required positional argument: 'anything'
    """
    def __init__(self, function):
        self._function = function
        self.__signature = inspect.signature(function)
        self.__doc__ = function.__doc__
        self._specs = inspect.getfullargspec(self._function)
        self._self = None
        self._errors = ErrorMessage(
            'While calling {}:',
            "parameter '{name}' had value '{value}' of type '{typename}'",
            self.signature)

    def __get__(self, instance, clazz):
        """
        Stores calling instances and returns this decorator object as function.
        """
        # In Python, every function is a property. Before Python invokes function,
        # it must access the function using __get__, where it can deliver the calling
        # object. After the __get__, function is ready for being invoked by __call__.
        self._self = instance
        return self

    def iter_positional_args(self, args):
        """
        Yields type, name, value combination of function arguments.
        """
        # specs.args contains all arguments of the function. Loop here all
        # argument names and their values putting them together. If there
        # are arguments missing values, fill them with None.
        for name, val in itertools.zip_longest(self._specs.args, args, fillvalue=None):
            # __annotations__ is a dictionary of argument name and annotation.
            # We accept empty annotations, in which case the argument has no
            # type requirement.
            yield self._function.__annotations__.get(name, None), name, val

    def signature(self):
        """
        Returns signature and class of currently invoked function.

        >>> @type_converted
        ... def test(value: int, answer: bool): pass
        >>> test.signature()
        'test(value:int, answer:bool)'
        """
        sig = inspect.signature(self._function)
        name = self._function.__name__
        if self._self:
            return "%s.%s%s" % (self._self.__class__.__name__, name, str(sig))
        else:
            return "%s%s" % (name, str(sig))

    def _analyze_args(self, args):
        """
        Invoked by __call__ in order to work with positional arguments.

        This function does the actual work of evaluating arguments against
        their annotations. Any deriving class can override this function
        to do different kind of handling for the arguments. Overriding function
        must return list of arguments that will be used to call the decorated
        function.

        @param args: Arguments given for the function.
        @return same list of arguments given in parameter.
        """
        # TODO: inspect.Signature does quite lot of similar things. Figure
        #       out, how to take advantage of that.
        for arg_type, arg_name, arg_value in self.iter_positional_args(args):
            if not arg_type or isinstance(arg_value, arg_type):
                continue

            self._errors.add(
                typename=type(arg_value).__name__,
                name=arg_name,
                value=arg_value)

        if self._errors:
            raise TypeError(str(self._errors))

        return args

    def __match_arg_count(self, args):
        """
        Verifies that proper number of arguments are given to function.
        """
        # With default values this verification is bit tricky. In case
        # given arguments match with number of arguments in function signature,
        # we can proceed.
        if len(args) == len(self._specs.args):
            return True

        # It's possible to have less arguments given than defined in function
        # signature in case any default values exist.
        if len(args) - len(self._specs.defaults or []) == len(self._specs.args):
            return True

        # When exceeding number of args, also check if function accepts
        # indefinite number of positional arguments.
        if len(args) > len(self._specs.args) and self._specs.varargs:
            return True

        # We got either too many arguments or too few.
        return False

    def __call__(self, *args, **kwargs):
        """
        Converts annotated types into proper type and calls original function.
        """
        self._errors.reset()

        # Methods require instance of the class to be first argument. We
        # stored it in __get__ and now add it to argument list so that
        # function can be invoked correctly.
        if self._self:
            args = (self._self, ) + args

        # Before doing any type checks, make sure argument count matches.
        if self.__match_arg_count(args):
            args = self._analyze_args(args)

        return self._function(*args, **kwargs)


class type_converted(type_safe):
    """
    Decorator to enforce types and do auto conversion to values.

    >>> @type_converted
    ... def convert(value: int, answer: bool, anything):
    ...     return value, answer, anything
    ...
    >>> convert("12", "false", None)
    (12, False, None)

    >>> class Example:
    ...     @type_converted
    ...     def convert(self, value: int, answer: bool, anything):
    ...       return value, answer, anything
    ...
    >>> Example().convert("12", 0, "some value")
    (12, False, 'some value')

    >>> Example().convert(None, None, None)
    Traceback (most recent call last):
    ...
    pytraits.core.errors.TypeConversionError: While calling Example.convert(self, value:int, answer:bool, anything):
       - got arg 'value' as 'None' of type 'NoneType' which cannot be converted to 'int'
       - got arg 'answer' as 'None' of type 'NoneType' which cannot be converted to 'bool'
    """
    def __init__(self, function):
        super().__init__(function)
        self.__converters = {bool: self.boolean_conversion}
        self._errors = ErrorMessage(
            'While calling {}:',
            "got arg '{name}' as '{value}' of type '{typename}' "
            "which cannot be converted to '{expectedtype}'",
            self.signature)

    def convert(self, arg_type, arg_name, arg_value):
        """
        Converts argument to given type.
        """
        # If no type required, return value as is.
        if arg_type is None:
            return arg_value

        try:
            return self.__converters[arg_type](arg_value)
        except KeyError:
            return arg_type(arg_value)

    def boolean_conversion(self, value):
        """
        Convert given value to boolean.

        >>> conv = type_converted(lambda self: None)
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

        raise TypeConversionError()  # This will be caught by convert method.

    def _analyze_args(self, args):
        """
        Converts annotated types into proper type and calls original function.
        """
        self._errors.reset()
        new_args = []

        for arg_type, arg_name, arg_value in self.iter_positional_args(args):
            try:
                new_args.append(self.convert(arg_type, arg_name, arg_value))
            except (TypeConversionError, TypeError):
                self._errors.add(
                    name=arg_name,
                    value=arg_value,
                    typename=type(arg_value).__name__,
                    expectedtype=arg_type.__name__)

        if self._errors:
            raise TypeConversionError(str(self._errors))

        return new_args


if __name__ == "__main__":
    import doctest
    doctest.testmod()
