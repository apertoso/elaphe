# coding: utf-8
import string

from base import Symbology
from util.translation import digits
from util.checksum import upc_checksum


class UPC(Symbology):
    """
    The Universal Product Code.

    >>> s1 = UPC('12345678901') # except checksum
    >>> s1.left_digits, s1.right_digits, s1.checksum
    ([1, 2, 3, 4, 5, 6], [7, 8, 9, 0, 1], 2)
    >>> s1.digits
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
    >>> s2 = UPC('01234567890') # except checksum
    >>> s2.digits
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 5]
    >>> s2.is_ndc
    False
    >>> s3 = UPC('30000000000')
    >>> s3.is_ndc
    True

    """
    def encode(self):
        """Encodes data into UPC digits.

        UPC consists of SLLLLLLMRRRRRCE, where S, M, E, R, L, C are
        start, middle, end, left, right, checksum.
        Checksum is 

        """
        ordinals = list(digits(self._data))
        if len(ordinals) in [11, 12]:
            self.left_digits = ordinals[:6]
            self.right_digits = ordinals[6:11]
            if ordinals[11:]: # with checksum
                self.checksum = ordinals[11]
            else:
                self.checksum = upc_checksum(ordinals[:11])
            self.digits = self.left_digits+self.right_digits+[self.checksum]
        else:
            raise ValueError

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
        

if __name__=="__main__":
    from doctest import testmod
    testmod()

