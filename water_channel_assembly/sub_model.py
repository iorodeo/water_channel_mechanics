import scipy
from py2scad import *


class SubModel(object):

    def __init__(self,params):
        self.params = params
        self.parts = {}
        self.__make_anterior_cap()
        self.__make_motor_housing()
        self.__make_fluid_housing()
        self.__make_nozzle()
        self.__make_hydrofoil()

    def __make_hydrofoil(self):
        h = self.params['hydrofoil_height']
        w = self.params['hydrofoil_width']
        l = self.params['hydrofoil_length']
        hydrofoil = Cylinder(r1=0.5,r2=0.5,h=h)
        hydrofoil = Scale(hydrofoil,v=[l,w,1])
        x_shift = 0.5*l
        z_shift =  0.5*h + 0.5*self.params['body_diameter']
        hydrofoil = Translate(hydrofoil,v=[x_shift,0,z_shift])
        self.parts['hydrofoil'] = hydrofoil

    def __make_nozzle(self):
        h = self.params['nozzle_length']
        r2 = 0.5*self.params['body_diameter']
        r1 = 0.5*self.params['nozzle_exit_diameter']
        epsilon = self.params['nozzle_trans_param']
        nozzle = make_nozzle(r1,r2,h,epsilon)
        nozzle = Rotate(nozzle,a=90,v=[0,1,0])
        x_shift = -self.params['fluid_housing_length'] - 0.5*h
        nozzle = Translate(nozzle,v=[x_shift,0,0])
        self.parts['nozzle'] = nozzle

    def __make_anterior_cap(self):
        r = 0.5*self.params['body_diameter']
        h = self.params['anterior_cap_length']
        cap = bullet(r,h)
        cap = Rotate(cap,a=90,v=[0,1,0])
        x_shift = self.params['motor_housing_length']
        cap = Translate(cap,v=[x_shift,0,0])
        self.parts['anterior_cap'] = cap

    def __make_fluid_housing(self):
        r = 0.5*self.params['body_diameter']
        h = self.params['fluid_housing_length']
        fuild_housing = Cylinder(r1=r, r2=r, h=h)
        fuild_housing = Rotate(fuild_housing,a=90,v=[0,1,0])
        fuild_housing = Translate(fuild_housing,v=[-0.5*h,0,0])
        self.parts['fuild_housing'] = fuild_housing

    def __make_motor_housing(self):
        r = 0.5*self.params['body_diameter']
        h = self.params['motor_housing_length']
        motor_housing = Cylinder(r1=r, r2=r, h=h)
        motor_housing = Rotate(motor_housing,a=90,v=[0,1,0])
        motor_housing = Translate(motor_housing,v=[0.5*h,0,0])
        self.parts['motor_housing'] = motor_housing

    def get_assembly(self):
        # Create union of all parts
        sub = Union(self.parts.values())
        # Shift so that sub is centered w.r.t to hydrofoil
        x_shift = -0.5*self.params['hydrofoil_length']
        sub = Translate(sub,v=[x_shift,0,0])
        # Shidt so that top of hydrofoil is at z=0
        z_shift = -0.5*self.params['body_diameter'] - self.params['hydrofoil_height']
        sub = Translate(sub,v=[0,0,z_shift])
        return sub


def bullet(r,h):
    """
    Creates a bullet shaped object with radius r and height h.
    """
    sphere = Sphere(r=1)
    cut_cube = Cube(size=[3*r, 3*r, 3*r])
    cut_cube = Translate(cut_cube,v=[0,0,-1.5*r])
    bullet = Difference([sphere, cut_cube])
    vscale = [r,r,h]
    bullet = Scale(bullet,v=vscale)
    return [bullet]

def make_nozzle(r1, r2, h, epsilon, num_pts = 100):
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
    y = scipy.absolute(r2-r1)*y/(y.max() -y.min())
    y = y +r1 - y.min()
    # Create polygon and rotate into position
    poly = curve2polygon(x,y)
    poly = Rotate(poly,a=-90,v=[0,0,1])
    # Revolve
    part = Rotate_Extrude(poly)
    return part


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

# -----------------------------------------------------------------------------
if __name__ == "__main__":

    from params import sub_model_params

    sub = SubModel(params=sub_model_params)
    sub_assem = sub.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 70
    prog.add(sub_assem)
    prog.write('sub_model.scad')
