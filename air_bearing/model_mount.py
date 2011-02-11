import RAB
from py2scad import *
from params import params

class Model_Mount(object):
    """
    Creates an assembly for connecting the model to the RAB air bearing slide.
    """

    def __init__(self,params):
        self.params = params
        self.parts = {}
        self.__make_front_plate()
        self.__make_back_plate()
        self.__make_bottom_plate()

    def __make_front_plate(self):

        # Get parametes
        bearing_type = self.params['bearing_type']
        beam_profile = self.params['crossbeam_profile']
        bearing_params = RAB.bearing_params[bearing_type]
        beam_params = extruded_beam.profile_data[beam_profile]

        # Create plate
        x_overhang = self.params['mount_plate_x_overhang']
        y_overhang = self.params['mount_plate_y_overhang']
        length = bearing_params['carriage_length'] + 2*x_overhang
        width = bearing_params['carriage_width'] + 2*y_overhang
        thickness = self.params['mount_plate_thickness']
        top_plate = Cube(size=[length,width,thickness])

        # Create beam mount holes
        radius = 0.5*self.params['mount2crossbeam_hole_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        hole_list = []
        for xpos in beam_params['slot_ypos']:
            for j in (-1,1):
                ypos = j*(0.5*width - self.params['mount2crossbeam_hole_inset'])
                hole = Translate(base_hole,v=[xpos,ypos,0])
                hole_list.append(hole)

        # Remove hole material
        top_plate = Difference([top_plate] + hole_list)

        # Create leveling holes
        radius = 0.5*self.params['mount_leveling_hole_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        dx = 0.5*length - self.params['mount_leveling_hole_inset']
        dy = 0.5*width - self.params['mount_leveling_hole_inset']
        pos_list = [(dx,0),(-dx,dy), (-dx,-dy)]
        hole_list = []
        for xpos,ypos in pos_list:
            hole = Translate(base_hole,v= [xpos,ypos,0])
            hole_list.append(hole)

        # Remove hole material
        top_plate = Difference([top_plate] + hole_list)
        self.parts['top_plate'] = top_plate

    def __make_bottom_plate(self):

        # Get parametes
        bearing_type = self.params['bearing_type']
        beam_profile = self.params['crossbeam_profile']
        bearing_params = RAB.bearing_params[bearing_type]
        beam_params = extruded_beam.profile_data[beam_profile]

        # Create plate
        x_overhang = self.params['mount_plate_x_overhang']
        y_overhang = self.params['mount_plate_y_overhang']
        length = bearing_params['carriage_length'] + 2*x_overhang
        width = bearing_params['carriage_width'] + 2*y_overhang
        thickness = self.params['mount_plate_thickness']
        bottom_plate = Cube(size=[length,width,thickness])

        # Create bearing mount holes
        radius = 0.5*bearing_params['carriage_screw_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                xpos = i*0.5*bearing_params['carriage_screw_dL']
                ypos = j*0.5*bearing_params['carriage_screw_dW']
                hole = Translate(base_hole,v=[xpos,ypos,0])
                hole_list.append(hole)

        # Remove hole material
        bottom_plate = Difference([bottom_plate] + hole_list)
        self.parts['bottom_plate'] = bottom_plate

        # Create leveling holes
        radius = 0.5*self.params['mount_leveling_hole_size']
        base_hole = Cylinder(r1=radius,r2=radius,h=2*thickness)
        dx = 0.5*length - self.params['mount_leveling_hole_inset']
        dy = 0.5*width - self.params['mount_leveling_hole_inset']
        pos_list = [(dx,0),(-dx,dy), (-dx,-dy)]
        hole_list = []
        for xpos,ypos in pos_list:
            hole = Translate(base_hole,v= [xpos,ypos,0])
            hole_list.append(hole)

        # Remove hole material
        bottom_plate = Difference([bottom_plate] + hole_list)
        self.parts['bottom_plate'] = bottom_plate

    def get_top_plate(self,color=None):
        return self.parts['top_plate']

    def get_bottom_plate(self,color=None):
        return self.parts['bottom_plate']

    def get_assembly(self,color=None):
        """
        Returns assembly of parts
        """
        # Get parts
        top_plate = self.parts['top_plate']
        bottom_plate = self.parts['bottom_plate']
        # Tranlslate top plate into position
        thickness = self.params['mount_plate_thickness']
        gap = self.params['mount_plate_assembly_gap']
        top_plate = Translate(top_plate,v=[0,0,thickness+gap])
        # Create assembly list and add color if specified
        assembly =  [top_plate, bottom_plate]
        if not color is None:
            assembly_w_color = []
            for part in assembly:
                part = Color(part,rgba=color)
                assembly_w_color.append(part)
            assembly = assembly_w_color
        return assembly





# -----------------------------------------------------------------------------
if __name__ == '__main__':

    mount = Bearing_Mount(params)
    assembly = mount.get_assembly()

    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(assembly)
    prog.write('bearing_mount.scad')
