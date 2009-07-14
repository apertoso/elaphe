# -*- coding: utf-8 -*-

def build_tests():
    import unittest
    import doctest
    import sys
    from os.path import dirname
    sys.path.insert(0, dirname(dirname(__file__)))
    suite = unittest.TestSuite()
    from elaphe.bwipp import DEFAULT_PLUGINS
    for modname in DEFAULT_PLUGINS:
        suite.addTest(doctest.DocTestSuite(modname))
    return suite
