# -*- coding: utf-8 -*-


class MessageCodec(object):
    """Base class for message decoder.
    """
    def encode(self, ordinals, errors=None, **kwargs):
        return NotImplemented

    def decode(self, message, errors=None, **kwargs):
        return NotImplemented


class CharMapCodec(MessageCodec):
    """Codec for character-mapperd message system.

    >>> dc = CharMapCodec('0123456789+')
    >>> list(dc.decode('+123912')) # yields decoded list of ordinals
    [10, 1, 2, 3, 9, 1, 2]
    >>> list(dc.decode('+1X23912')) # chars out of map raises error on default
    Traceback (most recent call last):
    ...
    ValueError: Invalid character: X
    >>> list(dc.decode('+1X23912', 'ignore')) # errors='ignore' ignores error.
    [10, 1, 2, 3, 9, 1, 2]
    >>> ''.join(dc.encode([10, 1, 2, 3, 9, 1, 2]))
    '+123912'

    """
    def __init__(self, chars):
        self.chars = chars
        self.map = dict(t[::-1] for t in enumerate(chars))

    def decode(self, message, errors=None):
        for c in message:
            try:
                ordinal = self.map[c]
            except KeyError:
                if errors is 'ignore':
                    pass
                    continue
                else:
                    raise ValueError(u'Invalid character: %c' %(c))
            yield ordinal

    def encode(self, ordinals, errors=None, **kwargs):
        for i in ordinals:
            try:
                char = self.chars[i]
            except IndexError:
                if errors is ignore:
                    continue
            yield char


class Code128Codec(MessageCodec):
    """Converts a string into a sequence of code128 ordinals.

    >>> dc = Code128Codec()
    >>> list(dc.decode('^103AZ_^^_\\0\\1\\2'))
    [103, 33, 58, 63, 62, 63, 64, 65, 66]
    >>> list(dc.decode('^104AZ_^^_\\x60ab'))
    [104, 33, 58, 63, 62, 63, 64, 65, 66]
    >>> list(dc.decode('^105^102^'))
    [105, 102]
    >>> list(dc.decode('^105^X'))
    Traceback (most recent call last):
    ...
    ValueError: Invalid character in escape sequence: X
    >>> list(dc.decode('^105^X^102', 'ignore'))
    [105, 102]
    >>> list(dc.decode('^105^102123456^100A1'))
    [105, 102, 12, 34, 56, 100, 33, 17]
    >>> list(dc.decode('^105^102123456^100A1'))
    [105, 102, 12, 34, 56, 100, 33, 17]
    >>> ''.join(dc.encode([105, 102, 12, 34, 56, 100, 33, 17]))
    '^105^102123456^100A1'
    >>> ''.join(dc.encode([102, 12, 34, 56, 100, 33, 17]))
    Traceback (most recent call last):
    ...
    ValueError: Invalid ordinal sequence: 12
    >>> ''.join(dc.encode([102, 12, 34, 56, 100, 33, 17], errors='ignore'))
    '^102^100A1'
    >>> ''.join(dc.encode([102, 12, 34, 56, 100, 33, 17], code='A'))
    '^102,BX^100A1'

    """
    ASCII_7BITS = ''.join(chr(i) for i in range(128))
    CODE_A_TABLE = ASCII_7BITS[32:96] + ASCII_7BITS[:32]
    CODE_B_TABLE = ASCII_7BITS[32:128]

    def decode(self, message, errors=None):
        code = None
        escape = False
        carry = ''
        for c in message:
            try:
                if escape:
                    if c=='^':
                        escape, carry = False, ''
                        yield 62
                    elif c in '0123456789':
                        carry+=c
                        ordinal = int(carry, 10)
                        if ordinal in range(96, 108):
                            escape, carry = False, ''
                            if ordinal in (99, 105):
                                code = 'C'
                            if ordinal in (100, 104):
                                code = 'B'
                            elif ordinal in (101, 103):
                                code = 'A'
                            yield ordinal
                        if ordinal >=108:
                            raise ValueError(u'%d is not allowed for Code128' %ordinal)
                    else:
                        raise ValueError(u'Invalid character in escape sequence: %c' %(c))
                else:
                    if c=='^': # escape in
                        escape = True
                        carry = ''
                        continue
                    else:
                        if code == 'A':
                            ordinal = self.CODE_A_TABLE.index(c)
                        elif code == 'B':
                            ordinal = self.CODE_B_TABLE.index(c)
                        elif code == 'C':
                            if carry:
                                ordinal = int(carry+c, 10)
                                carry = ''
                            else:
                                carry = c
                                continue
                        else:
                            raise ValueError(u'Invalid character: %c' %code)
                        yield ordinal
            except ValueError:
                if errors is 'ignore':
                    escape, carry = False, ''
                    continue
                else:
                    raise
        if carry:
            raise ValueError(u'Unexpected end of codestring, residue=%s' %carry)

    def encode(self, ordinals, errors=None, code=None):
        encoders = {
            'A': lambda i: self.CODE_A_TABLE[i],
            'B': lambda i: self.CODE_A_TABLE[i],
            'C': lambda i: '%02d' %i }
        for i in ordinals:
            try:
                if i in range(96, 108):
                    if i in (99, 105):
                        code = 'C'
                    if i in (100, 104):
                        code = 'B'
                    elif i in (101, 103):
                        code = 'A'
                    yield '^%d' %i
                else:
                    yield encoders[code](i)
            except (ValueError, KeyError, IndexError):
                if errors is 'ignore':
                    continue
                else:
                    raise ValueError('Invalid ordinal sequence: %d' %(i))


if __name__=="__main__":
    from doctest import testmod
    testmod()
