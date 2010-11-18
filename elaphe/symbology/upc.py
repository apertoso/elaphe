# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""Universal Product Code, UPC-A and Zero-compressed UPC (UPC-E).
"""
import string

from base import Symbology
from util.translation import digits
from util.checksum import upc_checksum


class UPC_A(Symbology):
    """
    The Universal Product Code, UPC-A.

    >>> s1 = UPC_A('12345678901') # except checksum
    >>> s1.left_digits, s1.right_digits, s1.checksum
    ([1, 2, 3, 4, 5, 6], [7, 8, 9, 0, 1], 2)
    >>> s1.digits, s1.checksum
    ([1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1], 2)
    >>> s2 = UPC_A('01234567890') # except checksum
    >>> s2.digits, s2.checksum
    ([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0], 5)
    >>> s2.is_ndc
    False
    >>> s3 = UPC_A('30000000000')
    >>> s3.is_ndc
    True

    """
    def encode(self):
        """Encodes data into UPC digits.

        UPC consists of SLLLLLLMRRRRRCE, where S, M, E, R, L, C are
        start, middle, end, left, right and checksum respectively.

        """
        ordinals = list(digits(self._data))
        if len(ordinals) in [11, 12]:
            self.left_digits = ordinals[:6]
            self.right_digits = ordinals[6:11]
            if ordinals[11:]: # with checksum
                self.checksum = ordinals[11]
            else:
                self.checksum = upc_checksum(ordinals[:11])
        else:
            raise ValueError

    @property
    def digits(self):
        return self.left_digits+self.right_digits

    def is_prefixed(self, *prefixes):
        """Returns True if code uses any of given prefixes.
        """
        return self.left_digits[0] in prefixes

    @property
    def is_local(self):
        """Returns True if code uses prefix reserved for local use.
        """
        return self.is_prefixed(2, 4)

    @property
    def is_ndc(self):
        """Returns True if code uses prefix for NDC number.
        """
        return self.is_prefixed(3)

    @property
    def is_coupon(self):
        """Returns True if code uses prefix reserved for coupons.
        """
        return self.is_prefixed(5, 9)
# Generally, UPC represents UPC_A
UPC = UPC_A


class UPC_E(Symbology):
    """Zero-compressed UPC.

    >>> s1 = UPC_E('654321')
    >>> s1.upc_a_equivalent
    [0, 6, 5, 1, 0, 0, 0, 0, 4, 3, 2, 7]
    >>> s1.parities
    'EOEOEO'
    """
    PARITY_PATTERNS = {
        0: 'EEEOOO', 1: 'EEOEOO', 2: 'EEOOEO', 3: 'EEOOOE', 4: 'EOEEOO',
        5: 'EOOEEO', 6: 'EOOOEE', 7: 'EOEOEO', 8: 'EOEOOE', 9: 'EOOEOE',
        }
    
    UPC_A_FORMATS = {
        0: (lambda o: [0, o[0], o[1], 0, 0, 0, 0, 0, o[2], o[3], o[4]]),
        1: (lambda o: [0, o[0], o[1], 1, 0, 0, 0, 0, o[2], o[3], o[4]]),
        2: (lambda o: [0, o[0], o[1], 2, 0, 0, 0, 0, o[2], o[3], o[4]]),
        3: (lambda o: [0, o[0], o[1], o[2], 0, 0, 0, 0, 0, o[3], o[4]]),
        4: (lambda o: [0, o[0], o[1], o[2], o[3], 0, 0, 0, 0, 0, o[4]]),
        5: (lambda o: [0, o[0], o[1], o[2], o[3], o[4], 0, 0, 0, 0, 5]),
        6: (lambda o: [0, o[0], o[1], o[2], o[3], o[4], 0, 0, 0, 0, 6]),
        7: (lambda o: [0, o[0], o[1], o[2], o[3], o[4], 0, 0, 0, 0, 7]),
        8: (lambda o: [0, o[0], o[1], o[2], o[3], o[4], 0, 0, 0, 0, 8]),
        9: (lambda o: [0, o[0], o[1], o[2], o[3], o[4], 0, 0, 0, 0, 9]),
        }

    def encode(self):
        """Encodes data into UPC-E digits.

        UPC-E should have data of 6 digits. It can be converted
        to UPC-A using following scheme:
        Given UPC-E digits DDDDDX where D and X are [0-9],
        last digits concerns format of UPC-A equivalent as follows:

          +-----+--------+------------+-------------+
          |  X  | UPC-E  | UPC-A left | UPC-A right |
          +-----+--------+------------+-------------+
          |  0  | MMPPP0 |   0MM000   |    00PPPC   |
          |  1  | MMPPP1 |   0MM100   |    00PPPC   |
          |  2  | MMPPP2 |   0MM200   |    00PPPC   |
          |  3  | MMMPP3 |   0MMM00   |    000PPC   |
          |  4  | MMMMP4 |   0MMMM0   |    0000PC   |
          | 5-9 | MMPPPX |   0MMPPP   |    0000XC   |
          +-----+--------+------------+-------------+

        The encoded UPC-E does not include checkdigit.
        Instead, code parities are used for data collection.
        
        Code parities are determined by UPC-A checkdigit C as follows:

          +---+--------+---+--------+---+--------+
          | C | Parity | C | Parity | C | Parity |
          +---+--------+---+--------+---+--------+
          | 0 | EEEOOO | 1 | EEOEOO | 2 | EEOOEO |
          | 3 | EEOOOE | 4 | EOEEOO | 5 | EOOEEO |
          | 6 | EOOOEE | 7 | EOEOEO | 8 | EOEOOE |
          | 9 | EOOEOE +---+--------+---+--------+
          +---+--------+

        Where E, O indicate Even, Odd, respectively.

        """
        ordinals = list(digits(self._data))
        if len(ordinals)==6:
            self.digits = ordinals
            upc_a = self.upc_a_equivalent
            self.parities = self.PARITY_PATTERNS[upc_a[-1]]
        else:
            raise ValueError

    @property
    def upc_a_equivalent(self):
        """Returns UPC-A equivalent.

        >>> UPC_E('654321').upc_a_equivalent
        [0, 6, 5, 1, 0, 0, 0, 0, 4, 3, 2, 7]

        """
        upc_a_ordinals = self.UPC_A_FORMATS[self.digits[-1]](self.digits)
        checksum = upc_checksum(upc_a_ordinals)
        return upc_a_ordinals + [checksum]


if __name__=="__main__":
    from doctest import testmod
    testmod()

