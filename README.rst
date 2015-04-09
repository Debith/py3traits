===============================
py3traits
===============================

| |docs| |travis| |appveyor| |coveralls| |landscape| |scrutinizer|
| |version| |downloads| |wheel| |supported-versions| |supported-implementations|

.. |docs| image:: https://readthedocs.org/projects/pytraits/badge/?style=flat
    :target: https://readthedocs.org/projects/pytraits
    :alt: Documentation Status

.. |travis| image:: http://img.shields.io/travis/Debith/pytraits/master.png?style=flat
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/Debith/pytraits

.. |appveyor| image:: https://ci.appveyor.com/api/projects/status/github/Debith/pytraits?branch=master
    :alt: AppVeyor Build Status
    :target: https://ci.appveyor.com/project/Debith/pytraits

.. |coveralls| image:: http://img.shields.io/coveralls/Debith/pytraits/master.png?style=flat
    :alt: Coverage Status
    :target: https://coveralls.io/r/Debith/pytraits

.. |landscape| image:: https://landscape.io/github/Debith/pytraits/master/landscape.svg?style=flat
    :target: https://landscape.io/github/Debith/pytraits/master
    :alt: Code Quality Status

.. |version| image:: http://img.shields.io/pypi/v/py3traits.png?style=flat
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/py3traits

.. |downloads| image:: http://img.shields.io/pypi/dm/py3traits.png?style=flat
    :alt: PyPI Package monthly downloads
    :target: https://pypi.python.org/pypi/py3traits

.. |wheel| image:: https://pypip.in/wheel/py3traits/badge.png?style=flat
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/py3traits

.. |supported-versions| image:: https://pypip.in/py_versions/py3traits/badge.png?style=flat
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/py3traits

.. |supported-implementations| image:: https://pypip.in/implementation/py3traits/badge.png?style=flat
    :alt: Supported imlementations
    :target: https://pypi.python.org/pypi/py3traits

.. |scrutinizer| image:: https://img.shields.io/scrutinizer/g/Debith/pytraits/master.png?style=flat
    :alt: Scrutinizer Status
    :target: https://scrutinizer-ci.com/g/Debith/pytraits/

Trait support for Python 3

* Free software: Apache license

Installation
============

::

    pip install py3traits

Documentation
=============

https://pytraits.readthedocs.org/

Development
===========

To run the all tests run::

    tox

About Traits
============

Traits are classes which contain methods that can be used to extend
other classes, similar to mixins, with exception that traits do not use
inheritance. Instead, traits are composed into other classes. That is;
methods, properties and internal state is copied to master object. 

The point is to improve code reusability by dividing code into simple 
building blocks that can be then combined into actual classes.

Read more from wikipedia: http://en.wikipedia.org/wiki/Traits_class

----------------------------------------------------------------

Features
========
 - Composition of Traits
    - [X] No conflicts
    - [X] Cherry-picking
    - [ ] Symmertric Sum
    - [ ] Override
    - [ ] Alias
    - [ ] Exclusion
 - Supported Trait Targets
    - [X] Classes
    - [X] Instances
 - Supported Trait Types
    - [X] Classes
    - [X] Instances
    - [X] Methods
    - [X] Functions
      - [X] as instance methods
      - [X] as classmethods
      - [X] as staticmethods
    - [X] Properties
 - Supported trait access level
      - [X] Private class attributes
      - [X] Hidden class attributes
      - [X] Public class attributes
      - [X] Private instance attributes
      - [X] Hidden instance attributes
      - [X] Public instance attributes
 - [X] Singleton


Composition of Traits
---------------------

Traits are classes that are not supposed to run stand alone (nothing stops to make them work
like that though). Traits are classes that are composed (by copying functions and properties)
into other classes. Advantage is that there is no inheritance happening and so there are no
typical problems occurring with normal inheritance. For instance, diamond inheritance is not
possible as everything is copied to target class and all conflicting methods and properties
needs to be resolved during composition.

In Python, this kind of approach is handy with metaclasses, since metaclasses have very strict
requirements for inheritance.

This library goes bit further than extending just classes. It's possible to also compose traits
into instances of classes, in which case, composition only affects single instance, not whole
class. Also, this library allows cherrypicking methods and properties from other classes and 
composing them to target objects. If anything, it at least enables possibility for highly 
creative ways to reuse your code.