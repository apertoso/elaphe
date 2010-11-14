# coding: utf-8
"""Copyright (c) 2010 Yasushi Masuda. All rights reserved.
"""


class Symbology(object):
    """
    aAbstract base class for symbologies.

    The DEFAULT_OPTIONS class attributes are used default value for
    ``options`` instance attribute. Subclass may override it.

    Example usage::
    
      # >>> s = SomeSymbology(foo_option=42, bar_option='baz')
      # >>> s.encode('spam eggs')
      # <some-data-strucute-representing-the-encoded-data>
    
    For convenience, giving "default encoder function" is encouraged:

      # >>> encode_somesymbology = SomeSymbology().encode
      # >>> encode_somesymbology('spam eggs')
      # <some-data-strucute-representing-the-encoded-data>

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
        self.data = data
        self.options = dict(self.DEFAULT_OPTIONS, **options)


