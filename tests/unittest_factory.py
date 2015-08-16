#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest

from pytraits import Factory
from pytraits.support.errors import (FactoryError,
                                     FactoryRegisterError,
                                     FactoryClassMissingError)

from utils import for_examples


class TestFactory1(Factory):
    pass


class TestFactory2(Factory):
    pass


class TestFactory(unittest.TestCase):
    def setUp(self):
        @TestFactory1.register
        class TestClass1:
            pass

        @TestFactory2.register
        class TestClass2:
            pass

    def tearDown(self):
        TestFactory1.reset()
        TestFactory2.reset()

    def test_inherited_factories_are_own_instances(self):
        self.assertEqual(TestFactory1().registered_classes, ['TestClass1'])
        self.assertEqual(TestFactory2().registered_classes, ['TestClass2'])

    def test_can_create_instances_of_classes_with_create_classmethod(self):
        @TestFactory1.register
        class TestClass3:
            def __init__(self, test_value=None):
                self.test_value = test_value

            @classmethod
            def create(cls, init_value):
                return cls(init_value)

        instance = TestFactory1["TestClass3"](5)
        self.assertEqual(instance.test_value, 5)

    def test_classes_with_call_method_are_initialized(self):
        @TestFactory2.register
        class TestClass4:
            def __init__(self, test_value="default"):
                self.test_value = test_value

            def __call__(self, argument):
                return str(argument)

        sub_factory = TestFactory2["TestClass4"]
        answer_to_everything = sub_factory(42)
        self.assertEqual(sub_factory.test_value, "default")
        self.assertEqual(answer_to_everything, '42')

    def test_classes_with_call_and_create_method_are_properly(self):
        @TestFactory2.register
        class TestClass5:
            def __init__(self, test_value="default"):
                self.test_value = test_value

            @classmethod
            def create(cls):
                return cls("modified")

            def __call__(self, argument):
                return str(argument)

        sub_factory = TestFactory2["TestClass5"]
        answer_to_everything = sub_factory(100)
        self.assertEqual(sub_factory.test_value, "modified")
        self.assertEqual(answer_to_everything, '100')

    def test_complains_when_registered_class_exists_in_factory(self):
        @TestFactory2.register
        class TestClass4:
            pass

        with self.assertRaises(FactoryRegisterError):
            @TestFactory2.register
            class TestClass4:
                pass

    def test_factory_is_abstract(self):
        with self.assertRaises(FactoryError):
            Factory()

    def test_complains_when_class_missing_factory(self):
        with self.assertRaisesRegex(FactoryClassMissingError, 'is not in registered'):
            TestFactory1()["MissingClass"]

    def test_can_register_multiple_classes_in_single_call(self):
        TestClass3 = type('TestClass3', (), {})
        TestClass4 = type('TestClass4', (), {})
        TestFactory1.register(TestClass3, TestClass4)
        self.assertIn('TestClass3', TestFactory1().registered_classes)
        self.assertIn('TestClass4', TestFactory1().registered_classes)

    def test_knows_when_class_is_registered(self):
        TestClass5 = type('TestClass5', (), {})
        self.assertFalse(TestFactory1().exists(TestClass5))
        TestFactory1.register(TestClass5)
        self.assertTrue(TestFactory1().exists(TestClass5))

    def test_register_works_as_decorator(self):
        TestClass6 = type('TestClass6', (), {})
        clazz = TestFactory1.register(TestClass6)
        self.assertEqual(TestClass6, clazz)

    def test_registering_multiple_classes_returns_nothing(self):
        TestClass7 = type('TestClass7', (), {})
        TestClass8 = type('TestClass8', (), {})
        clazz = TestFactory1.register(TestClass7, TestClass8)
        self.assertEqual(None, clazz)

if __name__ == '__main__':
    unittest.main()
