from __future__ import division
from py2scad import *
from params import params
import water_channel
import sled_assembly_model

class WaterChannelAssembly(object):
    """
    Creates a model of the water channel assembly.
    """

    def __init__(self,params):
        self.params = params
        self.__make_assembly()

    def __make_assembly(self):
        """
        Creates the water channel assembly
        """
        self.parts = {}

        # Create water channel
        self.parts['water_channel'] = water_channel.WaterChannel(self.params).get_assembly()
        # self.water_channel = water_channel.WaterChannel(self.params).get_assembly()
        # self.water_channel = Translate(self.water_channel,v=[0,0,0])
        # self.parts['water_channel'] = self.water_channel

        # Create sled assembly
        self.parts['sled_assembly_model'] = sled_assembly_model.Sled_Assembly_Model(self.params).get_assembly()
        # self.sled_assembly = sled_assembly.Sled_Assembly(self.params).get_assembly()
        # self.sled_assembly = Translate(self.sled_assembly,v=[0,0,0])
        # self.parts['sled_assembly'] = self.sled_assembly

    def get_assembly(self):
        """
        Returns water_channel assembly
        """
        return Union(self.parts.values())

# ---------------------------------------------------------------------
if __name__ == '__main__':
    water_channel_assembly = WaterChannelAssembly(params).get_assembly()
    prog = SCAD_Prog()
    prog.fn = 50
    prog.add(water_channel_assembly)
    prog.write('water_channel_assembly.scad')



