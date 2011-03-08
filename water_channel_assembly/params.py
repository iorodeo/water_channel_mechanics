sub_model_params = {
        'body_diameter'         : 6.00,
        'fluid_housing_length'  : 10.63,
        'motor_housing_length'  : 11.00,
        'anterior_cap_length'   : 7.50,
        'nozzle_length'         : 11.13,
        'nozzle_exit_diameter'  : 2.00,
        'nozzle_trans_param'    : 0.33,
        'hydrofoil_height'      : 14.50,
        'hydrofoil_length'      : 5.0,
        'hydrofoil_width'       : 1.0,
        'mount_plate_length'    : 8.0,
        'mount_plate_thickness' : 0.25,
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
        'bearing_mount_beam_length'  : 35.75,
        'bearing_mount_beam_color'   : [0.5,0.5,0.5,1.0],
        'bearing_mount_beam_tz'      : 10.0,
        # Parameters for the water channel
        'water_channel_rail_diameter'       : 1.5,
        'water_channel_rail_rail_distance'  : 48.75,
        'water_channel_rail_length'         : 1200,
        'water_channel_rail_tank_distance'  : 1.75,
        'water_channel_rail_color'          : [0.5,0.5,0.5,1.0],
        'water_channel_tank_length'         : 1200,
        'water_channel_tank_thickness'      : 0.5,
        'water_channel_tank_color'          : [0.5,0.5,0.5,0.5],
        'water_channel_show_tank'           : 'true',
        'water_channel_channel_depth'       : 23.5,
        'water_channel_channel_width'       : 43.25,
        'water_channel_water_depth'         : 17.25,
        'water_channel_water_color'         : [0.0,0.0,1.0,0.25],
        'water_channel_show_water'          : 'true',
        # Parameters for the pillowblocks
        'pillowblock_color'                 : [1.0,1.0,0.0,1.0],
        'pillowblock_profile'               : 'pillowblock',
        'pillowblock_length'                : 3.75,
        'pillowblock_mount_face_tz'         : 1.75,
        'pillowblock_mount_plate_color'     : [0.3,0.3,0.3,1.0],
        'pillowblock_mount_plate_length'    : 5.0,
        'pillowblock_mount_plate_thickness' : 0.25,
        # Parameters for the model sled assembly
        'sled_assembly_model_color'            : [0.5,0.5,0.5,1.0],
        'sled_assembly_model_length'           : 35.75,
        'sled_assembly_model_width'            : 53.75,
        'sled_assembly_model_y_beam_width'     : 5.0,
        'sled_assembly_model_y_beam_height'    : 2.0,
        'sled_assembly_model_y_beam_thickness' : 0.125,
        # Parameters for the motorized sled assembly
        'sled_assembly_motorized_color'            : [0.7,0.7,0.7,1.0],
        'sled_assembly_motorized_length'           : 40,
        'sled_assembly_motorized_width'            : 53.375,
        'sled_assembly_motorized_height'           : 2.5,
        'sled_assembly_motorized_plate_thickness'  : 0.5,

        'sled_sled_gap' : 4.0,

        # Parameters for the model mount plates
        'model_mount_plate_thickness'                   : 0.5,
        'model_mount_plate_bearing_offset'              : 2.0,
        'model_mount_plate_horizontal_vertical_overlap' : 0.25,
        'model_mount_plate_vertical_underhang'          : 10.0,
        'model_mount_plate_fit_clearance'               : 0.015,

        # Additional assembly params
        'sub_model_params'           : sub_model_params,
        }

