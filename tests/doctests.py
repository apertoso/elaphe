# -*- coding: utf-8 -*-


def build_tests():
    import unittest
    import doctest
    import sys
    from os.path import dirname, abspath
    sys.path.insert(0, dirname(dirname(abspath(__file__))))
    suite = unittest.TestSuite()
    from elaphe.bwipp import DEFAULT_PLUGINS
    modules = ['elaphe.utils.checkdigit'] + DEFAULT_PLUGINS
    for modname in modules:
        suite.addTest(doctest.DocTestSuite(modname))
    return suite


if __name__=="__main__":
    from unittest import TextTestRunner
    TextTestRunner().run(build_tests())
