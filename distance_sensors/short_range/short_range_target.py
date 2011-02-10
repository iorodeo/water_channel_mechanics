"""
Target design for short range laser sensor. The targe is essentially a right
angle bracket and is designed to be laser cut from acrylic.


Author: Will Dickson, IO Rodeo Inc.
"""
from py2scad import *

# Part parameters -------------------------------------------------------------
thickness = 6.0 # 6mm material thickness
tab_depth = 5.5 # 5mm
base_width = 5.0*INCH2MM
base_depth = 5.0*INCH2MM
face_width = 5.0*INCH2MM
face_height = 5.0*INCH2MM

# Output files ----------------------------------------------------------------
assembly_file = 'short_range_target_assembly.scad'
projection_file = 'short_range_target_projection.scad' 


# Design --------------------------------------------------------------------

# Define base-to-face tabs (pos, width, depth, tab_dir)
base2face_tabs = [
        (0.2, 0.5*INCH2MM,  tab_depth),
        (0.50, 0.5*INCH2MM, tab_depth),
        (0.8, 0.5*INCH2MM,  tab_depth),
        ]

# Define right angle supports
face_tabs = [ 
        (0.15, 0.5*INCH2MM, tab_depth),
        (0.85, 0.5*INCH2MM, tab_depth),
        ]

base_tabs =  [
        (0.2, 0.5*INCH2MM, tab_depth),
        (0.5, 0.5*INCH2MM, tab_depth),
        (0.8, 0.5*INCH2MM, tab_depth),
        ]

support_params = {
        'depth'     :  base_depth - 1.0*INCH2MM, 
        'height'    :  face_height - thickness, 
        'thickness' :  thickness, 
        'face_tabs' : face_tabs, 
        'base_tabs' : base_tabs, 
        }

support_list = [ 
        { 'pos':  2.0*INCH2MM, 'params': support_params},
        { 'pos': -2.0*INCH2MM, 'params': support_params}, 
        ]

# Define holes in base
hole_list  = []
for x in range(-2,3):
    for y in range(-2,3):
        if y > -2 and abs(x) == 2:
            continue
        else:
            hole = {
                    'plate'    : 'base', 
                    'type'     : 'round',
                    'size'     :  0.25*INCH2MM, 
                    'location' :  (x*INCH2MM,y*INCH2MM),
                    }
            hole_list.append(hole)

# Pack parameters for right angle bracket
params = {
        'base_width'         : base_width,
        'base_depth'         : base_depth,
        'base_thickness'     : thickness,
        'face_width'         : face_width,
        'face_height'        : face_height,
        'face_thickness'     : thickness,
        'base2face_tabs'     : base2face_tabs, 
        'base_tab_dir'       : '+',
        'supports'           : support_list,
        'hole_list'          : hole_list,
        }

# Create bracket, both assembly and projection
rt_bracket = Right_Angle_Bracket(params)
rt_bracket.make()
assembly = rt_bracket.get_assembly(explode=(0,0,0))
projection = rt_bracket.get_projection()


# -----------------------------------------------------------------------------
if __name__ == "__main__":

    # If module is called as main program write parts to file
    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write(assembly_file)
    
    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(projection)
    prog.write(projection_file)
