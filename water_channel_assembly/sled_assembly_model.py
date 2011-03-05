"""

"""
from __future__ import division
from py2scad import *
import air_bearing_rab
import air_bearing_rab_mount
import extruded_profile
import sub_model
from params import params

class Sled_Assembly_Model(object):

    def __init__(self,params):
        self.params = params
        self.__make_assembly()
        self.__make_sub_model()

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
        px = params['sled_assembly_model_length']/2 - params['pillowblock_mount_plate_length']/2
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

        # Create y beams
        y_beam_x = params['sled_assembly_model_y_beam_width']
        y_beam_y = params['sled_assembly_model_width']
        y_beam_z = params['sled_assembly_model_y_beam_height']
        y_beam = Cube(size=[y_beam_x,y_beam_y,y_beam_z])
        y_beam_thickness = params['sled_assembly_model_y_beam_thickness']
        y_beam_void_x = y_beam_x - y_beam_thickness*2
        y_beam_void_y = y_beam_y + y_beam_thickness*2
        y_beam_void_z = y_beam_z - y_beam_thickness*2
        y_beam_void = Cube(size=[y_beam_void_x,y_beam_void_y,y_beam_void_z])
        y_beam = Difference([y_beam,y_beam_void])
        y_beam = Color(y_beam,params['sled_assembly_model_color'])
        y_beam_tx = params['sled_assembly_model_length']/2 - params['sled_assembly_model_y_beam_width']/2
        y_beam_tz = params['pillowblock_mount_face_tz'] + params['pillowblock_mount_plate_thickness'] + y_beam_z/2
        y_beam_1 = Translate(y_beam,v=[y_beam_tx,0,y_beam_tz])
        self.parts['y_beam_1'] = y_beam_1
        y_beam_2 = Translate(y_beam,v=[-y_beam_tx,0,y_beam_tz])
        self.parts['y_beam_2'] = y_beam_2

        # Create bearing mount beam
        profile = self.params['bearing_mount_beam_profile']
        profile_data = extruded_profile.profile_data[profile]
        length = self.params['bearing_mount_beam_length']
        color = self.params['bearing_mount_beam_color']
        bearing_mount_beam = extruded_profile.extruded_profile(profile,length,color)

        # Rotate and Traslate cross beam into position
        # bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[0,0,1])
        # bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[1,0,0])
        bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[0,1,0])
        bearing_mount_beam_thickness = profile_data['dx']
        # z_shift = 0.5*bearing_mount_beam_thickness + 2*bearing_mount_thickness + bearing_mount_gap
        bearing_mount_beam_tz = params['bearing_mount_beam_tz']
        bearing_mount_beam = Translate(bearing_mount_beam,v=[0,0,bearing_mount_beam_tz])
        self.parts['bearing_mount_beam'] = bearing_mount_beam

        # Create air bearing mount plates and rotate it to match the bearing_mount_beam
        bearing_mount_maker = air_bearing_rab_mount.Bearing_Mount(params=params)
        bearing_mount = bearing_mount_maker.get_assembly(color=self.params['bearing_mount_plate_color'])
        bearing_mount = Rotate(bearing_mount,a=90,v=[0,0,1])

        # Translate bearing mount into position
        bearing_mount_thickness = params['bearing_mount_plate_thickness']
        bearing_mount_gap = params['bearing_mount_plate_assembly_gap']
        bearing_mount_tz = bearing_mount_beam_tz - (bearing_mount_thickness + bearing_mount_gap/2) - bearing_mount_beam_thickness/2
        bearing_mount = Translate(bearing_mount,v=[0,0,bearing_mount_tz])
        self.parts['bearing_mount'] = bearing_mount

        # Create air bearing
        bearing_type = self.params['bearing_type']
        slide_travel = self.params['bearing_slide_travel']
        slide_color = self.params['bearing_slide_color']
        carriage_color = self.params['bearing_carriage_color']
        bearing_params = air_bearing_rab.bearing_params[bearing_type]
        air_bearing_maker = air_bearing_rab.RAB(bearing_type,
                                                slide_travel,
                                                slide_color = slide_color,
                                                carriage_color = carriage_color
                                                )
        air_bearing = air_bearing_maker.get_assembly()

        # Translate air bearing to mate with the bearing mount
        air_bearing_carriage_height = bearing_params['carriage_height']
        air_bearing_tz = bearing_mount_tz - (bearing_mount_thickness + bearing_mount_gap/2) - air_bearing_carriage_height/2
        air_bearing = Translate(air_bearing,v=[0,0,air_bearing_tz])
        self.parts['air_bearing'] = air_bearing

        # Create horizontal model mount plate
        sub_params = self.params['sub_model_params']
        model_mount_plate_horizontal_x = bearing_params['slide_base_length'] + slide_travel - 2*bearing_params['slide_screw_inset'] - params['model_mount_plate_thickness']
        model_mount_plate_horizontal_y = sub_params['mount_plate_length']
        self.model_mount_plate_horizontal_z = params['model_mount_plate_thickness']
        model_mount_plate_horizontal = Cube(size=[model_mount_plate_horizontal_x,model_mount_plate_horizontal_y,self.model_mount_plate_horizontal_z])
        self.model_mount_plate_horizontal_tz = air_bearing_tz - bearing_params['carriage_height']/2 - self.model_mount_plate_horizontal_z/2 - params['model_mount_plate_bearing_offset']
        model_mount_plate_horizontal = Translate(model_mount_plate_horizontal,v=[0,0,self.model_mount_plate_horizontal_tz])
        self.parts['model_mount_plate_horizontal'] = model_mount_plate_horizontal

        # Create vertical model mount plates
        model_mount_plate_vertical_x = params['model_mount_plate_thickness']

    def __make_sub_model(self):
        sub_params = self.params['sub_model_params']
        sub = sub_model.SubModel(params=sub_params)
        sub_assem = sub.get_assembly()
        bearing_type = self.params['bearing_type']
        bearing_params = air_bearing_rab.bearing_params[bearing_type]
        # sub_tz = -bearing_params['carriage_height'] - 3
        sub_tz = self.model_mount_plate_horizontal_tz - self.model_mount_plate_horizontal_z/2
        sub_assem = Translate(sub_assem,v=[0,0,sub_tz])
        self.parts['sub_model'] = sub_assem


    def get_assembly(self):
        # return self.parts.values()
        return Union(self.parts.values())


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    assembly_maker = Sled_Assembly_Model(params)
    assembly = assembly_maker.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write('sled_assembly_model.scad')
