from __future__ import division
import scipy
from py2scad import *


class SubModel(object):

    def __init__(self,params):
        self.params = params
        self.parts = {}
        self.__make_mount_plate()
        self.__make_hydrofoil()
        self.__make_nozzle()
        self.__make_anterior_cap()
        self.__make_motor_housing()
        self.__make_fluid_housing()

    def __make_mount_plate(self):
        self.mount_plate_x = self.params['mount_plate_length']
        self.mount_plate_y = self.params['mount_plate_length']
        self.mount_plate_z = self.params['mount_plate_thickness']
        mount_plate = Cube(size=[self.mount_plate_x,self.mount_plate_y,self.mount_plate_z])
        self.parts['mount_plate'] = mount_plate

    def __make_hydrofoil(self):
        self.hydrofoil_y = self.params['hydrofoil_width']
        self.hydrofoil_x = self.params['hydrofoil_length']
        self.hydrofoil_z = self.params['hydrofoil_height']
        hydrofoil = Cylinder(r1=0.5,r2=0.5,h=self.hydrofoil_z)
        hydrofoil = Scale(hydrofoil,v=[self.hydrofoil_x,self.hydrofoil_y,1])
        # x_shift = 0.5*l
        # hydrofoil_tz =  0.5*h + 0.5*self.params['body_diameter']
        self.hydrofoil_tz =  self.hydrofoil_z/2 + self.mount_plate_z/2
        hydrofoil = Translate(hydrofoil,v=[0,0,-self.hydrofoil_tz])
        self.parts['hydrofoil'] = hydrofoil

    def __make_nozzle(self):
        h = self.params['nozzle_length']
        r2 = 0.5*self.params['body_diameter']
        r1 = 0.5*self.params['nozzle_exit_diameter']
        epsilon = self.params['nozzle_trans_param']
        nozzle = make_nozzle(r1,r2,h,epsilon)
        nozzle = Rotate(nozzle,a=90,v=[0,1,0])
        self.nozzle_tx = -self.params['fluid_housing_length'] - 0.5*h - self.hydrofoil_x/2
        self.nozzle_tz = -self.hydrofoil_tz - self.hydrofoil_z/2 - self.params['body_diameter']/2
        nozzle = Translate(nozzle,v=[self.nozzle_tx,0,self.nozzle_tz])
        self.parts['nozzle'] = nozzle

    def __make_anterior_cap(self):
        r = 0.5*self.params['body_diameter']
        h = self.params['anterior_cap_length']
        cap = bullet(r,h)
        cap = Rotate(cap,a=90,v=[0,1,0])
        self.anterior_cap_tx = self.params['motor_housing_length'] - self.hydrofoil_x/2
        self.anterior_cap_tz = self.nozzle_tz
        cap = Translate(cap,v=[self.anterior_cap_tx,0,self.anterior_cap_tz])
        self.parts['anterior_cap'] = cap

    def __make_fluid_housing(self):
        r = 0.5*self.params['body_diameter']
        h = self.params['fluid_housing_length']
        fuild_housing = Cylinder(r1=r, r2=r, h=h)
        fuild_housing = Rotate(fuild_housing,a=90,v=[0,1,0])
        self.fluid_housing_tx = -h/2 - self.hydrofoil_x/2
        self.fluid_housing_tz = self.nozzle_tz
        fuild_housing = Translate(fuild_housing,v=[self.fluid_housing_tx,0,self.fluid_housing_tz])
        self.parts['fuild_housing'] = fuild_housing

    def __make_motor_housing(self):
        r = 0.5*self.params['body_diameter']
        h = self.params['motor_housing_length']
        motor_housing = Cylinder(r1=r, r2=r, h=h)
        motor_housing = Rotate(motor_housing,a=90,v=[0,1,0])
        self.motor_housing_tx = h/2 - self.hydrofoil_x/2
        self.motor_housing_tz = self.nozzle_tz
        motor_housing = Translate(motor_housing,v=[self.motor_housing_tx,0,self.motor_housing_tz])
        self.parts['motor_housing'] = motor_housing

    def get_assembly(self):
        # Create union of all parts
        sub = Union(self.parts.values())
        # Shift so that sub is centered w.r.t to hydrofoil
        # x_shift = -0.5*self.params['hydrofoil_length']
        # sub = Translate(sub,v=[x_shift,0,0])
        # Shidt so that top of hydrofoil is at z=0
        # z_shift = -0.5*self.params['body_diameter'] - self.params['hydrofoil_height']
        sub_tz = -self.params['mount_plate_thickness']/2
        sub = Translate(sub,v=[0,0,sub_tz])
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
