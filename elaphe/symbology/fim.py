# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The facing identification mark (FIM)
"""
import string

from reportlab.graphics import shapes
from reportlab.lib import colors

from base import LinearBarSymbology


class FIM(LinearBarSymbology):
    """
    Face Identification Marker (FIM).

    >>> s = FIM()
    >>> s                    # doctest: +ELLIPSIS
    <FIM object at ...>
    >>> s.generate('a')      # doctest: +ELLIPSIS
    <reportlab.graphics.shapes.Group instance at ...>
    
    """

    fim_bits = { 'a': [1, 1, 0, 0, 1, 0, 0, 1, 1], 
                 'b': [1, 0, 1, 1, 0, 1, 1, 0, 1],
                 'c': [1, 1, 0, 1, 0, 1, 0, 1, 1],
                 'd': [1, 1, 1, 0, 1, 0, 1, 1, 1] }


    def __init__(self, bar_bottom=0, bar_height=5/8.0, **kwargs):
        super(FIM, self).__init__(bar_height=bar_height, **kwargs)
        self.bar_bottom = 0.0
        self.bar_width = 1/32.0
        self.bar_gap = 2.25/32.0
        self._prepare()

    def _prepare(self):
        bar_attrs = dict(strokeColor=None, strokeWidth=0,
                         fillColor=self.bar_color)
        dpi = self.dpi
        self.cache = {}
        for char, bits in self.fim_bits.items():
            group = shapes.Group()
            for i, bit in enumerate(bits):
                if bit==1:
                    bar = shapes.Rect(i*self.bar_gap*dpi,
                                      self.bar_bottom*dpi,
                                      self.bar_width*dpi,
                                      self.bar_height*dpi,
                                      **bar_attrs)
                    group.add(bar)
            self.cache[char] = group

    def generate(self, data):
        return self.cache[data]


# FIM is the abbreviation of Facing Identification Mark
FacingIdentificationMark=FIM


if __name__=="__main__":
    from doctest import testmod
    testmod()

