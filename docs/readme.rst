# Python Traits

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

Using Traits
------------

To be effective with traits, one must have some knowledge about how to
write code that can be reused effectively through out the system. It also
helps to know something about good coding practices, for example:
    * [SOLID principles](https://en.wikipedia.org/wiki/SOLID_(object-oriented_design))
    * [Law of Demeter](https://en.wikipedia.org/wiki/Law_of_Demeter)

Especially in Law of Demeter, the interfaces tend to bloat because many small
and specific functions needs to be implemented for classes. Traits can help to
keep interfaces more manageable since one trait would contain methods only for
some specific situation.

Vertical and Horizontal program architecture
--------------------------------------------

Traits can really shine, when the application is layered both vertically and
horizontally. Vertical layer basically means different components of the system,
such as: User, Address, Account, Wallet, Car, Computer, etc.
Horinzontal layers would contain: Security, Serialization, Rendering, etc.
One approach with traits for above layering would be to create modules for
horizontal parts and then create trait for each type object needing that
behavior. Finally, in your main module, you would combine traits into classes.

Example:
    `core/account.py`
    ``
        from pytraits import extendable

        # Very simple address class
        @extendable
        class Address:
            def __init__(self, street, number):
                self.__street = street
                self.__number = number
    ``

    `core/wallet.py`
    ``
        from pytraits import extendable

        # Very simple wallet class
        @extendable
        class Wallet:
            def __init__(self, money=0):
                self.__money = money
    ``

    `horizontal/html_rendering.py`
    ``
        # This is a trait for address rendering
        class Address:
            def render(self):
                data = dict(street=self.__street, number=self.__number)
                return "<p>Address: {street} {number}</p>".format(**data)

        class Wallet:
            def render(self):
                # It is extremely straight-forward to render money situation.
                return "<p>Money: 0€</p>"
    ``

    `__main__.py`
    ``
        from core import Address, Wallet
        from horizontal import html_rendering

        Address.add_traits(html_rendering.Address)
        Wallet.add_traits(html_rendering.Wallet)
    ``

With this approach, if there becomes a need to support other rendering mechanisms
then just add new module and write rendering specific code there.

Features in pytraits
--------------------

### Composing traits

### Combining classes

### Adding properties dynamically

Properties can be very handy in some situations. Unfortunately, it is not
that straightforward to add new properties to instances, thus pytraits has
a small convenience function named ``setproperty`` which can be accessed by
importing ``from pytraits import setproperty``.

Using the function should be as simple as possible as it is quite flexible
with ways to use it. Here is example of the simplest case:
``
    from pytraits import setproperty

    class Account:
        def __init__(self, money):
            self.__money = money

        def money(self):
            return self.__money

        def set_money(self, new_money):
            self.__money = new_money

    my_account = Account(0)
    setproperty(my_account, "money", "set_money")
``

There are more examples found in ``examples/property_is_created_into_instance.py``
