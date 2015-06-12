#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest

from pytraits import type_converted
from pytraits.core.magic import TypeConversionError


class TestTypeConverted(unittest.TestCase):
    def test_shows_unassigned_arguments_error_for_omitted_arguments(self):
        # We need to make sure that when user misses argument from the
        # function call, we show proper error message.
        @type_converted
        def converted(existing, missing):
            pass

        with self.assertRaisesRegex(TypeError, ".*missing 1 required.*"):
            converted(True)

    def test_shows_unassigned_arguments_error_for_ommitted_arguments_with_type(self):
        # Even if argument has any arguments with annotated type, we still
        # need to give proper error message, when that argument has been
        # omitted.
        @type_converted
        def converted(existing, missing: int):
            pass

        with self.assertRaisesRegex(TypeError, ".*missing 1 required.*"):
            converted(True)

    def test_uses_default_value_for_omitted_arguments(self):
        # Missing arguments with default values should be properly used when
        # arguments are omitted.
        @type_converted
        def converted(existing, missing_with_default=42):
            return missing_with_default

        self.assertEqual(converted(True), 42)

    def test_uses_default_value_for_omitted_arguments_with_type(self):
        # Missing arguments with default values should be properly used when
        # arguments are omitted even when there are annotated arguments.
        @type_converted
        def converted(existing, missing_with_default: int=42):
            return missing_with_default

        self.assertEqual(converted(True), 42)

    def test_ignores_default_value_when_argument_given_with_type(self):
        # Missing arguments with default values should be properly used when
        # arguments are omitted even when there are annotated arguments.
        @type_converted
        def converted(existing, missing_with_default: int=42):
            return missing_with_default

        self.assertEqual(converted(True, "52"), 52)

    def test_handles_properly_tuple_arguments(self):
        @type_converted
        def converted(existing, *remainder):
            return existing

        self.assertEqual(converted(True), True)

    def test_handles_properly_tuple_arguments_with_type(self):
        @type_converted
        def converted(existing: bool, *remainder):
            return existing

        self.assertEqual(converted(True), True)

    def test_handles_properly_tuple_arguments_with_type(self):
        @type_converted
        def converted(existing: bool, *remainder):
            return existing

        with self.assertRaisesRegex(TypeConversionError, "While calling.*"):
            converted(2, "tuple", "args")

    def test_shows_proper_error_when_too_many_args_given(self):
        @type_converted
        def converted(existing):
            return missing_with_default

        with self.assertRaisesRegex(TypeError, ".*takes 1 positional.*"):
            self.assertEqual(converted(True, 52), 52)

    def test_shows_proper_error_when_too_many_args_given_with_type(self):
        @type_converted
        def converted(existing: bool):
            return missing_with_default

        with self.assertRaisesRegex(TypeError, ".*takes 1 positional.*"):
            self.assertEqual(converted(True, 52), 52)

    def test_shows_proper_error_when_too_many_args_given_with_default(self):
        @type_converted
        def converted(existing=False):
            return missing_with_default

        with self.assertRaisesRegex(TypeError, ".*takes from 0 to 1 positional.*"):
            self.assertEqual(converted(True, 52), 52)

    def test_shows_proper_error_when_too_many_args_given_with_type_and_default(self):
        @type_converted
        def converted(existing: bool=False):
            return missing_with_default

        with self.assertRaisesRegex(TypeError, ".*takes from 0 to 1 positional.*"):
            self.assertEqual(converted(True, 52), 52)

if __name__ == '__main__':
    unittest.main()
