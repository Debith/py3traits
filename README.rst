===============================
py3traits
===============================

| |docs| |travis|

.. |docs| image:: https://readthedocs.org/projects/py3traits/badge/?style=flat
    :target: https://readthedocs.org/projects/py3traits
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/Debith/py3traits/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Debith/py3traits

Trait support for Python 3

* Free software: Apache license

Installation
============

::

    pip install py3traits

Documentation
=============

https://py3traits.readthedocs.org/

Development
===========

To run the all tests run::

    tox

About Traits
============

Traits are classes which contain methods that can be used to extend
other classes, similar to mixins, with exception that traits do not use
inheritance. Instead, traits are composed into other classes. That is;
methods, properties and internal state are copied to master object.

The point is to improve code reusability by dividing code into simple
building blocks that can be then combined into actual classes.

Read more from wikipedia: http://en.wikipedia.org/wiki/Traits_class

Look for examples from examples folder.
