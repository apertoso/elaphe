# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Codabar symbology.
"""
import string

from base import Symbology
from util.translation import charmap, MapTranslation
from util.checksum import upc_checksum


codabar_map = MapTranslation(
    charmap('0123456789-$:/.+ABCD'),
    extra_map=dict(zip(list('TN*E'), range(16,20)))).translate


# class Codabar(Symbology):
#     """
#     The Codabar symbology.

#     >>> s1 = Codabar('A1234567890B')
#     >>> s1.digits
#     [16, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 17]
#     >>> s1.start_char, s1.end_char
#     ('A', 'B')

#     """
#     def encode(self):
#         """Encodes data into Codabar digits.

#         Codabar consists of S...E, where S, E are
#         start, end, respectively.

#         """
#         self.start_char, self.end_char = None, None
#         if self._data:
#             if self._data[0] in 'ABCDTN*E':
#                 self.start_char = self._data[0] 
#             if self._data[-1] in 'ABCDTN*E':
#                 self.end_char = self._data[-1]
#         self.digits = list(codabar_map(self._data))

# # Codabar is known as NW-7 in Japan.
# NW_7=Codabar


if __name__=="__main__":
    from doctest import testmod
    testmod()

