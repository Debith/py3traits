#!/usr/bin/python -tt
# -*- coding: utf-8 -*-


class MetaClass(type):
    def __init__(self):
        pass


class ExampleClass:
    TEST_ATTR_PUB = "public"

    def __init__(self):
        self.test_attr_pub = "public"

    @property
    def test_property(self):
        pass

    def test_method(self):
        pass

    @classmethod
    def test_classmethod(cls):
        pass

    @staticmethod
    def test_staticmethod():
        pass

example_instance = ExampleClass()


def example_function():
    pass


def example_function_self(self):
    pass


def example_function_cls(cls):
    pass
