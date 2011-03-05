"""

"""
from __future__ import division
from py2scad import *
import extruded_profile
from params import params

class Sled_Assembly_Motorized(object):

    def __init__(self,params):
        self.params = params
        self.__make_assembly()

    def __make_assembly(self):

        self.parts = {}

        # Create pillowblocks
        pillowblock_profile = params['pillowblock_profile']
        pillowblock_length = params['pillowblock_length']
        pillowblock_mount_plate_length = params['pillowblock_mount_plate_length']
        pillowblock = extruded_profile.extruded_profile(pillowblock_profile,pillowblock_length)
        pillowblock = Color(pillowblock,params['pillowblock_color'])
        pillowblock = Rotate(pillowblock,a=90,v=[1,0,0])
        pillowblock = Rotate(pillowblock,a=90,v=[0,0,1])
        px = params['sled_assembly_motorized_length']/2 - params['pillowblock_mount_plate_length']/2
        py = params['water_channel_rail_rail_distance']/2
        pillowblock_1 = Translate(pillowblock,v=[px,py,0])
        self.parts['pillowblock_1'] = pillowblock_1
        pillowblock_2 = Translate(pillowblock,v=[-px,py,0])
        self.parts['pillowblock_2'] = pillowblock_2
        pillowblock_3 = Translate(pillowblock,v=[px,-py,0])
        self.parts['pillowblock_3'] = pillowblock_3
        pillowblock_4 = Translate(pillowblock,v=[-px,-py,0])
        self.parts['pillowblock_4'] = pillowblock_4

        # Create pillowblock mount plates
        pillowblock_mount_x = params['pillowblock_mount_plate_length']
        pillowblock_mount_y = pillowblock_mount_x
        pillowblock_mount_z = params['pillowblock_mount_plate_thickness']
        pillowblock_mount = Cube(size=[pillowblock_mount_x,pillowblock_mount_y,pillowblock_mount_z])
        pillowblock_mount = Color(pillowblock_mount,params['pillowblock_mount_plate_color'])
        pillowblock_mount_tz = params['pillowblock_mount_face_tz'] + pillowblock_mount_z/2
        pillowblock_mount_1 = Translate(pillowblock_mount,v=[px,py,pillowblock_mount_tz])
        self.parts['pillowblock_mount_1'] = pillowblock_mount_1
        pillowblock_mount_2 = Translate(pillowblock_mount,v=[-px,py,pillowblock_mount_tz])
        self.parts['pillowblock_mount_2'] = pillowblock_mount_2
        pillowblock_mount_3 = Translate(pillowblock_mount,v=[px,-py,pillowblock_mount_tz])
        self.parts['pillowblock_mount_3'] = pillowblock_mount_3
        pillowblock_mount_4 = Translate(pillowblock_mount,v=[-px,-py,pillowblock_mount_tz])
        self.parts['pillowblock_mount_4'] = pillowblock_mount_4

        # Create horizontal plate
        plate_horizontal_x = params['sled_assembly_motorized_length']
        plate_horizontal_y = params['sled_assembly_motorized_width']
        plate_horizontal_z = params['sled_assembly_motorized_plate_thickness']
        plate_horizontal = Cube(size=[plate_horizontal_x,plate_horizontal_y,plate_horizontal_z])
        pillowblock_mount_face_tz = params['pillowblock_mount_face_tz']
        pillowblock_mount_plate_thickness = params['pillowblock_mount_plate_thickness']
        plate_horizontal_tz = pillowblock_mount_face_tz + pillowblock_mount_plate_thickness + plate_horizontal_z/2
        plate_horizontal = Translate(plate_horizontal,v=[0,0,plate_horizontal_tz])
        plate_horizontal = Color(plate_horizontal,params['sled_assembly_motorized_color'])
        self.parts['plate_horizontal'] = plate_horizontal

        # Create vertical x plates
        x_plate_vertical_x = params['sled_assembly_motorized_length']
        x_plate_vertical_y = params['sled_assembly_motorized_plate_thickness']
        x_plate_vertical_z = params['sled_assembly_motorized_height'] - params['sled_assembly_motorized_plate_thickness']
        x_plate_vertical = Cube(size=[x_plate_vertical_x,x_plate_vertical_y,x_plate_vertical_z])
        x_plate_vertical_tz = plate_horizontal_tz + plate_horizontal_z/2 + x_plate_vertical_z/2
        x_plate_vertical = Translate(x_plate_vertical,v=[0,0,x_plate_vertical_tz])
        x_plate_vertical_ty = plate_horizontal_y/2 - x_plate_vertical_y/2
        x_plate_vertical = Color(x_plate_vertical,params['sled_assembly_motorized_color'])
        x_plate_vertical_1 = Translate(x_plate_vertical,v=[0,x_plate_vertical_ty,0])
        self.parts['x_plate_vertical_1'] = x_plate_vertical_1
        x_plate_vertical_2 = Translate(x_plate_vertical,v=[0,-x_plate_vertical_ty,0])
        self.parts['x_plate_vertical_2'] = x_plate_vertical_2

        # Create vertical y plates
        y_plate_vertical_x = params['sled_assembly_motorized_plate_thickness']
        y_plate_vertical_y = plate_horizontal_y - x_plate_vertical_y*2
        y_plate_vertical_z = x_plate_vertical_z
        y_plate_vertical = Cube(size=[y_plate_vertical_x,y_plate_vertical_y,y_plate_vertical_z])
        y_plate_vertical_tz = x_plate_vertical_tz
        y_plate_vertical = Translate(y_plate_vertical,v=[0,0,y_plate_vertical_tz])
        y_plate_vertical_tx = plate_horizontal_x/2 - y_plate_vertical_x/2
        y_plate_vertical = Color(y_plate_vertical,params['sled_assembly_motorized_color'])
        y_plate_vertical_1 = Translate(y_plate_vertical,v=[y_plate_vertical_tx,0,0])
        self.parts['y_plate_vertical_1'] = y_plate_vertical_1
        y_plate_vertical_2 = Translate(y_plate_vertical,v=[-y_plate_vertical_tx,0,0])
        self.parts['y_plate_vertical_2'] = y_plate_vertical_2

    def get_assembly(self):
        # return self.parts.values()
        return Union(self.parts.values())


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    assembly_maker = Sled_Assembly_Motorized(params)
    assembly = assembly_maker.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write('sled_assembly_motorized.scad')
