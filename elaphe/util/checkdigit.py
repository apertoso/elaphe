# -*- coding: utf-8 -*-
"""Various checkdigits.
"""
import string
from codec import CharMapCodec, Code128Codec


def charmap(chars):
    """
    >>> charmap('ABC')
    ({'A': 0, 'C': 2, 'B': 1}, {0: 'A', 1: 'B', 2: 'C'})
    """
    forward_map = dict(t[::-1] for t in enumerate(chars)) # char to int
    reverse_map = dict(t for t in enumerate(chars)) # int to char
    return forward_map, reverse_map


def modcomp(b, n):
    """Computes complemented modulus (b, n).

    >>> (modcomp(1, 1), modcomp(1, 2), modcomp(1, 3)), (modcomp(2, 1), modcomp(2, 2), modcomp(2, 3))
    ((0, 0, 0), (1, 0, 1))
    """
    return (b-n%b)%b


class CheckDigit(object):
    """Base class for checkdigit systems.
    """
    def __init__(self, *args, **kwargs):
        self.message_codec = getattr(self, 'MESSAGE_CODEC', self.get_message_codec())

    def get_message_codec(self):
        return NotImplemented

    def normalize_message(self, message):
        return message

    def compute(self, ordinals, **kwargs):
        raise NotImplemented

    def as_ordinal(self, message, errors=None, **kwargs):
        return self.compute(self.message_codec.decode(self.normalize_message(message), errors, **kwargs))

    def as_char(self, message, errors=None, **kwargs):
        return ''.join(self.message_codec.encode([self.as_ordinal(message, errors, **kwargs)]))


class Modulus43(CheckDigit):
    """Modulus-43, used in Code39.

    >>> Modulus43().as_ordinal('ABCD1234+')
    11
    >>> Modulus43().as_char('B')
    'B'

    """
    MESSAGE_CODEC = CharMapCodec(string.digits+string.ascii_uppercase+'-. $/+%')

    def nomalize_message(self, message):
        return (c.upper() for c in message)

    def compute(self, ordinals, **kwargs):
        return sum(ordinals)%43

modulus_43 = Modulus43().as_char


class NumericOnlyCheckDigit(CheckDigit):
    MESSAGE_CODEC = CharMapCodec(string.digits)


class Modulus10W3(NumericOnlyCheckDigit):
    """Modulus 10, weighted with 3. Used in JAN ITF and NW-7.
    
    >>> Modulus10W3().as_char('490123456789')
    '4'

    """
    def compute(self, ordinals, **kwargs):
        return modcomp(10, sum(ordinal*(1+2*(i%2)) for i, ordinal in enumerate(ordinals)))

modulus_10_w3 = Modulus10W3().as_char


class Modulus16(CheckDigit):
    """Modulus 16, used in NW-7. Argument should include start/stop/checkdigit.
    
    >>> Modulus16().as_char('A19+1243*B')
    ':'

    """
    MESSAGE_CODEC = CharMapCodec(string.digits+'-$:/.+ABCD')

    def normalize_message(self, message):
        list_chars = list(message)
        return (c.upper() for i, c in enumerate(list_chars) if i!=len(list_chars)-2)

    def compute(self, ordinals, **kwargs):
        return modcomp(16, sum(ordinals))

modulus_16 = Modulus16().as_char


class Modulus11(NumericOnlyCheckDigit):
    """Modulus 11, used in NW-7. Argucment should exclude start/stop.
    
    >>> Modulus11().as_char('2431245*')
    '6'

    """
    def normalize_message(self, message):
        return message[:6]

    def compute(self, ordinals, **kwargs):
        return modcomp(11, sum(ordinal*(7-i) for i, ordinal in enumerate(ordinals)))

modulus_11 = Modulus11().as_char


class Modulus10w2(NumericOnlyCheckDigit):
    """Modulus 10, weighted with 2. Used in NW-7. Argument should exclude start/stop/checkdigit.

    >>> modulus_10_w2('938745343')
    '7'

    """
    def compute(self, ordinals, **kwargs):
        return modcomp(10, sum(ordinal*(2-(i%2)) for i, ordinal in enumerate(ordinals)))

modulus_10_w2 = Modulus10w2().as_char


class CheckDR7(NumericOnlyCheckDigit):
    """7-check DR checkdigit, used in NW-7. Argument should exclude start/stop/checkdigit.

    >>> check_DR_7('8745343')
    '5'

    """
    def as_ordinal(self, message, errors=None, **kwargs):
        return int(''.join(message), 10)%7

    def as_char(self, message, errors=None, **kwargs):
        return ''.join(self.message_codec.encode([self.as_ordinal(message, errors, **kwargs)]))

check_DR_7 = CheckDR7().as_char


class WeightedModulus11(NumericOnlyCheckDigit):
    """Weighted modulus 11, used in NW-7. Argument should exclude start/stop.

    >>> weighted_modulus_11('5012924346')
    '4'
    >>> weighted_modulus_11('0200290068')
    '1'

    """
    WEIGHT_1 = [6, 3, 5, 9, 10, 7, 8, 4, 5, 3, 6, 2]
    WEIGHT_2 =  [5, 8, 6, 2, 10, 4, 3, 7, 6, 8, 5, 9]

    def compute(self, ordinals, **kwargs):
        olist = list(ordinals)
        mod = sum(ordinal*self.WEIGHT_1[-1-i] for i, ordinal in enumerate(olist[::-1]))%11
        if mod==0:
            return 0
        elif mod==1:
            return modcomp(11, sum(ordinal*self.WEIGHT_2[-1-i] for i, ordinal in enumerate(olist[::-1])))
        else:
            return modcomp(11, mod)

weighted_modulus_11 = WeightedModulus11().as_char


class Runes(NumericOnlyCheckDigit):
    """RUNES modulus 10, weighted with 2. Used in NW-7.

    >>> runes('938745343')
    '5'

    """
    def compute(self, ordinals, **kwargs):
        return modcomp(10, sum(sum(divmod(ordinal*(2-(i%2)), 10)) for i, ordinal in enumerate(ordinals)))

runes = Runes().as_char


class Modulus103(CheckDigit):
    """Modulus 103, used in code128. Code should include start char and exclude stop char.

    >>> modulus_103('^105^102123456^100A1')
    '35'

    """
    MESSAGE_CODEC = Code128Codec()

    def compute(self, ordinals, **kwargs):
        csum = 0
        for i, ordinal in enumerate(ordinals):
            if i==0:
                csum = ordinal
            else:
                csum += i*ordinal
        return csum%103

    def as_char(self, message, code=None, errors=None, **kwargs):
        return ''.join(self.message_codec.encode([self.as_ordinal(message, errors, **kwargs)], code=code))
    
_modulus_103 = Modulus103()
modulus_103 = lambda s: _modulus_103.as_char(s, code='C')


if __name__=='__main__':
    from doctest import testmod
    testmod()
    
