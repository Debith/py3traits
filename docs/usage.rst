Usage
=====

Composing traits
----------------

Combining classes
-----------------

Adding properties dynamically
-----------------------------

Properties can be very handy in some situations. Unfortunately, it is not
that straightforward to add new properties to instances, thus pytraits has
a small convenience function named `setproperty`. Using the function should
be as simple as possible as it is quite flexible with ways to use it.
Here is example of the simplest case::

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


There are more examples found in ``examples/property_is_created_into_instance.py``
