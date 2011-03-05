from __future__ import division
from py2scad import *
from params import params
import water_channel
import sled_assembly_model
import sled_assembly_motorized

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

        # Create model sled assembly
        self.parts['sled_assembly_model'] = sled_assembly_model.Sled_Assembly_Model(self.params).get_assembly()

        # Create motorized sled assembly
        self.sled_assembly_motorized = sled_assembly_motorized.Sled_Assembly_Motorized(self.params).get_assembly()
        sled_assembly_model_length = params['sled_assembly_model_length']
        sled_assembly_motorized_length = params['sled_assembly_motorized_length']
        sled_sled_gap = params['sled_sled_gap']
        sled_assembly_motorized_tx = sled_assembly_model_length/2 + sled_assembly_motorized_length/2 + sled_sled_gap
        self.sled_assembly_motorized = Translate(self.sled_assembly_motorized,v=[sled_assembly_motorized_tx,0,0])
        self.parts['sled_assembly_motorized'] = self.sled_assembly_motorized

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



