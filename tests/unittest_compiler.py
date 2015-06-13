#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest

from utils import for_examples

from pytraits.core.compiler import Compiler


def empty_func(self):
    pass


class TestDummy:
    def __private_func(self): pass
    def _hidden_func(self): pass
    def public_func(self): pass


class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.compiler = Compiler()
        self.recompile = self.compiler.recompile
        self.test_class = type("TestClass", (), {})

    @for_examples(
        (lambda self: self.__private,       ('_TestClass__private', )),
        (lambda self: self.__internal__,    ('__internal__', )),
        (lambda self: self.public,          ('public', )),
        (lambda self: self.__private(),     ('_TestClass__private', )),
        (lambda self: self.public(),        ('public', )),
        (lambda self: (self.a, self._b, self._c, self.__d, self.__e),
                      ('a', '_b', '_c', '_TestClass__d', '_TestClass__e')),
        (empty_func,                        ()))
    def test_supports_converting_attribute_names(self, func, attributes):
        compiled = self.recompile(func, self.test_class, "test")
        self.assertEqual(compiled.__code__.co_names, attributes)

    @for_examples(
        (empty_func, "anything", "anything"),
        (empty_func, "", "empty_func"),
        (empty_func, None, "empty_func"),
        (lambda: None, "anything", "anything"),
        (lambda: None, "", "lambda"),
        (TestDummy.public_func, "anything", "anything"),
        (TestDummy.public_func, "", "public_func"),
        (TestDummy._hidden_func, "anything", "anything"),
        (TestDummy._hidden_func, "", "_hidden_func"),
        (TestDummy._TestDummy__private_func, "anything", "anything"),
        (TestDummy._TestDummy__private_func, "", "__private_func"))
    def test_supports_renaming_trait(self, func, given_name, expected_name):
        compiled = self.recompile(func, self.test_class, given_name)
        self.assertEqual(compiled.__name__, expected_name)


if __name__ == '__main__':
    unittest.main()
