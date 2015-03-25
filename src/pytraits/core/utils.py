def is_container(obj):
    """
    Checks whether the object is container or not.
    
    Container is considered an object, which includes other objects,
    thus string is not qualified, even it implments iterator protocol.

    >>> is_container("text")
    False

    >>> is_container(tuple())
    True
    """
    if isinstance(obj, str):
        return False
    
    return hasattr(obj, '__iter__')


def has_dict_protocol(obj):
    """ 
    Checks whether object supports dict protocol.
    """
    return hasattr(obj, "__getitem__") and hasattr(obj, "__setitem__")


def flatten(items):
    """
    Flatten the nested arrays into single one.

    Example about list of lists.
    >>> list(flatten([[1, 2], [3, 4]]))
    [1, 2, 3, 4]

    Example of deeply nested irregular list:
    >>> list(flatten([[[1, 2]], [[[3]]], 4, 5, [[6, [7, 8]]]]))
    [1, 2, 3, 4, 5, 6, 7, 8]

    List of strings is handled properly too
    >>> list(flatten(["one", "two", ["three", "four"]]))
    ['one', 'two', 'three', 'four']
    """
    for subitem in items:
        if is_container(subitem):
            for item in flatten(subitem):
                yield item 
        else:
            yield subitem

if __name__ == "__main__":
    import doctest
    doctest.testmod()