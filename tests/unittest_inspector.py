#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest
from collections import OrderedDict as odict

from pytraits.support.inspector import Inspector

from utils import for_examples
from testdata import *


class tdict(odict):
    def set(self, key, value):
        # Create a clone so that we don't mess up other tests.
        new_dict = tdict(self)
        new_dict[key] = value
        return new_dict


class TestInspector(unittest.TestCase):
    TESTS = tdict([
        (unittest, False),
        (MetaClass, False),
        (ExampleClass, False),
        (example_instance, False),
        (for_examples, False),
        (ExampleClass.test_method, False),
        (ExampleClass.test_property, False),
        (ExampleClass.TEST_ATTR_PUB, False),
        (ExampleClass.test_classmethod, False),
        (ExampleClass.test_staticmethod, False),
        (ExampleClass.__dict__["test_staticmethod"], False),
        (example_instance.test_method, False),
        (example_instance.TEST_ATTR_PUB, False),
        (example_instance.test_classmethod, False),
        (example_instance.test_staticmethod, False),
        (example_function, False),
        (int, False),
        (int.__add__, False),
        (type, False),
        (str, False),
        (1, False),
        ("test", False),
        (True, False),
        (None, False),
        (type(None), False),
        (map, False)])

    def setUp(self):
        self.inspector = Inspector()
        self.inspect = self.inspector.inspect

    @for_examples(
        (unittest, 'module'),
        (MetaClass, 'metaclass'),
        (ExampleClass, 'class'),
        (example_instance, 'instance'),
        (odict(), 'instance'),
        (for_examples, 'function'),
        (ExampleClass.test_method, 'function'),
        (ExampleClass.test_property, 'property'),
        (ExampleClass.TEST_ATTR_PUB, 'data'),
        (ExampleClass.test_classmethod, 'classmethod'),
        (ExampleClass.test_staticmethod, 'staticmethod'),
        (ExampleClass.__dict__["test_staticmethod"], 'staticmethod'),
        (example_instance.test_method, 'method'),
        (example_instance.TEST_ATTR_PUB, 'data'),
        (example_instance.test_classmethod, 'classmethod'),
        (example_instance.test_staticmethod, 'staticmethod'),
        (example_function, 'function'),
        (int, 'builtin'),
        (int.__add__, 'routine'),
        (type, 'builtin'),
        (str, 'builtin'),
        (1, 'data'),
        ("test", 'data'),
        (True, 'data'),
        (None, 'data'),
        (type(None), 'builtin'),
        (map, 'builtin'))
    def test_check_all_types_when_hooks_are_not_defined(self, object, typename):
        self.assertEqual(self.inspect(object), typename)

    @for_examples(*TESTS.set(example_instance, True).items())
    def test_isinstance_checks_identifies_types_properly(self, object, expected_result):
        self.assertEqual(self.inspector['instance'](object), expected_result)

    @for_examples(*TESTS.set(MetaClass, True).items())
    def test_ismetaclass_checks_identifies_types_properly(self, object, expected_result):
        self.assertEqual(self.inspector['metaclass'](object), expected_result)

    @for_examples(*TESTS.set(ExampleClass, True).items())
    def test_isclass_checks_identifies_types_properly(self, object, expected_result):
        self.assertEqual(self.inspector['class'](object), expected_result)

    @for_examples(*TESTS.set(ExampleClass.test_staticmethod, True)
                        .set(ExampleClass.__dict__["test_staticmethod"], True).items())
    def test_isclass_checks_identifies_types_properly(self, object, expected_result):
        self.assertEqual(self.inspector['staticmethod'](object), expected_result)

    def test_allows_promoting_type_checks(self):
        self.assertEqual(self.inspector.typenames[0], 'builtin')
        self.inspector.add_typecheck('data')
        self.assertEqual(self.inspector.typenames[0], 'data')
        self.assertEqual(self.inspector.inspect(2), 'data')

if __name__ == '__main__':
    unittest.main()
