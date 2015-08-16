Python Traits
=============

About Traits
------------

Traits are classes which contain methods that can be used to extend
other classes, similar to mixins, with exception that traits do not use
inheritance. Instead, traits are composed into other classes. That is;
methods, properties and internal state are copied to master object.

The point is to improve code reusability by dividing code into simple
building blocks that can be then combined into actual classes.

There is also a wikipedia article about Traits_.

Basics
------

In the simplest form, traits are very similar to any class, that is inherited
by some other class. That is a good way to approach traits in general; If you
can inherit some class, then you can also use it as a trait. Let's look an
example::

    .. code:: python
        from pytraits import extendable

        class Parent:
            def parent_function(self):
                return "Hello World"

        # Traditional inheritance
        class TraditionalChild(Parent):
            pass

        @extendable
        class ExceptionalChild:
            pass

        # Composing as trait
        ExceptionalChild.add_traits(Parent)

Places to use Traits
--------------------

To be effective with traits, one must have some knowledge about how to
write code that can be reused effectively through out the system. It also
helps to know something about good coding practices, for example:

    * `SOLID principles`_
    * `Law of Demeter`_

Especially in Law of Demeter, the interfaces tend to bloat because many small
and specific functions needs to be implemented for classes. Traits can help to
keep interfaces more manageable since one trait would contain methods only for
some specific situation.

Vertical and Horizontal program architecture
--------------------------------------------

Traits can really shine, when the application is layered both vertically and
horizontally. Vertical layer basically means different components of the system,
such as: `User`, `Address`, `Account`, `Wallet`, `Car`, `Computer`, etc.
Horinzontal layers would contain: `Security`, `Serialization`, `Rendering`, etc.
One approach with traits for above layering would be to create modules for
horizontal parts and then create trait for each type object needing that
behavior. Finally, in your main module, you would combine traits into classes.

Example:
    `core/account.py`

    .. code:: python

        from pytraits import extendable

        # Very simple address class
        @extendable
        class Address:
            def __init__(self, street, number):
                self.__street = street
                self.__number = number

    `core/wallet.py`

    .. code:: python

        from pytraits import extendable

        # Very simple wallet class
        @extendable
        class Wallet:
            def __init__(self, money=0):
                self.__money = money

    `horizontal/html_rendering.py`

    .. code:: python

        # This is a trait for address rendering
        class Address:
            def render(self):
                data = dict(street=self.__street, number=self.__number)
                return "<p>Address: {street} {number}</p>".format(**data)

        class Wallet:
            def render(self):
                # It is extremely straight-forward to render money situation.
                return "<p>Money: 0€</p>"

    `__main__.py`

    .. code:: python

        from core import Address, Wallet
        from horizontal import html_rendering

        Address.add_traits(html_rendering.Address)
        Wallet.add_traits(html_rendering.Wallet)

With this approach, if there becomes a need to support other rendering mechanisms
then just add new module and write rendering specific code there.

.. _Traits: http://en.wikipedia.org/wiki/Traits_class
.. _SOLID principles: https://en.wikipedia.org/wiki/SOLID_(object-oriented_design)
.. _Law of Demeter: https://en.wikipedia.org/wiki/Law_of_Demeter
