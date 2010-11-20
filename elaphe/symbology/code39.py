# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Code39
"""
import string

from base import Symbology
from util.translation import charmap, Translation, TranslationError, MapTranslation
from util.checksum import modulus_43


_code39_charmap = charmap('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%*')
code39_map = MapTranslation(_code39_charmap, skip_char='_').translate

def _code39_full_ascii_map():
    """Full ASCII map for Code39 extended encoding.

    >>> from pprint import pprint
    >>> pprint(_code39_full_ascii_map())
    """
    full_ascii_code_groups = (
        ('%', 'U'),
        ('$', string.ascii_uppercase),
        ('%', 'ABCDE'),
        ('', ' '),
        ('/', 'ABCDEFGHIJKL'),
        ('', '-.'),
        ('/', 'O'),
        ('', '0123456789'),
        ('/', 'Z'),
        ('%', 'FGHIJV'),
        ('', string.ascii_uppercase),
        ('%', 'KLMNOW'),
        ('+', string.ascii_uppercase),
        ('%', 'PQRST'))
    return map(lambda s: tuple(_code39_charmap[c] for c in s),
               reduce(list.__add__, 
                      ([p+c for c in s] 
                       for p, s in full_ascii_code_groups)))

code39_full_ascii_map = MapTranslation(
    charmap([chr(i) for i in range(128)],
            _code39_full_ascii_map())).translate
del _code39_charmap, _code39_full_ascii_map
   

class Code39(Symbology):
    """
    The Code39 symbology.

    >>> s1 = Code39('ABC123+/')
    >>> s1.digits
    [10, 11, 12, 1, 2, 3, 41, 40]
    >>> s1.checksum
    34
    >>> s2 = Code39('ABC123+/', code_map='full_ascii')
    >>> s2.digits
    [10, 11, 12, 1, 2, 3, 40, 20, 40, 24]

    """
    def __init__(self, data, code_map=None, **options):
        if code_map=='full_ascii':
            self.code_map = code39_full_ascii_map
        elif code_map in ['basic', None]:
            self.code_map = code39_map
        else:
            raise ValueError(u'Unsupported code map type.')
        super(Code39, self).__init__(data, **options)
                            
    def encode(self):
        """Encodes data into ITF digits.
        """
        # always strip start/end character.
        self.digits = list(self.code_map(self._data.strip('*')))
        self.checksum = modulus_43(self.digits)


if __name__=="__main__":
    from doctest import testmod
    testmod()
