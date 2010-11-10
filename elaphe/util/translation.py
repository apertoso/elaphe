# -*- coding: utf-8 -*-
"""Symbology-specific message translations.

Tranlation object parforms conversion from message to sequence of
ordinals, to support alphabets/escape-sequences for individual
symbologies.

"""


class TranslationError(ValueError):
    """
    Exception raised for errors during translation process.
    Kind of ValueError.

    >>> issubclass(TranslationError, ValueError)
    True
    """
    pass


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
    # singletons
    class RAISE_ON_ERROR(object): pass
    class IGNORE_ON_ERROR(object): pass

    def __init__(self, **kwargs):
        """Constructor.
        """
        return

    def translate(self, message, on_error=None, **kwargs):
        """Converts sequence of ordinals to message string.
        """
        queue = []
        for char in message:
            queue.append(char)
            ordinal = None
            try:
                ordinal = self.translate_chars(queue)
            except TranslationError, e:
                if on_error == self.RAISE_ON_ERROR:
                    raise e
                if on_error == self.IGNORE_ON_ERROR:
                    queue = []
                elif on_error is not None:
                    # clear queue, yield replacement and go on
                    queue = []
                    yield on_error
                else:
                    # defaults to ignore,
                    queue = []
            except:
                raise
            if ordinal is None:
                # wait for next char
                continue
            elif ordinal is NotImplemented:
                raise TypeError(u'This type has no valid '
                                'translate_chars() implementation.')
            else:
                # clear queue, yield something not None.
                queue = []
                yield ordinal
    
    def translate_chars(self, chars):
        return NotImplemented


class CharMapTranslation(Translation):
    """
    Translation using character map.

    >>> cmt = CharMapTranslation('+0123456789')
    >>> cmt # doctest: +ELLIPSIS
    <...CharMapTranslation object at ...>

    ``CharMapTranslation.map`` indicates internal translation map.
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
    TranslationError: x not in allowed chars: +0123456789

    Explicit IGNORE_ON_ERROR behave same as default.
    >>> list(cmt.translate('1234xx', on_error=Translation.IGNORE_ON_ERROR))
    [2, 3, 4, 5]

    Replacement chars for ``on_error`` yields itself.
    >>> list(cmt.translate('1234xx', on_error='#'))
    [2, 3, 4, 5, '#', '#']

    Offsets and skip_char are for tweaking non-ordinal alphabets.
    >>> cmt = CharMapTranslation('0*1*2*3*4', offset=100, skip_char='*')
    >>> sorted(cmt.map.items()) # doctest: +ELLIPSIS
    [('0', 100), ('1', 102), ('2', 104), ('3', 106), ('4', 108)]
    >>> list(cmt.translate('2413'))
    [104, 108, 102, 106]

    """
    def __init__(self, chars, offset=0, skip_char=None):
        """Constructor.

        Accepts a positional argument ``char``, and two optional
        parameters: ``offset`` and ``skip_char``.
        """
        self.allowed_chars = chars
        if skip_char:
            self.allowed_chars.replace(skip_char, '')
        self.map = dict(
            (char, idx+offset) for idx, char in enumerate(chars)
            if char!=skip_char)

    def translate_chars(self, chars):
        """
        Performs per-char translation.

        Multiple characters in chars are not allowed.
        """
        if len(chars)>1:
            raise TranslationError(u'Multiple characters not allowed.')
        elif len(chars)<1:
            return
        # else
        char = chars[0]
        if char not in self.map:
            raise TranslationError(
                u'%(char)s not in allowed chars: %(allowed_chars)s' 
                %dict(char=char, allowed_chars=self.allowed_chars))
        # else
        return self.map.get(char)
        


if __name__=="__main__":
    from doctest import testmod
    testmod()
