# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights reserved.
"""The Code128 symbology.
"""
import string
from util.translation import Translation, TranslationError


class Code128Translation(Translation):
    """
    Converts message to code128 ordinals. Accepts cap('^')-escaped non-printables.

    >>> c128t = Code128Translation()
    >>> c128t # doctest: +ELLIPSIS
    <...Code128Translation object at ...>

    Escaped characters are processed successfully.
    >>> list(c128t.translate('^103AZ_^^_\\0\\1\\2', on_error=Translation.RAISE_ON_ERROR))
    [103, 33, 58, 63, 62, 63, 64, 65, 66]
    >>> list(c128t.translate('^104AZ_^^_\\x60ab', on_error=Translation.RAISE_ON_ERROR))
    [104, 33, 58, 63, 62, 63, 64, 65, 66]
    >>> list(c128t.translate('^105^102^', on_error=Translation.RAISE_ON_ERROR))
    [105, 102]
    >>> list(c128t.translate('^105^102123456^100A1', on_error=Translation.RAISE_ON_ERROR))
    [105, 102, 12, 34, 56, 100, 33, 17]
    >>> list(c128t.translate('^105^102123456^100A1', on_error=Translation.RAISE_ON_ERROR))
    [105, 102, 12, 34, 56, 100, 33, 17]

    Invalid character raises TranslationError (provided on_error is set).
    >>> list(c128t.translate('^105^X', on_error=Translation.RAISE_ON_ERROR))
    Traceback (most recent call last):
    ...
    TranslationError: ^X is not allowed for Code128 escape sequence.
    >>> list(c128t.translate('^105^X^102'))
    [105, 102]
    
    """
    ASCII_7BITS = ''.join(chr(i) for i in range(128))
    CODE_A_TABLE = ASCII_7BITS[32:96] + ASCII_7BITS[:32]
    CODE_B_TABLE = ASCII_7BITS[32:128]
    CODE_TABLES = dict(A=CODE_A_TABLE, B=CODE_B_TABLE)

    @staticmethod
    def cap_escape(s):
        """
        Converts string to cap-escaped printables.

        >>> cap_escape = Code128Translation.cap_escape
        >>> cap_escape('abcdef')
        'abcdef'
        >>> cap_escape('\\1\\2\\3\\10\\20\\30\\110\\120\\130\\200\\210\\220\\240')
        '^1^2^3^8^16^24HPX^128^136^144^160'

        """
        return ''.join(c if c in string.printable else '^'+str(ord(c))
                       for c in s)

    def __init__(self, **kwargs):
        super(Code128Translation, self).__init__(**kwargs)
        self.code = None

    def reset(self):
        """Resets internal code status.
        """
        self.code = None

    def translate_chars(self, chars):
        """
        Translates characters according to Code128 rules.

        The method employs internal mode stored in ``code`` instance attribute.
        
        >>> c128t = Code128Translation()
        >>> c128t.code # None
        >>> c128t.translate_chars(list('^')) # None
        >>> c128t.translate_chars(list('^^'))
        62

        # Shift code to A
        >>> c128t.translate_chars(list('^101'))
        101
        >>> c128t.code
        'A'
        >>> c128t.translate_chars(list('Z'))
        58

        # Shift code to B
        >>> c128t.translate_chars(list('^104'))
        104
        >>> c128t.code
        'B'

        # Shift code to C
        >>> c128t.translate_chars(list('^99'))
        99
        >>> c128t.code
        'C'

        """
        if chars[0]=='^':
            if len(chars)==1:
                # escape in
                return
            else:
                # escaped already
                if chars[1]=='^':
                    return 62
                else:
                    escaped = ''.join(chars[1:])
                    if escaped.isdigit():
                        ordinal = int(escaped, 10)
                        if ordinal<96:
                            return
                        elif ordinal in range(96, 108):
                            if ordinal in (99, 105):
                                self.code = 'C'
                            elif ordinal in (100, 104):
                                self.code = 'B'
                            elif ordinal in (101, 103):
                                self.code = 'A'
                            return ordinal
                        else: 
                            # ordinal larger than 108
                            pass
                    # ordinal larger than 108, or invalid escape sequence
                    raise TranslationError(
                        u'^%s is not allowed for Code128 escape sequence.' 
                        %(escaped))
        else:
            ordinal = None
            if self.code in ['A', 'B']:
                code_table = self.CODE_TABLES[self.code]
                try:
                    ordinal = code_table.index(chars[0])
                except IndexError:
                    raise TranslationError(
                        u'%(char)s is not in code table %(code)s'
                        %(dict(char=chars[0], code=self.code)))
            elif self.code == 'C':
                # requires two chars to continue
                if len(chars)==2:
                    ordinal = int(''.join(chars), 10)
                else:
                    return
            return ordinal
code128_map = Code128Translation().translate


if __name__=="__main__":
    from doctest import testmod
    testmod()

