#!/usr/bin/python -tt
# -*- coding: utf-8 -*-

from .base import TraitFactory
from .primitives.trait_object import TraitObject
import pytraits.core.composing  # NOQA

__all__ = ["TraitObject", "TraitFactory"]
