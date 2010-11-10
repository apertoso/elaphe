# -*- coding: utf-8 -*-
"""Copyright (c) 2010 Yasushi Masuda. All rights reserved.

Elaphe
======

Elaphe is a barcode generator library in Python.


Overview
---------

Elaphe consisits of two major parts: **symbology** and **renderer**.

The **symbology** is a collection of Symbology classes. Symbology
handles data encoding process -- transforms data, computes checksum
and generates sequence or matrice of encoded bits.

The **renderer** is a collection of Renderer classes. Renderer
handles all drawing stuff for various devices -- bitmap or vector
graphics as well as canvas on desktop UI compnent.

"""


from  version import VERSION
__version__ = __VERSION__ = version = VERSION
