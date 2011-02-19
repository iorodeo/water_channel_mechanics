from __future__ import division
from py2scad import *
from params import params

class WaterChannel(object):
    """
    Creates a model of the water channel.
    """

    def __init__(self,params):
        self.params = params
        self.parts = {}
        self.__make_rails()
        self.__make_tank()
        self.__make_water()

    def __make_rails(self):
        """
        Creates the water channel rails
        """
        rail_diameter = self.params['water_channel_rail_diameter']
        rail_rail_distance = self.params['water_channel_rail_rail_distance']
        rail_length = self.params['water_channel_rail_length']
        rail_color = self.params['water_channel_rail_color']

        rail_1 = Cylinder(r1=rail_diameter/2,r2=rail_diameter/2,h=rail_length)
        rail_1 = Rotate(rail_1,a=90,v=[0,1,0])
        rail_1 = Translate(rail_1,v=[0,rail_rail_distance/2,0])
        rail_1 = Color(rail_1,rail_color)

        rail_2 = Cylinder(r1=rail_diameter/2,r2=rail_diameter/2,h=rail_length)
        rail_2 = Rotate(rail_2,a=90,v=[0,1,0])
        rail_2 = Translate(rail_2,v=[0,-rail_rail_distance/2,0])
        rail_2 = Color(rail_2,rail_color)

        self.parts['rail_1'] = rail_1
        self.parts['rail_2'] = rail_2

    def __make_tank(self):
        """
        Creates the water channel tank
        """
        tank_length = self.params['water_channel_tank_length']
        tank_thickness = self.params['water_channel_tank_thickness']
        channel_depth = self.params['water_channel_channel_depth']
        channel_width = self.params['water_channel_channel_width']
        rail_tank_distance = self.params['water_channel_rail_tank_distance']
        tank_color = self.params['water_channel_tank_color']
        show_tank = self.params['water_channel_show_tank'].lower()
        # Make tank 2 times bigger in z direction, then cut in half
        channel = Cube(size=[tank_length*1.1,channel_width,channel_depth*2])
        tank = Cube(size=[tank_length,channel_width+tank_thickness*2,channel_depth*2+tank_thickness*2])
        tank = Difference([tank,channel])
        tank_half = Cube(size=[tank_length*1.1,(channel_width+tank_thickness*2)*1.1,(channel_depth+tank_thickness)*2])
        tank_half = Translate(tank_half,v=[0,0,channel_depth+tank_thickness])
        tank = Difference([tank,tank_half])
        tank = Translate(tank,v=[0,0,-rail_tank_distance])
        tank = Color(tank,tank_color)
        if show_tank == 'true':
            self.parts['tank'] = tank

    def __make_water(self):
        """
        Creates the water channel water
        """
        tank_length = self.params['water_channel_tank_length']
        channel_depth = self.params['water_channel_channel_depth']
        channel_width = self.params['water_channel_channel_width']
        rail_tank_distance = self.params['water_channel_rail_tank_distance']
        water_depth = self.params['water_channel_water_depth']
        water_color = self.params['water_channel_water_color']
        show_water = self.params['water_channel_show_water'].lower()
        water = Cube(size=[tank_length,channel_width,water_depth])
        water = Translate(water,v=[0,0,-water_depth/2-(channel_depth-water_depth)-rail_tank_distance])
        water = Color(water,water_color)
        if show_water == 'true':
            self.parts['water'] = water

    def get_assembly(self):
        """
        Returns water_channel parts assembly
        """
        return Union(self.parts.values())

# ---------------------------------------------------------------------
if __name__ == '__main__':
    water_channel = WaterChannel(params)
    part_assem = water_channel.get_assembly()
    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(part_assem)
    prog.write('water_channel.scad')



