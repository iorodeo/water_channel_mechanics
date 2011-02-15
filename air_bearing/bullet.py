from py2scad import *

def bullet(r,h):
    """
    Creates a bullet shaped object with radius r and height h.
    """
    sphere = Sphere(r=1)
    cut_cube = Cube(size=[3*r, 3*r, 3*r])
    cut_cube = Translate(cut_cube,v=[0,0,-1.5*r])
    bullet = Difference([sphere, cut_cube])
    scale_factor = h/r
    bullet = Scale(bullet,v=[1,1,scale_factor])
    return [bullet]

r = 1.0
h = 3.0
part = bullet(r,h)

prog = SCAD_Prog()
prog.fn = 50
prog.add(part)
prog.write('bullet.scad')



