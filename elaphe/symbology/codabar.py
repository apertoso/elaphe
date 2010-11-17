# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Codabar symbology.
"""
import string

from base import Symbology
from util.translation import nw7, nw7_tne
from util.checksum import upc_checksum


class Codabar(Symbology):
    """
    The Codabar symbology.

    >>> s1 = Codabar('A1234567890B')
    >>> s1.digits
    [16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 17]

    """
    def encode(self):
        """Encodes data into Codabar digits.

        Codabar consists of S...E, where S, E are
        start, end, respectively.
        There are two types of codemap, which varies
        start/stop alphabets: (A, B, C, D) or (T, N, *, E).

        """
        translation = nw7
        if any((c in self._data) for c in ['T', 'N', '*', 'E']):
            translation = nw7_tne
        self.digits = list(translation(self._data))

    @property
    def label_type(self):
        """
        Returns label type of the code.

        Codabar uses different start/stop code pairs between label types
        as follows:
        
          +------+-------+-----+
          | Type | Start | End |
          +------+-------+-----+
          |  a   |   A   |  T  |
          |  b   |   B   |  N  |
          |  c   |   C   |  *  |
          |  d   |   D   |  E  |
          +------+-------+-----+

        """
        return {'A': 'a', 'B': 'b', 'C': 'c', 'D': 'd'}[self._data[0]]
# Codabar is known as NW-7 in Japan.
NW_7=Codabar


if __name__=="__main__":
    from doctest import testmod
    testmod()

