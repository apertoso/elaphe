# coding: utf-8
from fim import *

from reportlab.graphics import renderPDF
from os import system

if __name__=='__main__':
    sf = FIM()
    g = sf.generate('a')
    lbx, lby, rtx, rty = g.getBounds()
    w, h = rtx-lbx, rty-lby
    canvw, canvh = w*4.8, h*1.2+20
    d = shapes.Drawing(canvw, canvh)
    for i, ch in enumerate('abcd'):
        g = sf.generate(ch)
        ofx, ofy = ((0.1+i*1.2)*w, h*0.1+20)
        d.add(shapes.Line(ofx-0.1*w, 0, ofx-0.1*w, canvh))
        g.shift(ofx, ofy)
        # s.shift(ofx, ofy)
        d.add(g)
        s = shapes.String(ofx, ofy-10, 'FIM %s' %ch.upper())
        d.add(s)
        
    renderPDF.drawToFile(d, 'test.pdf')
    system('open test.pdf')
    
    
    

