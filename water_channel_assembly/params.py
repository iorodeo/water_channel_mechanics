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
        'bearing_type'           : 'RAB6',
        'bearing_slide_travel'   : 4,
        'bearing_slide_color'    : [0.2,0.9,0.2,1.0],
        'bearing_carriage_color' : [0.1,0.5,0.5,1.0],
        # Parameters for rab air bearing mount plates
        'bearing_mount_plate_color'               : [0.3,0.3,0.3,1.0],
        'bearing_mount_plate_thickness'           : 0.5,
        'bearing_mount_plate_x_overhang'          : 1.0,
        'bearing_mount_plate_y_overhang'          : 0.5,
        'bearing_mount_plate_to_beam_hole_inset'  : 0.75,
        'bearing_mount_plate_to_beam_hole_size'   : 0.25,
        'bearing_mount_plate_leveling_hole_size'  : 0.5,
        'bearing_mount_plate_leveling_hole_inset' : 0.5,
        'bearing_mount_plate_assembly_gap'        : 0.1,
        # Parameters for bearing mount beam
        'bearing_mount_beam_profile' : '2040',
        'bearing_mount_beam_length'  : 5.0*12.0,
        'bearing_mount_beam_color'   : [0.5,0.5,0.5,1.0],
        # Parameters for the water channel
        'water_channel_rail_diameter'      : 1.5,
        'water_channel_rail_rail_distance' : 49,
        'water_channel_rail_length'        : 1200,
        'water_channel_rail_tank_distance' : 4,
        'water_channel_rail_color'         : [0.5,0.5,0.5,1.0],
        'water_channel_tank_length'        : 1200,
        'water_channel_tank_thickness'     : 0.5,
        'water_channel_tank_color'         : [0.5,0.5,0.5,0.5],
        'water_channel_show_tank'          : 'true',
        'water_channel_channel_depth'      : 43,
        'water_channel_channel_width'      : 43,
        'water_channel_water_depth'        : 30,
        'water_channel_water_color'         : [0.0,0.0,1.0,0.25],
        'water_channel_show_water'         : 'true',
        # Additional assembly params
        'sub_model_params'           : sub_model_params,
        }

