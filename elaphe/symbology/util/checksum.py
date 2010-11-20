# coding: utf-8
# Copyright (c) 2010 Yasushi Masuda. All rights reserved.
"""Various checksum algorithms
"""


def modcomp(b, n):
    """
    Computes complemented modulus (b, n).

    >>> modcomp(1, 1), modcomp(1, 2), modcomp(1, 3), modcomp(2, 1), modcomp(2, 2), modcomp(2, 3)
    (0, 0, 0, 1, 0, 1)

    """
    return (b-n%b)%b


class Modulus(object):
    """Simple factory for modulus N functions

    >>> mod43 = Modulus(43)
    >>> mod43([6]*8)
    5

    """
    def __init__(self, modulo, weight_func=None, complement=False):
        self.modulo = modulo
        self.complement = complement
        self.weight_func = weight_func
    
    def __call__(self, ordinals):
        ordinals = list(ordinals)
        if self.weight_func:
            weights = self.weight_func(ordinals)
        else:
            weights = [1]*len(ordinals)
        ret = sum(o*w for o, w in zip(ordinals, weights))%self.modulo
        if self.complement:
            ret = (self.modulo-ret)%self.modulo
        return ret


check_dr_7 = Modulus(7, weight_func=(lambda os: [(10**(6-i) if i<7 else 0) for i in range(len(os))]))
modulus_4 = Modulus(4, weight_func=(lambda os: [(int(10**(i-1)) if i<2 else 1) for i in range(len(os))]))
modulus_10_w3 = Modulus(10, weight_func=(lambda os: [(1+2*((i+1)%2)) for i in range(len(os))[::-1]]), complement=True)
modulus_10_w2 = Modulus(10, weight_func=(lambda os: [(2-(i%2)) for i in range(len(os))]), complement=True)
modulus_11 = Modulus(11, weight_func=(lambda os: [((7-i) if i<6 else 0) for i in range(len(os))]), complement=True)
modulus_16 = Modulus(16, complement=True)
modulus_43 = Modulus(43)
modulus_47 = Modulus(47, weight_func=(lambda os: range(1, len(os)+1)[::-1])) # Untested!
modulus_103 = Modulus(103, weight_func=(lambda os: [max(i, 1) for i in range(len(os))]))
upc_checksum = Modulus(10, weight_func=(lambda os: [(1+2*((i+1)%2)) for i in range(len(os))]), complement=True)


__test__= {'Modulus instances': """
Modulus 16, used in NW-7. Argument should include start/stop/checkdigit.

>>> nw7_ordinals = [16, 1, 9, 15, 1, 2, 4, 3, 17] # 'A19+1243*B'
>>> modulus_16(nw7_ordinals)
12

modulus 4, used for parity bits in EAN-2.

>>> [modulus_4([0, i]) for i in range(10)]
[0, 1, 2, 3, 0, 1, 2, 3, 0, 1]

Modulus 10, weighted with 3. Used in JAN ITF and NW-7.

>>> modulus_10_w3(translation.digits('12345678'))
4
>>> modulus_10_w3(translation.digits('4912345'))
6

Modulus 103, used in code128. 
Code should include start char and exclude stop char.

>>> modulus_103([41, 41, 41, 41, 41]) # (41+41+82+123+164)%103
39

7-check DR checkdigit, used in NW-7. 
Argument should exclude start/stop/checkdigit.

>>> check_dr_7(translation.digits('8745343'))
5

Modulus 10, weighted with 2. Used in NW-7. 
Argument should exclude start/stop/checkdigit.

>>> modulus_10_w2(translation.digits('938745343'))
7

Modulus 11, used in NW-7. Argucment should exclude start/stop.

>>> modulus_11(translation.digits('2431245*'))
6
    
UPC-A checksum, kind of modulus10-w3.

>>> upc_checksum(translation.digits('03600029145'))
2
>>> upc_checksum(translation.digits('06510000432'))
7
>>> upc_checksum(translation.digits('54300018670'))
6

"""}


def weighted_modulus_11(ordinals):
    """
    Weighted modulus 11, used in NW-7. Argument should exclude start/stop.

    >>> weighted_modulus_11(translation.digits('5012924346'))
    4
    >>> weighted_modulus_11(translation.digits('0200290068'))
    1

    """
    WEIGHTS_1 = [6, 3, 5, 9, 10, 7, 8, 4, 5, 3, 6, 2]
    WEIGHTS_2 =  [5, 8, 6, 2, 10, 4, 3, 7, 6, 8, 5, 9]
    olist = list(ordinals)[::-1]
    mod = sum(ordinal*WEIGHTS_1[-1-i] 
              for i, ordinal in enumerate(olist))%11
    if mod==0:
        return 0
    elif mod==1:
        return modcomp(
            11, 
            sum(ordinal*WEIGHTS_2[-1-i] 
                for i, ordinal in enumerate(olist)))
    else:
        return modcomp(11, mod)


def runes(ordinals):
    """
    RUNES modulus 10, weighted with 2. Used in NW-7.

    >>> runes(translation.digits('938745343'))
    5

    """
    return modcomp(
        10, 
        sum(sum(divmod(ordinal*(2-(i%2)), 10)) 
            for i, ordinal in enumerate(ordinals)))


if __name__=='__main__':
    import translation
    from doctest import testmod
    testmod()
