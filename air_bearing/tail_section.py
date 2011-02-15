import scipy
import pylab
from py2scad import *



def curve2polygon(x_pts,y_pts):
    """
    Creates a 2D polygon from an x,y curve
    """
    points = []
    for x,y in zip(x_pts, y_pts):
        points.append([x,y])
    points.append([x_pts[-1], 0])
    points.append([x_pts[0],0])
    points.reverse()
    paths = [range(0,len(points))]
    poly = Polygon(points=points, paths=paths)
    return poly

def tail_section(r1, r2, h, epsilon, num_pts = 100):
    """
    Creates submarine tail section
    r1      = bottom radius
    r2      = top radius
    h       = height
    epsilon = transition parameter
    """
    x = scipy.linspace(-0.5*h, 0.5*h,num_pts)
    y = -scipy.arctan(epsilon*x)
    # Shift to get correct radii
    y = r2*y/(y.max() -y.min())
    y = y +r1 - y.min()
    # Create polygon and rotate into position
    poly = curve2polygon(x,y)
    poly = Rotate(poly,a=-90,v=[0,0,1])
    # Revolve
    part = Rotate_Extrude(poly)
    return part  


part = tail_section(1,2,10,0.3)
prog = SCAD_Prog()
prog.fn = 60
prog.add(part)
prog.write('test.scad')
