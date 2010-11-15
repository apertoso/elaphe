# coding: utf-8
"""Copyright (c) 2010 Yasushi Masuda. All rights reserved.
"""


class Symbology(object):
    """
    aAbstract base class for symbologies.

    The DEFAULT_OPTIONS class attributes are used default value for
    ``options`` instance attribute. Subclass may override it.

    Example usage::
    
      # >>> s = SomeSymbology('some data', foo_option=42, bar_option='baz')
      # >>> s.bits
      # (encoded data bits)
      # >>> s.checksum
      # (encoded checksum bits)

    """
    DEFAULT_OPTIONS = {}
    
    def __init__(self, data, **options):
        """
        Constructor.

        Takes arbitrary number of keyword arguments.
        All keyword arguments are passed to ``options`` instance
        attribute to update encoding options, those defaults to value
        described in DEFAULT_OPTIONS class attribute.

        """
        self._data = data
        self._options = dict(self.DEFAULT_OPTIONS, **options)
        self.encode()
        
    def get_data(self):
        return self._data

    def set_data(self, data):
        self._data = data
        self.encode()

    data = property(get_data, set_data)

    def get_options(self):
        return self._options

    def set_options(self, **options):
        self._options = options
        self.encode()

    options = property(get_options, set_options)

    def encode(self):
        """Do actual encoding work. Subclass should override.
        """


if __name__=="__main__":
    from doctest import testmod
    testmod()
