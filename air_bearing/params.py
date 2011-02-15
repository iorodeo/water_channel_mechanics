
sub_model_params = { 
        'body_diameter'        : 6.00,
        'fluid_housing_length' : 10.63,
        'motor_housing_length' : 11.00, 
        'anterior_cap_length'  : 7.50,
        'nozzle_length'        : 11.13,
        'nozzle_exit_diameter' : 2.00,
        'nozzle_trans_param'   : 0.33,
        'hydrofoil_height'     : 14.50,
        'hydrofoil_length'     : 5.0,
        'hydrofoil_width'      : 1.0,
        }

params= {
        # Parameters for air bearing
        'bearing_type'               : 'RAB6',
        'slide_travel'               : 4,
        'slide_color'                : [0.2,0.9,0.2,1.0],
        'carriage_color'             : [0.1,0.5,0.5,1.0],
        'bearing_mount_color'        : [0.3,0.3,0.3,1.0],
        # Parameters for crossbeam
        'crossbeam_profile'          : '2040',
        'crossbeam_length'           : 5.0*12.0,
        # Parameters for mounting plates
        'mount_plate_thickness'      : 0.5,
        'mount_plate_x_overhang'     : 1.0,
        'mount_plate_y_overhang'     : 0.5,
        'mount2crossbeam_hole_inset' : 0.75,
        'mount2crossbeam_hole_size'  : 0.25,
        'mount_leveling_hole_size'   : 0.5,
        'mount_leveling_hole_inset'  : 0.5,
        'mount_plate_assembly_gap'   : 1.0,
        'sub_model_params'           : sub_model_params,
        }

