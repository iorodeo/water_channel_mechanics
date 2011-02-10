"""

"""
from py2scad import *
import RAB
import bearing_mount
import extruded_beam
from params import params

class Mount_Assembly(object):

    def __init__(self,params):
        self.params = params
        self.__make_assembly()

    def __make_assembly(self):

        self.parts = {}

        # Create air bearing
        bearing_type = self.params['bearing_type']
        slide_travel = self.params['slide_travel']
        slide_color = self.params['slide_color']
        carriage_color = self.params['carriage_color']
        bearing_params = RAB.bearing_params[bearing_type]
        air_bearing_maker = RAB.RAB(
                bearing_type,
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
        mount_maker = bearing_mount.Bearing_Mount(params=params)
        mount = mount_maker.get_assembly(color=self.params['bearing_mount_color'])

        # Translate bearing mount into position
        mount_thickness = params['mount_plate_thickness']
        mount_gap = params['mount_plate_assembly_gap']
        mount = Translate(mount,v=[0,0,0.5*mount_thickness])
        self.parts['mount'] = mount

        # Create cross beam
        profile = self.params['crossbeam_profile']
        profile_data = extruded_beam.profile_data[profile]
        length = self.params['crossbeam_length']
        crossbeam = extruded_beam.extruded_beam(profile,length)

        # Rotate and Traslate cross beam into position
        crossbeam = Rotate(crossbeam,a=90,v=[0,0,1])
        crossbeam = Rotate(crossbeam,a=90,v=[1,0,0])
        profile_thickness = profile_data['dx']
        z_shift = 0.5*profile_thickness + 2*mount_thickness + mount_gap
        crossbeam = Translate(crossbeam,v=[0,0,z_shift])
        self.parts['crossbeam'] = crossbeam


    def get_assembly(self):
        return self.parts.values() 


# -----------------------------------------------------------------------------
if __name__ == '__main__':

    assembly_maker = Mount_Assembly(params)
    assembly = assembly_maker.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write('mount_assembly.scad')
