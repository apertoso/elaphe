# coding: utf-8
"""Copyright (c) 2010 Yasushi Masuda. All rights reserved.
"""
from reportlab.lib import colors

class Symbology(object):
    """
    aAbstract base class for symbologies.

    >>> s = Symbology()
    >>> s # doctest: +ELLIPSIS
    <Symbology object at ...>
    >>> s.background_color==None
    True
    >>> s = Symbology(background_color=colors.black)
    >>> s.dpi, s.background_color
    (72.0, Color(0,0,0,1))

    """
    
    def __init__(self, dpi=72.0, background_color=None):
        """Constructor
        """
        self.dpi = dpi
        self.background_color=background_color

    def __repr__(self):
        return '<%s object at %x>' %(self.__class__.__name__, id(self))

    def generate(self, data, options):
        return NotImplemented


class LinearBarSymbology(Symbology):
    """
    >>> s = LinearBarSymbology()
    >>> s # doctest: +ELLIPSIS
    <LinearBarSymbology object at ...>
    >>> s.background_color, s.bar_height, s.bar_color
    (None, 1.0, Color(0,0,0,1))
    >>> s = LinearBarSymbology(bar_height=0.5, bar_color=colors.red)
    >>> s.background_color, s.bar_height, s.bar_color
    (None, 0.5, Color(1,0,0,1))

    """
    
    def __init__(self, bar_height=1.0, bar_color=colors.black, **kwargs):
        super(LinearBarSymbology, self).__init__(**kwargs)
        self.bar_height = bar_height
        self.bar_color = bar_color
    

if __name__=="__main__":
    from doctest import testmod
    testmod()
