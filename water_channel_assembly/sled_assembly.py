"""

"""
from py2scad import *
import air_bearing_rab
import air_bearing_rab_mount
import extruded_beam
import sub_model
from params import params

class Sled_Assembly(object):

    def __init__(self,params):
        self.params = params
        self.__make_assembly()
        self.__make_sub_model()

    def __make_assembly(self):

        self.parts = {}

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

        # Translate air bearing so that top surface is at z=0
        carriage_height = bearing_params['carriage_height']
        air_bearing = Translate(air_bearing,v=[0,0,-0.5*carriage_height])
        self.parts['air_bearing'] = air_bearing

        # Create air bearing mount plate
        bearing_mount_maker = air_bearing_rab_mount.Bearing_Mount(params=params)
        bearing_mount = bearing_mount_maker.get_assembly(color=self.params['bearing_mount_plate_color'])

        # Translate bearing mount into position
        bearing_mount_thickness = params['bearing_mount_plate_thickness']
        bearing_mount_gap = params['bearing_mount_plate_assembly_gap']
        bearing_mount = Translate(bearing_mount,v=[0,0,0.5*bearing_mount_thickness])
        self.parts['bearing_mount'] = bearing_mount

        # Create cross beam
        profile = self.params['bearing_mount_beam_profile']
        profile_data = extruded_beam.profile_data[profile]
        length = self.params['bearing_mount_beam_length']
        bearing_mount_beam = extruded_beam.extruded_beam(profile,length)

        # Rotate and Traslate cross beam into position
        # bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[0,0,1])
        # bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[1,0,0])
        bearing_mount_beam = Rotate(bearing_mount_beam,a=90,v=[0,1,0])
        profile_thickness = profile_data['dx']
        z_shift = 0.5*profile_thickness + 2*bearing_mount_thickness + bearing_mount_gap
        bearing_mount_beam = Translate(bearing_mount_beam,v=[0,0,z_shift])
        self.parts['bearing_mount_beam'] = bearing_mount_beam

    def __make_sub_model(self):
        sub_params = self.params['sub_model_params']
        sub = sub_model.SubModel(params=sub_params)
        sub_assem = sub.get_assembly()
        bearing_type = self.params['bearing_type']
        bearing_params = air_bearing_rab.bearing_params[bearing_type]
        z_shift = -bearing_params['carriage_height'] - 3
        # z_shift = 0
        sub_assem = Translate(sub_assem,v=[0,0,z_shift])
        self.parts['sub_model'] = sub_assem


    def get_assembly(self):
        return self.parts.values()


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    assembly_maker = Sled_Assembly(params)
    assembly = assembly_maker.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write('sled_assembly.scad')
