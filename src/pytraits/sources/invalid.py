class InvalidSource(object):
    """
    Null context for invalid cases.
    """
    BINDER_ID = 'null'
    VALID = False
    
    def __init__(self, extra_message):
        print("PyTraits: InvalidContext:", extra_message)
        self._extra_message = extra_message

    @property
    def error_message(self):
        return self._extra_message