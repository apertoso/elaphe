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


def modulus_4(ordinals):
    """
    modulus 4, used for parity bits in EAN-2.
    
    >>> [modulus_4([0, i]) for i in range(10)]
    [0, 1, 2, 3, 0, 1, 2, 3, 0, 1]

    """
    return sum(10**(1-i)*ordinal 
               for i, ordinal in enumerate(ordinals)
               if i<2)%4

def modulus_43(ordinals):
    """
    Modulus-43, used in Code39.

    >>> modulus_43(translation.code39('ABCD1234+'))
    11

    """
    return sum(ordinals)%43


def modulus_10_w3(ordinals):
    """
    Modulus 10, weighted with 3. Used in JAN ITF and NW-7.

    >>> modulus_10_w3(translation.digits('12345678'))
    4
    >>> modulus_10_w3(translation.digits('4912345'))
    6
    """
    return modcomp(
        10, 
        sum(ordinal*(1+2*((i+1)%2)) 
            for i, ordinal in enumerate(reversed(list(ordinals)))))


def upc_checksum(ordinals):
    """
    UPC-A checksum, kind of modulus10-w3.

    >>> upc_checksum(translation.digits('03600029145'))
    2
    """
    return modcomp(
        10, 
        sum(ordinal*(1+2*(i+1%2)) 
            for i, ordinal in enumerate(ordinals)))
    

def modulus_16(ordinals):
    """
    Modulus 16, used in NW-7. Argument should include start/stop/checkdigit.
  
    >>> modulus_16(translation.nw7('A19+1243*B'))
    12

    """
    return modcomp(16, sum(ordinals))


def modulus_11(ordinals):
    """
    Modulus 11, used in NW-7. Argucment should exclude start/stop.

    >>> modulus_11(translation.digits('2431245*'))
    6
    
    """
    return modcomp(
        11, 
        sum(ordinal*(7-i) 
            for i, ordinal in enumerate(ordinals)
            if i<6))


def modulus_10_w2(ordinals):
    """
    Modulus 10, weighted with 2. Used in NW-7. 
    Argument should exclude start/stop/checkdigit.

    >>> modulus_10_w2(translation.digits('938745343'))
    7

    """
    return modcomp(
        10, 
        sum(ordinal*(2-(i%2)) 
            for i, ordinal in enumerate(ordinals)))


def check_dr_7(ordinals):
    """
    7-check DR checkdigit, used in NW-7. 
    Argument should exclude start/stop/checkdigit.

    >>> check_dr_7(translation.digits('8745343'))
    5

    """
    return sum(
        (10**(6-i)*ordinal)
        for i, ordinal in enumerate(ordinals) if i<7)%7


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


def modulus_103(ordinals):
    """
    Modulus 103, used in code128. 
    Code should include start char and exclude stop char.

    >>> modulus_103(translation.code128('^105^102123456^100A1'))
    35

    """
    return sum(
        (ordinal if i==0 else i*ordinal)
        for i, ordinal in enumerate(ordinals))%103


if __name__=='__main__':
    import translation
    from doctest import testmod
    testmod()
    
