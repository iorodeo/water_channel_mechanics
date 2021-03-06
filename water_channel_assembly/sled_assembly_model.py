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

        # Create y beams
        y_beam_profile = params['sled_assembly_model_y_beam_profile']
        y_beam_length = params['sled_assembly_model_width']
        y_beam = extruded_profile.extruded_profile(y_beam_profile,y_beam_length)
        sled_assembly_model_color = params['sled_assembly_model_color']
        y_beam = Color(y_beam,sled_assembly_model_color)
        y_beam = Rotate(y_beam,a=90,v=[0,0,1])
        y_beam = Rotate(y_beam,a=90,v=[1,0,0])
        y_beam_profile_data = extruded_profile.profile_data[y_beam_profile]
        y_beam_tx = params['sled_assembly_model_length']/2 - y_beam_profile_data['dy']/2
        y_beam_tz = params['pillowblock_mount_face_tz'] + params['pillowblock_mount_plate_thickness'] + y_beam_profile_data['dx']/2
        y_beam_1 = Translate(y_beam,v=[y_beam_tx,0,y_beam_tz])
        self.parts['y_beam_1'] = y_beam_1
        y_beam_2 = Translate(y_beam,v=[-y_beam_tx,0,y_beam_tz])
        self.parts['y_beam_2'] = y_beam_2

        # Create bearing mount beam
        bearing_mount_beam_profile = self.params['bearing_mount_beam_profile']
        bearing_mount_beam_profile_data = extruded_profile.profile_data[bearing_mount_beam_profile]
        bearing_mount_beam_length = params['sled_assembly_model_length'] - 2*y_beam_profile_data['dy']
        bearing_mount_beam_color = self.params['bearing_mount_beam_color']
        bearing_mount_beam = extruded_profile.extruded_profile(bearing_mount_beam_profile,bearing_mount_beam_length,bearing_mount_beam_color)

        # Rotate and Traslate cross beam into position
        # bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[0,0,1])
        # bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[1,0,0])
        bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[0,1,0])
        bearing_mount_beam_thickness = bearing_mount_beam_profile_data['dx']
        # z_shift = 0.5*bearing_mount_beam_thickness + 2*bearing_mount_thickness + bearing_mount_gap
        bearing_mount_beam_tz = y_beam_tz
        bearing_mount_beam = Translate(bearing_mount_beam,v=[0,0,bearing_mount_beam_tz])
        self.parts['bearing_mount_beam'] = bearing_mount_beam

        # Create pillowblocks
        pillowblock_profile = params['pillowblock_profile']
        pillowblock_length = params['pillowblock_length']
        pillowblock = extruded_profile.extruded_profile(pillowblock_profile,pillowblock_length)
        pillowblock = Color(pillowblock,params['pillowblock_color'])
        pillowblock = Rotate(pillowblock,a=90,v=[1,0,0])
        pillowblock = Rotate(pillowblock,a=90,v=[0,0,1])
        pillowblock_tx = params['sled_assembly_model_length']/2 - y_beam_profile_data['dy']/2
        pillowblock_ty = params['water_channel_rail_rail_distance']/2
        pillowblock_1 = Translate(pillowblock,v=[pillowblock_tx,pillowblock_ty,0])
        self.parts['pillowblock_1'] = pillowblock_1
        pillowblock_2 = Translate(pillowblock,v=[-pillowblock_tx,pillowblock_ty,0])
        self.parts['pillowblock_2'] = pillowblock_2
        pillowblock_3 = Translate(pillowblock,v=[pillowblock_tx,-pillowblock_ty,0])
        self.parts['pillowblock_3'] = pillowblock_3
        pillowblock_4 = Translate(pillowblock,v=[-pillowblock_tx,-pillowblock_ty,0])
        self.parts['pillowblock_4'] = pillowblock_4

        # Create pillowblock mount plates
        pillowblock_mount_x = y_beam_profile_data['dy'] + 2.0
        pillowblock_mount_y = params['pillowblock_mount_plate_width']
        pillowblock_mount_z = params['pillowblock_mount_plate_thickness']
        pillowblock_mount = Cube(size=[pillowblock_mount_x,pillowblock_mount_y,pillowblock_mount_z])
        pillowblock_mount = Color(pillowblock_mount,params['pillowblock_mount_plate_color'])
        pillowblock_mount_tz = params['pillowblock_mount_face_tz'] + pillowblock_mount_z/2
        pillowblock_mount_1 = Translate(pillowblock_mount,v=[pillowblock_tx,pillowblock_ty,pillowblock_mount_tz])
        self.parts['pillowblock_mount_1'] = pillowblock_mount_1
        pillowblock_mount_2 = Translate(pillowblock_mount,v=[-pillowblock_tx,pillowblock_ty,pillowblock_mount_tz])
        self.parts['pillowblock_mount_2'] = pillowblock_mount_2
        pillowblock_mount_3 = Translate(pillowblock_mount,v=[pillowblock_tx,-pillowblock_ty,pillowblock_mount_tz])
        self.parts['pillowblock_mount_3'] = pillowblock_mount_3
        pillowblock_mount_4 = Translate(pillowblock_mount,v=[-pillowblock_tx,-pillowblock_ty,pillowblock_mount_tz])
        self.parts['pillowblock_mount_4'] = pillowblock_mount_4

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
        self.bearing_params = air_bearing_rab.bearing_params[bearing_type]
        air_bearing_maker = air_bearing_rab.RAB(bearing_type,
                                                slide_travel,
                                                slide_color = slide_color,
                                                carriage_color = carriage_color
                                                )
        air_bearing = air_bearing_maker.get_assembly()

        # Translate air bearing to mate with the bearing mount
        air_bearing_carriage_height = self.bearing_params['carriage_height']
        self.air_bearing_tz = bearing_mount_tz - (bearing_mount_thickness + bearing_mount_gap/2) - air_bearing_carriage_height/2
        air_bearing = Translate(air_bearing,v=[0,0,self.air_bearing_tz])
        self.parts['air_bearing'] = air_bearing

        # Create horizontal model mount plate
        sub_params = self.params['sub_model_params']
        model_mount_plate_horizontal_x = self.bearing_params['slide_base_length'] + slide_travel - 2*self.bearing_params['slide_screw_inset'] - params['model_mount_plate_thickness'] + 2*params['model_mount_plate_horizontal_vertical_overlap']
        model_mount_plate_horizontal_y = sub_params['mount_plate_length']
        self.model_mount_plate_horizontal_z = params['model_mount_plate_thickness']
        model_mount_plate_horizontal = Cube(size=[model_mount_plate_horizontal_x,model_mount_plate_horizontal_y,self.model_mount_plate_horizontal_z])
        self.model_mount_plate_horizontal_tz = self.air_bearing_tz - self.bearing_params['carriage_height']/2 - params['model_mount_plate_bearing_offset'] - self.model_mount_plate_horizontal_z/2
        model_mount_plate_horizontal = Translate(model_mount_plate_horizontal,v=[0,0,self.model_mount_plate_horizontal_tz])
        model_mount_plate_horizontal = Color(model_mount_plate_horizontal,sled_assembly_model_color)
        self.parts['model_mount_plate_horizontal'] = model_mount_plate_horizontal

        # Create vertical model mount plates
        model_mount_plate_vertical_x = params['model_mount_plate_thickness']
        model_mount_plate_vertical_y = sub_params['mount_plate_length']
        model_mount_plate_vertical_z = abs(self.air_bearing_tz - self.model_mount_plate_horizontal_tz + params['model_mount_plate_vertical_underhang'])
        model_mount_plate_vertical = Cube(size=[model_mount_plate_vertical_x,model_mount_plate_vertical_y,model_mount_plate_vertical_z])
        model_mount_plate_vertical_tx = (self.bearing_params['slide_base_length'] + slide_travel - 2*self.bearing_params['slide_screw_inset'])/2
        model_mount_plate_vertical_tz = self.air_bearing_tz - model_mount_plate_vertical_z/2
        model_mount_plate_vertical = Color(model_mount_plate_vertical,sled_assembly_model_color)
        fit_clearance = params['model_mount_plate_fit_clearance']
        slide_negative_x = self.bearing_params['slide_base_length'] + slide_travel + fit_clearance
        slide_negative_y = self.bearing_params['slide_width'] + fit_clearance
        slide_negative_z = self.bearing_params['slide_height'] + fit_clearance/2
        slide_negative = Cube(size=[slide_negative_x,slide_negative_y,slide_negative_z])
        slide_negative = Translate(slide_negative,v=[0,0,self.air_bearing_tz])
        model_mount_plate_horizontal_negative = Cube(size=[(model_mount_plate_horizontal_x + fit_clearance),(model_mount_plate_horizontal_y + fit_clearance),(self.model_mount_plate_horizontal_z + fit_clearance)])
        model_mount_plate_horizontal_negative = Translate(model_mount_plate_horizontal_negative,v=[0,0,self.model_mount_plate_horizontal_tz])
        model_mount_plate_vertical_1 = Translate(model_mount_plate_vertical,v=[model_mount_plate_vertical_tx,0,model_mount_plate_vertical_tz])
        model_mount_plate_vertical_1 = Difference([model_mount_plate_vertical_1,slide_negative])
        model_mount_plate_vertical_1 = Difference([model_mount_plate_vertical_1,model_mount_plate_horizontal_negative])

        # model_mount_plate_vertical_1 = Translate(model_mount_plate_vertical_1,v=[1.0,0,0])

        model_mount_plate_vertical_1 = Color(model_mount_plate_vertical_1,sled_assembly_model_color)
        self.parts['model_mount_plate_vertical_1'] = model_mount_plate_vertical_1
        model_mount_plate_vertical_2 = Translate(model_mount_plate_vertical,v=[-model_mount_plate_vertical_tx,0,model_mount_plate_vertical_tz])
        model_mount_plate_vertical_2 = Difference([model_mount_plate_vertical_2,slide_negative])
        model_mount_plate_vertical_2 = Color(model_mount_plate_vertical_2,sled_assembly_model_color)
        self.parts['model_mount_plate_vertical_2'] = model_mount_plate_vertical_2

    def __make_sub_model(self):
        sub_params = self.params['sub_model_params']
        sub = sub_model.SubModel(params=sub_params)
        sub_assem = sub.get_assembly()
        bearing_type = self.params['bearing_type']
        # sub_tz = -self.bearing_params['carriage_height'] - 3
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
