# coding: utf-8
from bases import Barcode, LinearCodeRenderer, DPI

class Rss14(Barcode):
    """
    >>> bc = Rss14()
    >>> bc # doctest: +ELLIPSIS
    <__main__.Rss14 object at ...>
    >>> print bc.render_ps_code('24012345678905') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 96 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (24012345678905) () rss14 barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('24012345678905', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'rss14'
    aliases = ('rss-14', 'rss_14', 'rss 14')
    class _Renderer(LinearCodeRenderer):
        default_options = dict(textyoffset=-7, textsize=10, height=0.3)

        def _code_bbox(self, codestring):
            """
            >>> r = Rss14._Renderer({})
            >>> r._code_bbox('24012345678905')
            [0, 0, 96, 72.0]
            """
            return [0, 0, 1+1+16+15*4+16+1+1, DPI]

        def _text_bbox(self, codestring):
            """
            >>> r = Rss14._Renderer({})
            >>> r._text_bbox('24012345678905')
            [0, -5.0, 96, 72.0]
            """
            hidestars = self.lookup_option('hidestars', False)
            textyoffset = self.lookup_option('textyoffset', 0)
            textsize = self.lookup_option('textsize', 10)
            textmaxy = textyoffset + textsize
            textmaxx = 9*len(codestring)+4+0.6*textsize
            codeminx, codeminy, codemaxx, codemaxy = self._code_bbox(codestring)
            return [codeminx, codeminy-textsize/2.0, codemaxx, codemaxy]
        
        def build_params(self, codestring):
            params = super(Rss14._Renderer, self).build_params(codestring)
            params['bbox'] = "%d %d %d %d" %self._boundingbox(
                self._code_bbox(codestring), self._text_bbox(codestring))
            return params
    renderer = _Renderer


class RssLimited(Barcode):
    """
    >>> bc = RssLimited()
    >>> bc # doctest: +ELLIPSIS
    <__main__.RssLimited object at ...>
    >>> print bc.render_ps_code('24012345678905') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 74 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (24012345678905) () rsslimited barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('24012345678905', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> # _.show()
    """
    codetype = 'rsslimited'
    aliases = ('rss limited', 'rss_limited', 'rss-limited',
               'rss14limited', 'rss14 limited', 'rss14_limited', 'rss14-limited',)
    class _Renderer(Rss14._Renderer):
        default_options = dict(textyoffset=-7, textsize=10, height=0.3)

        def _code_bbox(self, codestring):
            """
            >>> r = RssLimited._Renderer({})
            >>> r._code_bbox('THIS IS CODE39')
            [0, 0, 74, 72.0]
            """
            return [0, 0, 1+1+26+18+26+1+1, DPI]
    renderer = _Renderer


# EXPERIMENTAL
class RssExpanded(Barcode):
    """
    >>> bc = RssExpanded()
    >>> bc # doctest: +ELLIPSIS
    <__main__.RssExpanded object at ...>
    >>> print bc.render_ps_code('000000010011001010100001000000010000') # doctest: +ELLIPSIS
    %!PS-Adobe-2.0
    %%Pages: (attend)
    %%Creator: Elaphe powered by barcode.ps
    %%BoundingBox: 0 -5 74 72
    %%LanguageLevel: 2
    %%EndComments
    ...
    gsave
    0 0 moveto
    1.000000 1.000000 scale
    (000000010011001010100001000000010000) () rssexpanded barcode
    grestore
    showpage
    <BLANKLINE>
    >>> bc.render('000000010011001010100001000000010000', options=dict(includetext=None), scale=2, margin=10) # doctest: +ELLIPSIS
    <PIL.EpsImagePlugin.EpsImageFile instance at ...>
    >>> _.show()
    """
    
    codetype = 'rssexpanded'
    aliases = ('rss expanded', 'rss_expanded', 'rss-expanded',
               'rss14expanded', 'rss14 expanded', 'rss14_expanded', 'rss14-expanded',)
    class _Renderer(Rss14._Renderer):
        default_options = dict(textyoffset=-7, textsize=10, height=0.3)

        def _code_bbox(self, codestring):
            """
            >>> r = RssExpanded._Renderer({})
            >>> r._code_bbox('000000010011001010100001000000010000')
            [0, 0, 74, 72.0]
            """
            # TBD this should be wrong!
            return [0, 0, 15*(len(codestring)/8+3), DPI]
    renderer = _Renderer


if __name__=="__main__":
    from doctest import testmod
    testmod()