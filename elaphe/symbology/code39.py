# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights Reserved.
"""The Code39
"""
import string

from base import Symbology
from util.translation import charmap, Translation, TranslationError, MapTranslation
from util.checksum import modulus_43


code39_map = MapTranslation(
    charmap('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%*')).translate


class FullAsciiCode39Translation(Translation):
    """
    Translates full-ascii encoded code39 characters.
    
    >>> t = FullAsciiCode39Translation()
    >>> ordinals = list(t.translate('ABCD%A%B%C%D'))
    >>> ordinals, [chr(o) for o in ordinals]
    ([65, 66, 67, 68, 27, 28, 29, 30], ['A', 'B', 'C', 'D', '\\x1b', '\\x1c', '\\x1d', '\\x1e'])

    """
    CODE_GROUPS = (('%', 'U'),
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
    EXTRA_CODES = dict(('%'+c, 127) for c in 'XYZ')
    ENCODING_TABLE = dict(
        (code, ordinal)
        for ordinal, code in enumerate(
            reduce(list.__add__, ([p+c for c in s] 
                                  for p, s in CODE_GROUPS))))
    ENCODING_TABLE.update(EXTRA_CODES)

    def translate_chars(self, chars):
        """
        """
        if len(chars)>2:
            raise TranslationError
        else:
            return self.ENCODING_TABLE.get(''.join(chars), None)
full_ascii_code39_map=FullAsciiCode39Translation().translate


            

class Code39(Symbology):
    """
    The Code39 symbology.

    >>> s1 = Code39('ABC12345')
    >>> s1.digits
    [10, 11, 12, 1, 2, 3, 4, 5]
    >>> s1.checksum
    5

    """
    def encode(self):
        """Encodes data into ITF digits.
        """
        # always strip start/end character.
        self.digits = list(code39_map(self._data.strip('*')))
        self.checksum = modulus_43(self.digits)


class FullAsciiCode39(Code39):
    """
    """
    def encode(self):
        """Encodes (full-ascii encoded) data into ITF digits.
        """
        # always strip start/end character.
        self.digits = list(full_ascii_code39_map(self._data.strip('*')))
        self.checksum = modulus_43(self.digits)


if __name__=="__main__":
    from doctest import testmod
    testmod()
