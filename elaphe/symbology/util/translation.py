# -*- coding: utf-8 -*-
# Copyright (c) 2010 Yasushi Masuda. All rights reserved.
"""
Symbology-specific message translations.

Tranlation object parforms conversion from message to sequence of
ordinals, to support alphabets/escape-sequences for individual
symbologies.

"""
import string


# common exception
class TranslationError(ValueError):
    """
    Exception raised for errors during translation process.
    Kind of ValueError.

    >>> issubclass(TranslationError, ValueError)
    True

    """
    pass


# mapping utility
def charmap(chars, ordinals=None):
    """
    Generate character map for given chars.

    >>> cm1 = charmap('012ABCD')
    >>> sorted(cm1.items()) # doctest: +ELLIPSIS
    [('0', 0), ('1', 1), ('2', 2), ('A', 3), ('B', 4), ('C', 5), ('D', 6)]
    
    If ``ordinals`` is given, it will be mapped to chars.
    >>> oz = [ord(c) for c in 'abAB+/.']
    >>> cm2 = charmap('abAB+/.', ordinals=oz)
    >>> sorted(cm2.items()) # doctest: +ELLIPSIS
    [('+', 43), ('.', 46), ('/', 47), ('A', 65), ... ('b', 98)]
    """
    if ordinals==None:
        ordinals = range(len(chars))
    return dict(zip(chars, ordinals))


class Translation(object):
    """
    Abstract base class for translations.

    Translation class has one public method, ``translate()``
    which converts message into sequence of ordinals.

    >>> t = Translation()
    >>> t # doctest: +ELLIPSIS
    <...Translation object at ...>

    ``translate()`` ordinally returns generator.
    >>> g = t.translate('spam eggs')
    >>> g # doctest: +ELLIPSIS
    <generator object translate at ...>

    ``Translation`` does not implement translate_chars to cause error.
    >>> list(g)
    Traceback (most recent call last):
    ...
    TypeError: This type has no valid translate_chars() implementation.
    
    """
    # Symbolic singletons
    class RAISE_ON_ERROR(object): pass
    class IGNORE_ON_ERROR(object): pass

    def __init__(self, **kwargs):
        """Constructor.
        """

    def reset(self):
        """Resets internal status. Subclass may override.
        """

    def translate(self, message, on_error=None, **kwargs):
        """Converts sequence of ordinals to message string.
        """
        self.reset()
        queue = ''
        for char in message:
            queue += char
            ordinal_info = None
            try:
                ordinal_info = self.translate_chars(queue)
            except TranslationError, e:
                if on_error == self.RAISE_ON_ERROR:
                    raise e
                if on_error == self.IGNORE_ON_ERROR:
                    queue = ''
                elif on_error is not None:
                    # clear queue, yield replacement and go on
                    queue = ''
                    yield on_error
                else:
                    # defaults to ignore,
                    queue = ''
            except:
                raise
            if ordinal_info is None:
                # wait for next char
                continue
            elif ordinal_info is NotImplemented:
                raise TypeError(u'This type has no valid '
                                'translate_chars() implementation.')
            else:
                # clear queue, yield something not None.
                queue = ''
                if isinstance(ordinal_info, (list, tuple)):
                    # iterate if ordinal_info is sequence
                    for ordinal in ordinal_info:
                        yield ordinal
                else:
                    # ... or return it directly
                    yield ordinal_info
    
    def translate_chars(self, chars):
        """
        Translates queued sequence of codewords into ordinal.

        Subclass should override this method to implement actual 
        translation logic.

        """
        return NotImplemented


class MapTranslation(Translation):
    """
    Translation using a map.

    >>> cmt = MapTranslation(charmap('+0123456789'))
    >>> cmt # doctest: +ELLIPSIS
    <...MapTranslation object at ...>

    ``MapTranslation.map`` represents the internal translation map.
    >>> sorted(cmt.map.items()) # doctest: +ELLIPSIS
    [('+', 0), ('0', 1), ... ('8', 9), ('9', 10)]

    ``translate()`` yields sequence of ordinals.
    >>> list(cmt.translate('+++1357+++'))
    [0, 0, 0, 2, 4, 6, 8, 0, 0, 0]

    Invalid chars are ignored at default.
    >>> list(cmt.translate('1234xx'))
    [2, 3, 4, 5]

    Explicit RAISE_ON_ERROR will raise TranslatonError exception.
    >>> list(cmt.translate('1234xx', on_error=Translation.RAISE_ON_ERROR))
    Traceback (most recent call last):
    ...
    TranslationError: x not in allowed chars: ['+', '1', '0', '3', '2', '5', '4', '7', '6', '9', '8']

    Explicit IGNORE_ON_ERROR behave same as default.
    >>> list(cmt.translate('1234xx', on_error=Translation.IGNORE_ON_ERROR))
    [2, 3, 4, 5]

    Replacement chars for ``on_error`` yields itself.
    >>> list(cmt.translate('1234xx', on_error='#'))
    [2, 3, 4, 5, '#', '#']

    """
    def __init__(self, map_, min_chars=1, max_chars=1, extra_map=None,
                 **kwargs):
        """
        Constructor.

        Accepts a positional argument ``char``, and three optional
        parameters: min_chars, max_chars, and extra_map.

        """
        super(MapTranslation, self).__init__(**kwargs)
        self.min_chars, self.max_chars = min_chars, max_chars
        self.map = map_
        self.allowed_chars = map_.keys()
        if extra_map:
            self.map.update(extra_map)

    def translate_chars(self, chars):
        """
        Performs per-char translation.

        Multiple characters in chars are not allowed.

        """
        if len(chars)<self.min_chars:
            return
        elif len(chars)>self.max_chars:
            raise TranslationError(u'Unable to translate chars: %s.' %chars)
        else:
            if chars not in self.allowed_chars:
                raise TranslationError(
                    u'%(chars)s not in allowed chars: %(allowed_chars)s' 
                    %dict(chars=chars, allowed_chars=self.allowed_chars))
            return self.map.get(chars)


# common translation shortcuts 
digits = MapTranslation(charmap('0123456789')).translate


if __name__=="__main__":
    from doctest import testmod
    testmod()
