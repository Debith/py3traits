#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest

from pytraits.support.errors import FirstTraitArgumentError, TraitArgumentTypeError
from pytraits.support import flatten
from pytraits.core import TraitFactory

from testdata import *


inspect = TraitFactory["TraitTargetInspector"]


class TestClassObject(unittest.TestCase):
    def setUp(self):
        self.classtype = inspect(ExampleClass)
        self.dir = dir(self.classtype)
        self.items = dict(self.classtype.items())

    def __getitem__(self, key):
        return self.items[key]

    def typename(self, key):
        return type(self[key]).__name__

    @property
    def iterated(self):
        return list(self.classtype)

    def test_has_a_custom_dir(self):
        self.assertEqual(self.dir,
                         ['TEST_ATTR_PUB', 'test_classmethod', 'test_method',
                          'test_property', 'test_staticmethod'])

    def test_supports_showing_items(self):
        self.assertEqual(self.typename("TEST_ATTR_PUB"), "str")
        self.assertEqual(self.typename("test_classmethod"), "classmethod")
        self.assertEqual(self.typename("test_method"), "function")
        self.assertEqual(self.typename("test_property"), "property")
        self.assertEqual(self.typename("test_staticmethod"), "staticmethod")

    def test_supports_iteration(self):
        iterated = sorted([str(f) for f in self.iterated])
        self.assertEqual(iterated[0], "classmethod")
        self.assertEqual(iterated[1], "method")
        self.assertEqual(iterated[2], "property")
        self.assertEqual(iterated[3], "staticmethod")

    def test_can_be_flattened(self):
        flat = flatten(self.classtype)
        self.assertEqual(sorted([str(f) for f in list(flat)]),
                         ['classmethod', 'method', 'property', 'staticmethod'])

if __name__ == '__main__':
    unittest.main()
