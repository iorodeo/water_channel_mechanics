from py2scad import *
from params import params

class WaterChannel(object):
    """
    Creates a model of the water channel.
    """

    def __init__(self,bearing_type,slide_travel,slide_color=None,carriage_color=None):
        self.bearing_type = bearing_type
        self.params = bearing_params[bearing_type]
        self.params['bearing_slide_travel'] = slide_travel
        self.slide_color = slide_color
        self.carriage_color = carriage_color
        self.__make_slide()
        self.__make_carriage()
        self.__make_slide_travel()

    def set_slide_travel(self,val):
        self.params['bearing_slide_travel'] = val
        self.__make_slide()
        self.__make_carriage()
        self.__make_slide_travel()

    def __make_slide(self):
        """
        Creates the slide component of the RAB air bearing.
        """
        # Create base rectangle for slide
        length = self.params['slide_base_length'] + self.params['bearing_slide_travel']
        width = self.params['slide_width']
        height = self.params['slide_height']
        slide = Cube(size=[length,width,height])
        # Create the mounting holes
        radius = 0.5*self.params['slide_screw_size']
        base_hole = Cylinder(r1=radius, r2=radius, h=2*height)
        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                xpos = i*(0.5*length - self.params['slide_screw_inset'])
                ypos = j*(0.5*self.params['slide_screw_dW'])
                hole = Translate(base_hole,v=[xpos,ypos,0])
                hole_list.append(hole)
        # Remove hole material
        slide = Difference([slide] + hole_list)
        # Add color to slide if available
        if not self.slide_color is None:
            slide = Color(slide,rgba=self.slide_color)
        self.slide = slide

    def __make_carriage(self):
        """
        Creates the carriage component of the RAB air bearing.
        """
        # Create base rectangle
        length = self.params['carriage_length']
        width = self.params['carriage_width']
        height = self.params['carriage_height']
        carriage = Cube(size=[length, width, height])

        # Subtract slide from carraige
        slide_width = self.params['slide_width'] + 2*self.params['slide_tolerance']
        slide_height  = self.params['slide_height'] + 2*self.params['slide_tolerance']
        slide_cube = Cube(size=[2*length,slide_width,slide_height])
        carriage = Difference([carriage,slide_cube])

        # Create mounting holes
        radius = 0.5*self.params['carriage_screw_size']
        base_hole = Cylinder(r1=radius,r2=radius, h=2*height)
        hole_list = []
        for i in (-1,1):
            for j in (-1,1):
                xpos = i*0.5*self.params['carriage_screw_dL']
                ypos = j*0.5*self.params['carriage_screw_dW']
                hole = Translate(base_hole,v=[xpos,ypos,0])
                hole_list.append(hole)
        # Remove hole material
        carriage = Difference([carriage]+hole_list)
        # Add color to carriage is available
        if not self.carriage_color is None:
            carriage = Color(carriage,rgba=self.carriage_color)
        self.carriage = carriage

    def __make_slide_travel(self,color=[0,0,1,1]):
        """
        Make a colored region showing the slides travel.
        """
        length = self.params['carriage_width'] + self.params['bearing_slide_travel']
        width = self.params['slide_width'] + self.params['slide_tolerance']
        height = self.params['slide_height'] +  self.params['slide_tolerance']
        slide_travel = Cube(size=[length,width,height])
        self.slide_travel = Color(slide_travel,rgba=color)

    def get_assembly(self,show_slide_travel=False,color=None):
        """
        Returns air bearing parts assembly
        """
        assembly = [self.slide, self.carriage]
        if show_slide_travel == True:
            assembly.append(self.slide_travel)
        if not color is None:
            assembly_new = []
            for part in assembly:
                part = Color(part,rgba=color)
                assembly_new.append(part)
            assembly = assembly_new
        return assembly

    def get_slide(self):
        """
        Returns the air bearing slide
        """
        return self.slide

    def get_carriage(self):
        """
        Reurns the air bearing carriage
        """
        return self.carriage

# ---------------------------------------------------------------------
if __name__ == '__main__':

    bearing_type = params['bearing_type']
    slide_travel = params['bearing_slide_travel']

    bearing = RAB(bearing_type, slide_travel, slide_color=[0.3,0.3,1,1],carriage_color=[1.0,0.3,0.3,1])
    part_assem = bearing.get_assembly(show_slide_travel=True)
    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(part_assem)
    prog.write('air_bearing_rab.scad')



