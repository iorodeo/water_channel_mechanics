"""
Module for creating extruded parts with dxf profiles.
"""
from __future__ import division
from py2scad import *
from params import params

# Data for profiles
profile2dxf= {
        '1010'            : 'profiles/1010.dxf',
        '1020'            : 'profiles/1020.dxf',
        '1030'            : 'profiles/1030.dxf',
        '2040'            : 'profiles/2040.dxf',
        '1545'            : 'profiles/1545.dxf',
        '3030'            : 'profiles/3030.dxf',
        '3060'            : 'profiles/3060.dxf',
        'pillowblock'     : 'profiles/pillowblock.dxf',
        'rectangulartube' : 'profiles/rectangulartube.dxf',
        }

data_1010 = {
        'dx' : 1.0,
        'dy' : 1.0,
        'slot_xpos' : (0.0,),
        'slot_ypos' : (0.0,),
        }

data_1020 = {
        'dx' : 1.0,
        'dy' : 2.0,
        'slot_xpos' : (0.0,),
        'slot_ypos' : (-0.5,0.5),
        }

data_1030 = {
        'dx' : 1.0,
        'dy' : 3.0,
        'slot_xpos' : (0.0,),
        'slot_ypos' : (-1.0, 0.0, 1.0),
        }

data_2040 = {
        'dx' : 2.0,
        'dy' : 4.0,
        'slot_xpos' : (-0.5, 0.5),
        'slot_ypos' : (-1.5, -0.5, 0.5, 1.5),
        }

data_1545 = {
        'dx' : 1.5,
        'dy' : 4.5,
        'slot_xpos' : (0,),
        'slot_ypos' : (-1.5, 0.0, 1.5),
        }

data_3030 = {
        'dx' : 3.0,
        'dy' : 3.0,
        'slot_xpos' : (-0.75, 0.75),
        'slot_ypos' : (-0.75, 0.75),
        }

data_3060 = {
        'dx' : 3.0,
        'dy' : 6.0,
        'slot_xpos' : (-0.75, 0.75),
        'slot_ypos' : (-2.25, -0.75, 0.75, 2.25),
        }

data_pillowblock = {
        'dx' : 4.75,
        'dy' : 2.3,
        }

data_rectangulartube = {
        'dx' : 2.0,
        'dy' : 5.0,
        }

profile_data = {
        '1010'            : data_1010,
        '1020'            : data_1020,
        '1030'            : data_1030,
        '2040'            : data_2040,
        '1545'            : data_1545,
        '3030'            : data_3030,
        '3060'            : data_3060,
        'pillowblock'     : data_pillowblock,
        'rectangulartube' : data_rectangulartube,
        }

def extruded_profile(profile,length_in,color=None):
    """
    Creates an extruded profile with the given profile and length.

    Note, units are in inches.
    """
    dxf_file = profile2dxf[profile]
    part = Linear_DXF_Extrude(dxf_file,height=length_in)
    if not color is None:
        part = Color(part,rgba=color)
    return part


# ------------------------------------------------------------
if __name__ == '__main__':

    # Create part
    # profile = params['bearing_mount_beam_profile']
    # length = params['bearing_mount_beam_length']
    profile = params['pillowblock_profile']
    length = params['pillowblock_length']
    part = extruded_profile(profile,length)
    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(part)
    prog.write('extruded_profile.scad')




