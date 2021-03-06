from __future__ import division
import air_bearing_rab
import extruded_profile
from py2scad import *
from params import params

class Bearing_Mount(object):
    """
    Creates a plate for mounting the RAB air bearing.
    """

    def __init__(self,params):
        self.params = params
        self.parts = {}
        self.__make_bottom_plate()
        self.__make_top_plate()

#    def __make_mount(self):
#        """
#        Create the bearing mount.
#        """
#        # Get parametes
#        bearing_type = self.params['bearing_type']
#        beam_profile = self.params['extruded_profile_profile']
#        bearing_params = air_bearing_rab.bearing_params[bearing_type]
#        beam_params = extruded_profile.profile_data[beam_profile]
#
#        # Create plate
#        x_overhang = self.params['bearing_mount_plate_x_overhang']
#        y_overhang = self.params['bearing_mount_plate_y_overhang']
#        length = bearing_params['carriage_length'] + 2*x_overhang
#        width = bearing_params['carriage_width'] + 2*y_overhang
#        thickness = self.params['bearing_mount_plate_thickness']
#        part = Cube(size=[length,width,thickness])
#
#        # Create bearing mount holes
#        radius = 0.5*bearing_params['carriage_screw_size']
#        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
#        hole_list = []
#        for i in (-1,1):
#            for j in (-1,1):
#                xpos = i*0.5*bearing_params['carriage_screw_dL']
#                ypos = j*0.5*bearing_params['carriage_screw_dW']
#                hole = Translate(base_hole,v=[xpos,ypos,0])
#                hole_list.append(hole)
#
#        # Remove hole material
#        part = Difference([part] + hole_list)
#
#        # Create beam mount holes
#        radius = 0.5*self.params['bearing_mount_to_extruded_profile_hole_size']
#        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
#        hole_list = []
#        for xpos in beam_params['slot_ypos']:
#            for j in (-1,1):
#                ypos = j*(0.5*width - self.params['bearing_mount_to_extruded_profile_hole_inset'])
#                hole = Translate(base_hole,v=[xpos,ypos,0])
#                hole_list.append(hole)
#
#        # Remove hole material
#        part = Difference([part] + hole_list)
#        self.part = part

    def __make_top_plate(self):

        # Get parametes
        bearing_type = self.params['bearing_type']
        beam_profile = self.params['bearing_mount_beam_profile']
        bearing_params = air_bearing_rab.bearing_params[bearing_type]
        beam_params = extruded_profile.profile_data[beam_profile]

        # Create plate
        x_overhang = self.params['bearing_mount_plate_x_overhang']
        y_overhang = self.params['bearing_mount_plate_y_overhang']
        length = bearing_params['carriage_length'] + 2*x_overhang
        width = bearing_params['carriage_width'] + 2*y_overhang
        thickness = self.params['bearing_mount_plate_thickness']
        top_plate = Cube(size=[length,width,thickness])

        # Create beam mount holes
        radius = 0.5*self.params['bearing_mount_plate_to_beam_hole_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        hole_list = []
        for xpos in beam_params['slot_ypos']:
            for j in (-1,1):
                ypos = j*(0.5*width - self.params['bearing_mount_plate_to_beam_hole_inset'])
                hole = Translate(base_hole,v=[xpos,ypos,0])
                hole_list.append(hole)

        # Remove hole material
        top_plate = Difference([top_plate] + hole_list)

        # Create leveling holes
        radius = 0.5*self.params['bearing_mount_plate_leveling_hole_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        dx = 0.5*length - self.params['bearing_mount_plate_leveling_hole_inset']
        dy = 0.5*width - self.params['bearing_mount_plate_leveling_hole_inset']
        pos_list = [(dx,0),(-dx,dy), (-dx,-dy)]
        hole_list = []
        for xpos,ypos in pos_list:
            hole = Translate(base_hole,v= [xpos,ypos,0])
            hole_list.append(hole)

        # Remove hole material
        top_plate = Difference([top_plate] + hole_list)
        self.parts['top_plate'] = top_plate

    def __make_bottom_plate(self):

        # Get parametes
        bearing_type = self.params['bearing_type']
        beam_profile = self.params['bearing_mount_beam_profile']
        bearing_params = air_bearing_rab.bearing_params[bearing_type]
        beam_params = extruded_profile.profile_data[beam_profile]

        # Create plate
        x_overhang = self.params['bearing_mount_plate_x_overhang']
        y_overhang = self.params['bearing_mount_plate_y_overhang']
        length = bearing_params['carriage_length'] + 2*x_overhang
        width = bearing_params['carriage_width'] + 2*y_overhang
        thickness = self.params['bearing_mount_plate_thickness']
        bottom_plate = Cube(size=[length,width,thickness])

        # Create bearing mount holes
        radius = 0.5*bearing_params['carriage_screw_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                xpos = i*0.5*bearing_params['carriage_screw_dL']
                ypos = j*0.5*bearing_params['carriage_screw_dW']
                hole = Translate(base_hole,v=[xpos,ypos,0])
                hole_list.append(hole)

        # Remove hole material
        bottom_plate = Difference([bottom_plate] + hole_list)
        self.parts['bottom_plate'] = bottom_plate

        # Create leveling holes
        radius = 0.5*self.params['bearing_mount_plate_leveling_hole_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        dx = 0.5*length - self.params['bearing_mount_plate_leveling_hole_inset']
        dy = 0.5*width - self.params['bearing_mount_plate_leveling_hole_inset']
        pos_list = [(dx,0),(-dx,dy), (-dx,-dy)]
        hole_list = []
        for xpos,ypos in pos_list:
            hole = Translate(base_hole,v= [xpos,ypos,0])
            hole_list.append(hole)

        # Remove hole material
        bottom_plate = Difference([bottom_plate] + hole_list)
        self.parts['bottom_plate'] = bottom_plate

    def get_top_plate(self,color=None):
        return self.parts['top_plate']

    def get_bottom_plate(self,color=None):
        return self.parts['bottom_plate']

    def get_assembly(self,color=None):
        """
        Returns assembly of parts
        """
        # Get parts
        top_plate = self.parts['top_plate']
        bottom_plate = self.parts['bottom_plate']
        # Tranlslate plates into position
        thickness = self.params['bearing_mount_plate_thickness']
        gap = self.params['bearing_mount_plate_assembly_gap']
        tz = (thickness + gap)/2
        top_plate = Translate(top_plate,v=[0,0,tz])
        bottom_plate = Translate(bottom_plate,v=[0,0,-tz])
        # Create assembly list and add color if specified
        assembly =  [top_plate, bottom_plate]
        if not color is None:
            assembly_w_color = []
            for part in assembly:
                part = Color(part,rgba=color)
                assembly_w_color.append(part)
            assembly = assembly_w_color
        return assembly





# -----------------------------------------------------------------------------
if __name__ == '__main__':

    bearing_mount = Bearing_Mount(params)
    assembly = bearing_mount.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write('air_bearing_rab_mount.scad')
