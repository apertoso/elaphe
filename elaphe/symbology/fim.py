# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The facing identification mark (FIM)
"""
import string

from base import Symbology
from util.translation import charmap, MapTranslation


fim_map = MapTranslation(charmap('ABCD')).translate


class FIM(Symbology):
    """
    The facing identification mark.

    >>> s1 = FIM('A')
    >>> s1.digits
    [0]

    """
    def encode(self):
        """Encodes data into Codabar digits.

        Codabar consists of S...E, where S, E are
        start, end, respectively.

        """
        self.digits = list(fim_map(self._data))
# FIM is the abbreviation of Facing Identification Mark
FacingIdentificationMark=FIM


if __name__=="__main__":
    from doctest import testmod
    testmod()

