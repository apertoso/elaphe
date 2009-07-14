# coding: utf-8
from bases import Barcode

DEFAULT_PLUGINS = [
    'elaphe.bwipp.ean', 'elaphe.bwipp.upc', 'elaphe.bwipp.code128',
    'elaphe.bwipp.code39', 'elaphe.bwipp.code93', 'elaphe.bwipp.i2of5',
    'elaphe.bwipp.rss', 'elaphe.bwipp.pharmacode', 'elaphe.bwipp.code25',
    'elaphe.bwipp.code11', 'elaphe.bwipp.codabar', 'elaphe.bwipp.onecode',
    'elaphe.bwipp.postnet', 'elaphe.bwipp.royalmail', 'elaphe.bwipp.auspost',
    'elaphe.bwipp.kix', 'elaphe.bwipp.japanpost', 'elaphe.bwipp.msi',
    'elaphe.bwipp.plessey', 'elaphe.bwipp.raw', 'elaphe.bwipp.symbol',
    'elaphe.bwipp.pdf417', 'elaphe.bwipp.datamatrix', 'elaphe.bwipp.qrcode',
    'elaphe.bwipp.maxicode', 'elaphe.bwipp.azteccode']

if __name__=="__main__":
    DEFAULT_PLUGINS = [s.replace('elaphe.bwipp.', '') for s in DEFAULT_PLUGINS]
    

def load_plugins():
    """
    >>> sorted(Barcode.registry.keys()) # doctest: +ELLIPSIS
    ['auspost', 'aztec', 'aztec code', ... 'usps_onecode', 'uspsonecode']
    >>> import md5
    >>> md5.md5(str(sorted(Barcode.registry.keys()))).hexdigest()
    '9cba97993dd365182fbff8a7d3d6df90'
    """
    for PL in DEFAULT_PLUGINS:
        try:
            __import__(PL, fromlist=[PL])
        except ImportError, e:
            import sys
            sys.stdout.write(u'Warning: %s\n' %e)
    Barcode.update_codetype_registry()
load_plugins()


def barcode(codetype, codestring, options=None, **kw):
    """
    >>> barcode('nonexistent', '977147396801')
    Traceback (most recent call last):
    ...
    ValueError: No renderer for codetype nonexistent
    >>> barcode('qrcode', 'Hello Barcode Writer In Pure PostScript.',
    ...         options=dict(version=9, eclevel='M'), margin=10, data_mode='8bits') # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    # search for codetype registry
    renderer = Barcode.resolve_codetype(codetype)
    if renderer:
        return renderer().render(codestring, options=options, **kw)
    raise ValueError(u'No renderer for codetype %s' %codetype)


if __name__=="__main__":
    from doctest import testmod
    testmod()


