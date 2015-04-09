
Changelog
=========

0.10.0 (2014-01-01)
-----------------------------------------
  - Splitting into two projects: py2traits and py3traits
  - Taking new project template to use from cookiecutter.

0.9.0 Bringing back compatibility to Python 2.x
-----------------------------------------
  - Some small clean up too

0.8.0 Adding support to private class and instance attributes
-----------------------------------------
  - Redone function binding to include recompilation of the function
  - Leaving Python 2.x into unsupported state temporarily.

0.7.0 Improving usability of the library
-----------------------------------------
  - Introduced new extendable decorator, which adds function to add traits to object
  - Introduced new function combine_class to create new classes out of traits
  - Fixed module imports through out the library
  - Improved documentation in examples

0.6.0 Restructuring into library
-----------------------------------------
  - Added support for py.test
  - Preparing to support tox
  - Improved multiple examples and renamed them to make more sense
  - Removed the need of having two separate code branches for different Python versions

0.5.0 Instances can now be extended with traits in Python 3.x
-----------------------------------------
  - Instance support now similar to classes
  - Added more examples

0.4.0 Completed function binding with examples in Python 2.x
-----------------------------------------
  - Separate functions can now be bound to classes
    - Functions with 'self' as a first parameter will be acting as a method
    - Functions with 'cls' as a first parameter will be acting as classmethod
    - Other functions will be static methods.
  - Fixed an issue with binding functions

0.3.0 Trait extension support without conflicts for Python 2.x
-----------------------------------------
  - Classes can be extended
  - Instances can be extended
  - Python 2.x supported

0.2.0 Apache License Updated
-----------------------------------------
  - Added apache 2.0 license to all files
  - Set the character set as utf-8 for all files

0.1.0 Initial Version
-----------------------------------------
  - prepared files for Python 2.x
  - prepared files for Python 3.x