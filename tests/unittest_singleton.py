#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest

from pytraits import Singleton
from pytraits.support.errors import SingletonError, SingletonInstanceError


class TestSingleton(unittest.TestCase):
    def test_there_can_only_be_one(self):
        class One(metaclass=Singleton):
            pass

        first = One()
        second = One()

        self.assertEqual(id(first), id(second))

    def test_second_initialization_with_arguments_are_ignored(self):
        class OneWithArgs(metaclass=Singleton):
            def __init__(self, one, two):
                self.one = one
                self.two = two

        this = OneWithArgs(1, 2)
        other = OneWithArgs(3, 4)

        self.assertEqual(this.one, 1)
        self.assertEqual(this.two, 2)
        self.assertEqual(other.one, 1)
        self.assertEqual(other.two, 2)
        self.assertEqual(id(this), id(other))

    def test_second_initialization_with_kwarguments_are_ignored(self):
        class OneWithKwArgs(metaclass=Singleton):
            def __init__(self, **kwargs):
                self.one = kwargs['one']
                self.two = kwargs['two']

        this = OneWithKwArgs(one=1, two=2)
        other = OneWithKwArgs(three=3, four=4)

        self.assertEqual(this.one, 1)
        self.assertEqual(this.two, 2)
        self.assertEqual(other.one, 1)
        self.assertEqual(other.two, 2)
        self.assertEqual(id(this), id(other))

    def test_enforces_immutability(self):
        class NoWrite(metaclass=Singleton):
            def __init__(self, begin):
                self.begin = begin

        no_write = NoWrite(3)
        with self.assertRaises(SingletonError):
            no_write.test = 5
        with self.assertRaises(SingletonError):
            no_write.begin = 1
        self.assertEqual(no_write.begin, 3)

if __name__ == '__main__':
    unittest.main()
