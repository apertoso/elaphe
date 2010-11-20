# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Code93
"""
import string

from base import Symbology
from util.translation import charmap, Translation, TranslationError, MapTranslation
from util.checksum import modulus_43


# charmap except start/stop and control chars
_code93_charmap = charmap('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%')
code93_map = MapTranslation(_code93_charmap).translate

def _code93_full_ascii_map():
    """Full ASCII map for Code39 extended encoding.

    >>> _code93_full_ascii_map() # doctest: +ELLIPSIS
    [(44, 30), (43, 10), ... (45, 21), 36, 37, (45, 24), 0, 1, 2, ... (44, 29)]

    """
    full_ascii_code_groups = (
        (44, 'U'),
        (43, string.ascii_uppercase),
        (44, 'ABCDE'),
        (None, ' '),
        (45, 'ABCDEFGHIJKL'),
        (None, '-.'),
        (45, 'O'),
        (None, '0123456789'),
        (45, 'Z'),
        (44, 'FGHIJV'),
        (None, string.ascii_uppercase),
        (44, 'KLMNOW'),
        (46, string.ascii_uppercase),
        (44, 'PQRST'))
    return reduce(list.__add__, 
                  (([(escape, _code93_charmap[c]) for c in chars] if escape
                   else [_code93_charmap[c] for c in chars])
                   for escape, chars in full_ascii_code_groups))

code93_full_ascii_map = MapTranslation(
    charmap([chr(i) for i in range(128)],
            _code93_full_ascii_map())).translate
# del _code93_charmap, _code93_full_ascii_map
   

class Code93(Symbology):
    """
    The Code93 symbology.

    >>> s1 = Code93('ABC123+/')
    >>> s1.digits
    [10, 11, 12, 1, 2, 3, 41, 40]
    >>> s1.checksum
    34
    >>> s2 = Code93('ABC123+/', code_map='full_ascii')
    >>> s2.digits
    [10, 11, 12, 1, 2, 3, 45, 20, 45, 24]

    """
    def __init__(self, data, code_map=None, **options):
        if code_map=='full_ascii':
            self.code_map = code93_full_ascii_map
        elif code_map in ['basic', None]:
            self.code_map = code93_map
        else:
            raise ValueError(u'Unsupported code map type.')
        super(Code93, self).__init__(data, **options)
                            
    def encode(self):
        """Encodes data into ITF digits.
        """
        # always strip start/end character.
        self.digits = list(self.code_map(self._data.strip('*')))
        self.checksum = modulus_43(self.digits)


if __name__=="__main__":
    from doctest import testmod
    testmod()
