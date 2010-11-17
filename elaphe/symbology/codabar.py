# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Codabar symbology.
"""
import string

from base import Symbology
from util.translation import nw_7, nw7_tne
from util.checksum import upc_checksum


class Codabar(Symbology):
    """
    The Codabar symbology.

    >>> s1 = Codabar('A1234567890B')
    >>> s1.digits

    """
    def encode(self):
        """Encodes data into UPC digits.

        Codabar consists of S...E, where S, E are
        start, end, respectively.
        There are two types of codemap, which varies
        start/stop alphabets: (A, B, C, D) or (T, N, *, E).

        """
        translation = nw_7
        if any((c in self._data) for c in ['T', 'N', '*', 'E']):
            translation = nw_7_tne
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
