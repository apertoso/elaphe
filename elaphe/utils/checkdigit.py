# -*- coding: utf-8 -*-
"""Various checkdigits.
"""
import string

def charmap(chars):
    forward_map = dict(t[::-1] for t in enumerate(chars)) # char to int
    reverse_map = dict(t for t in enumerate(chars)) # int to char
    return forward_map, reverse_map

def modcomp(b, n):
    return (b-n%b)%b

def modulus_43(s):
    """Modulus-43, used in Code39.
    
    >>> modulus_43('ABCD1234+')
    'B'
    
    """
    table_src = string.digits+string.ascii_uppercase+'-. $/+%'
    fwd, rev = charmap(table_src)
    return rev[sum(fwd[c] for c in s.upper()) % 43]


def modulus_10_w3(s):
    """Modulus 10, weighted with 3. Used in JAN ITF and NW-7.
    
    >>> modulus_10_w3('490123456789')
    '4'

    """
    table_src = string.digits
    fwd, rev = charmap(table_src)
    return rev[modcomp(10, sum(fwd[c]*(1+2*(i%2)) for i, c in enumerate(list(s))))]


def modulus_16(s):
    """Modulus 16, used in NW-7. Argument should include start/stop/checkdigit.
    
    >>> modulus_16('A19+1243*B')
    ':'

    """
    table_src = string.digits+'-$:/.+ABCD'
    fwd, rev = charmap(table_src)
    return rev[modcomp(16, sum(fwd[c] for i, c in enumerate(list(s)) if i!=len(s)-2))]


def modulus_11(s):
    """Modulus 11, used in NW-7. Argucment should exclude start/stop.
    
    >>> modulus_11('2431245*')
    '6'

    """
    table_src = string.digits
    fwd, rev = charmap(table_src)
    return rev[modcomp(11, sum(fwd[c]*(7-i) for i, c in enumerate(list(s[:6]))))]


def modulus_10_w2(s):
    """Modulus 10, weighted with 2. Used in NW-7. Argument should exclude start/stop/checkdigit.

    >>> modulus_10_w2('938745343')
    '7'

    """
    table_src = string.digits
    fwd, rev = charmap(table_src)
    return rev[modcomp(10, sum(fwd[c]*(2-(i%2)) for i, c in enumerate(list(s))))]


def check_DR_7(s):
    """7-check DR checkdigit, used in NW-7. Argument should exclude start/stop/checkdigit.

    >>> check_DR_7('8745343')
    '5'

    """
    return str(int(s, 10)%7)


def weighted_modulus_11(s):
    """Weighted modulus 11, used in NW-7. Argument should exclude start/stop.

    >>> weighted_modulus_11('5012924346')
    '4'
    >>> weighted_modulus_11('0200290068')
    '1'

    """
    table_src = string.digits
    fwd, rev = charmap(table_src)
    weight_1 = [6, 3, 5, 9, 10, 7, 8, 4, 5, 3, 6, 2]
    weight_2 =  [5, 8, 6, 2, 10, 4, 3, 7, 6, 8, 5, 9]
    mod = sum(fwd[c]*weight_1[-1-i] for i, c in enumerate(list(s[::-1])))%11
    if mod==0:
        return rev[0]
    elif mod==1:
        return rev[modcomp(11, sum(fwd[c]*weight_2[-1-i] for i, c in enumerate(list(s[::-1]))))]
    else:
        return rev[(11-mod)%11]

def runes(s):
    """RUNES modulus 10, weighted with 2. Used in NW-7.

    >>> runes('938745343')
    '5'

    """
    table_src = string.digits
    fwd, rev = charmap(table_src)
    return rev[modcomp(10, sum(sum(divmod(fwd[c]*(2-(i%2)), 10)) for i, c in enumerate(list(s))))]


ASCII_7BITS = ''.join(chr(i) for i in range(128))
code128_A_tbl = ASCII_7BITS[32:96] + ASCII_7BITS[:32]
code128_B_tbl = ASCII_7BITS[32:128]

def code128_ords(s):
    """Converts a string into a sequence of code128 ordinals.

    >>> list(code128_ords('^103AZ_^^_\\0\\1\\2'))
    [('A', 103), ('A', 33), ('A', 58), ('A', 63), ('A', 62), ('A', 63), ('A', 64), ('A', 65), ('A', 66)]
    >>> list(code128_ords('^104AZ_^^_\\x60ab'))
    [('B', 104), ('B', 33), ('B', 58), ('B', 63), ('B', 62), ('B', 63), ('B', 64), ('B', 65), ('B', 66)]
    
    >>> list(code128_ords('^105^102^'))
    [('C', 105), ('C', 102)]

    >>> list(code128_ords('^105^102123456^100A1'))
    [('C', 105), ('C', 102), ('C', 12), ('C', 34), ('C', 56), ('B', 100), ('B', 33), ('B', 17)]

    """
    code = None
    escape = False
    carry = ''
    for c in s:
        if escape:
            if c=='^':
                escape, carry = False, ''
                yield code, 62
            elif c in '0123456789':
                carry+=c
                ord_ = int(carry, 10)
                if ord_ in range(96, 108):
                    escape, carry = False, ''
                    if ord_ in (99, 105):
                        code = 'C'
                    if ord_ in (100, 104):
                        code = 'B'
                    elif ord_ in (101, 103):
                        code = 'A'
                    yield code, ord_
                if ord_ >=108:
                    raise ValueError(u'%d is not allowed for Code128' %ord_)
            else:
                raise ValueError
        else:
            if c=='^': # escape in
                escape = True
                carry = ''
                continue
            else:
                if code == 'A':
                    ord_ = code128_A_tbl.index(c)
                elif code == 'B':
                    ord_ = code128_B_tbl.index(c)
                elif code == 'C':
                    if carry:
                        ord_ = int(carry+c, 10)
                        carry = ''
                    else:
                        carry = c
                        continue
                else:
                    raise ValueError(u'Invalid code: %s' %code)
                yield code, ord_
    if carry:
        raise ValueError(u'Unexpected end of codestring, residue=%s' %carry)


def modulus_103(s):
    """Modulus 103, used in code128. Code should include start char and exclude stop char.

    >>> modulus_103('^105^102123456^100A1')
    'C'
    """
    csum = 0
    for i, (code, ord_) in enumerate(code128_ords(s)):
        if i==0:
            csum = ord_
        else:
            csum += i*ord_
    modulated_ord = csum%103
    if code in 'AB':
        return {'A': code128_A_tbl, 'B': code128_B_tbl}[code][modulated_ord]
    else:
        return str(modulated_ord)


if __name__=='__main__':
    from doctest import testmod
    testmod()
    
