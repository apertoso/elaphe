# coding: utf-8
"""
Various checksum algorithms

Copyright (c) 2010 Yasushi Masuda. All rights reserved.

"""
def modcomp(b, n):
    """Computes complemented modulus (b, n).

    >>> modcomp(1, 1), modcomp(1, 2), modcomp(1, 3), modcomp(2, 1), modcomp(2, 2), modcomp(2, 3)
    (0, 0, 0, 1, 0, 1)
    """
    return (b-n%b)%b


def modulus_43(ordinals):
    """Modulus-43, used in Code39.

    >>> modulus_43(translation.code39('ABCD1234+'))
    11
    """
    return sum(ordinals)%43

# def modulus_10_w3 = 

# class NumericOnlyCheckDigit(CheckDigit):
#     MESSAGE_CODEC = CharMapCodec(string.digits)


# class Modulus10W3(NumericOnlyCheckDigit):
#     """Modulus 10, weighted with 3. Used in JAN ITF and NW-7.
    
#     >>> Modulus10W3().as_char('490123456789')
#     '4'

#     """
#     def compute(self, ordinals, **kwargs):
#         return modcomp(10, sum(ordinal*(1+2*(i%2)) for i, ordinal in enumerate(ordinals)))

# modulus_10_w3 = Modulus10W3().as_char


# class Modulus16(CheckDigit):
#     """Modulus 16, used in NW-7. Argument should include start/stop/checkdigit.
    
#     >>> Modulus16().as_char('A19+1243*B')
#     ':'

#     """
#     MESSAGE_CODEC = CharMapCodec(string.digits+'-$:/.+ABCD')

#     def normalize_message(self, message):
#         list_chars = list(message)
#         return (c.upper() for i, c in enumerate(list_chars) if i!=len(list_chars)-2)

#     def compute(self, ordinals, **kwargs):
#         return modcomp(16, sum(ordinals))

# modulus_16 = Modulus16().as_char


# class Modulus11(NumericOnlyCheckDigit):
#     """Modulus 11, used in NW-7. Argucment should exclude start/stop.
    
#     >>> Modulus11().as_char('2431245*')
#     '6'

#     """
#     def normalize_message(self, message):
#         return message[:6]

#     def compute(self, ordinals, **kwargs):
#         return modcomp(11, sum(ordinal*(7-i) for i, ordinal in enumerate(ordinals)))

# modulus_11 = Modulus11().as_char


# class Modulus10w2(NumericOnlyCheckDigit):
#     """Modulus 10, weighted with 2. Used in NW-7. Argument should exclude start/stop/checkdigit.

#     >>> modulus_10_w2('938745343')
#     '7'

#     """
#     def compute(self, ordinals, **kwargs):
#         return modcomp(10, sum(ordinal*(2-(i%2)) for i, ordinal in enumerate(ordinals)))

# modulus_10_w2 = Modulus10w2().as_char


# class CheckDR7(NumericOnlyCheckDigit):
#     """7-check DR checkdigit, used in NW-7. Argument should exclude start/stop/checkdigit.

#     >>> check_DR_7('8745343')
#     '5'

#     """
#     def as_ordinal(self, message, errors=None, **kwargs):
#         return int(''.join(message), 10)%7

#     def as_char(self, message, errors=None, **kwargs):
#         return ''.join(self.message_codec.encode([self.as_ordinal(message, errors, **kwargs)]))

# check_DR_7 = CheckDR7().as_char


# class WeightedModulus11(NumericOnlyCheckDigit):
#     """Weighted modulus 11, used in NW-7. Argument should exclude start/stop.

#     >>> weighted_modulus_11('5012924346')
#     '4'
#     >>> weighted_modulus_11('0200290068')
#     '1'

#     """
#     WEIGHT_1 = [6, 3, 5, 9, 10, 7, 8, 4, 5, 3, 6, 2]
#     WEIGHT_2 =  [5, 8, 6, 2, 10, 4, 3, 7, 6, 8, 5, 9]

#     def compute(self, ordinals, **kwargs):
#         olist = list(ordinals)
#         mod = sum(ordinal*self.WEIGHT_1[-1-i] for i, ordinal in enumerate(olist[::-1]))%11
#         if mod==0:
#             return 0
#         elif mod==1:
#             return modcomp(11, sum(ordinal*self.WEIGHT_2[-1-i] for i, ordinal in enumerate(olist[::-1])))
#         else:
#             return modcomp(11, mod)

# weighted_modulus_11 = WeightedModulus11().as_char


# class Runes(NumericOnlyCheckDigit):
#     """RUNES modulus 10, weighted with 2. Used in NW-7.

#     >>> runes('938745343')
#     '5'

#     """
#     def compute(self, ordinals, **kwargs):
#         return modcomp(10, sum(sum(divmod(ordinal*(2-(i%2)), 10)) for i, ordinal in enumerate(ordinals)))

# runes = Runes().as_char


# class Modulus103(CheckDigit):
#     """Modulus 103, used in code128. Code should include start char and exclude stop char.

#     >>> modulus_103('^105^102123456^100A1')
#     '35'

#     """
#     MESSAGE_CODEC = Code128Codec()

#     def compute(self, ordinals, **kwargs):
#         csum = 0
#         for i, ordinal in enumerate(ordinals):
#             if i==0:
#                 csum = ordinal
#             else:
#                 csum += i*ordinal
#         return csum%103

#     def as_char(self, message, code=None, errors=None, **kwargs):
#         return ''.join(self.message_codec.encode([self.as_ordinal(message, errors, **kwargs)], code=code))
    
# _modulus_103 = Modulus103()
# modulus_103 = lambda s: _modulus_103.as_char(s, code='C')


if __name__=='__main__':
    import sys; sys.path.insert(0, '.')
    import translation
    from doctest import testmod
    testmod()
    
