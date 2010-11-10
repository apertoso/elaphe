# -*- coding: utf-8 -*-
"""Symbology-specific message translations.

Tranlation object parforms conversion from message to sequence of
ordinals, to support alphabets/escape-sequences for individual
symbologies.

"""


class TranslationError(ValueError):
    pass


class Translation(object):
    """
    Abstract base class for translations.

    Translation class has one public method, ``translate()``
    which converts message into sequence of ordinals.

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
            try:
                ordinal = self.translate_chars(queue)
            except TranslationError:
                if on_error == self.RAISE_ON_ERROR:
                    raise
                elif on_error is not None:
                    # clear queue, yield replacement and go on
                    queue = []
                    yield on_error
                else:
                    # defaults to ignore, just clear queue
                    queue = []
            except:
                raise
            if ordinal is not None:
                # clear queue, yield something not None.
                queue = []
                yield ordinal
    
    def translate_chars(self, chars):
        return NotImplemented


