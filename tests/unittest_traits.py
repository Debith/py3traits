#!/usr/bin/python -tt
# -*- coding: utf-8 -*-
import unittest

from pytraits.core.errors import FirstTraitArgumentError, TraitArgumentTypeError
from pytraits.sources import Traits


class TestTraits(unittest.TestCase):
    def test_does_not_need_preprosessing_for_single_trait_object(self):
        traits = Traits(({}, ), {})
        self.assertFalse(traits.needs_preprocessing())

    def test_does_not_need_preprosessing_for_multiple_trait_objects(self):
        traits = Traits(({}, {}), {})
        self.assertFalse(traits.needs_preprocessing())

    def test_does_not_need_preprosessing_for_single_trait_function(self):
        traits = Traits((lambda: None, ), {})
        self.assertFalse(traits.needs_preprocessing())

    def test_does_not_need_preprosessing_for_multiple_trait_functions(self):
        traits = Traits((lambda: None, lambda: None), {})
        self.assertFalse(traits.needs_preprocessing())

    def test_does_not_need_preprosessing_for_multiple_trait_functions(self):
        traits = Traits((lambda: None, lambda: None), {})
        self.assertFalse(traits.needs_preprocessing())

    def test_raises_error_when_first_argument_is_string(self):
        traits = Traits(("", ""), {})
        with self.assertRaises(FirstTraitArgumentError):
            traits.needs_preprocessing()

    def test_raises_error_when_arguments_mixed_with_objects_and_strings(self):
        traits = Traits(({}, "", lambda: None), {})
        with self.assertRaises(TraitArgumentTypeError):
            traits.needs_preprocessing()

    def test_raises_error_when_arguments_mixed_with_function_and_strings(self):
        traits = Traits((lambda: None, "", ""), {})
        with self.assertRaises(FirstTraitArgumentError):
            traits.needs_preprocessing()

    def test_needs_preprosessing_when_object_and_strings_are_given(self):
        traits = Traits(({}, ""), {})
        self.assertTrue(traits.needs_preprocessing())

if __name__ == '__main__':
    unittest.main()
