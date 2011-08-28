# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Interleaved 2 of 5.
"""
import string

from base import Symbology
from util.translation import digits
from util.checksum import modulus_10_w3


# class ITF(Symbology):
#     """
#     The Interleaved 2 of 5 symbology.

#     >>> s1 = ITF('12345')
#     >>> s1.digits
#     [1, 2, 3, 4, 5]
#     >>> s1.checksum
#     7

#     """
#     def encode(self):
#         """Encodes data into ITF digits.
#         """
#         self.digits = list(digits(self._data))
#         self.checksum = modulus_10_w3(self.digits)


if __name__=="__main__":
    from doctest import testmod
    testmod()
