"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
from gnuradio import qtgui


class blk(gr.sync_block):
    def __init__(self, strength = 0.01, gain = 0, agc_mode = 0, sweep_delay = 0, sweep_step = 1):
        gr.sync_block.__init__(self,
            name="AGC",
            in_sig=[np.float32],
            out_sig=None)

        self.agc_mode = agc_mode
        self.strength = strength

        self.gain = gain
        self.gain_block = None
        self.control = None

        self.portName = 'messageOutput'
        self.message_port_register_out(pmt.intern(self.portName))

        self.sweep_step = sweep_step
        self.sweep_delay = sweep_delay
        self.stage = 0
        self.counter = 0


    def setup(self, gain_block, control_block):
        self.gain_block = gain_block
        self.gain = self.gain_block.value()
        self.control = control_block

    def work(self, input_items, output_items):
        for i in range(len(input_items)):
            #Decrease gain
            if(self.agc_mode == 2):
                if(input_items[0][i] > 0.8):
                    self.gain -= self.strength
                if(input_items[0][i] > 0.7):
                    self.gain -= self.strength
                if(input_items[0][i] < 0.3):
                    self.gain += self.strength
                if(input_items[0][i] < 0.2):
                    self.gain += self.strength
                self.gain_block.setValue(int(self.gain))

        if(self.agc_mode == 1):
            if(input_items[0][-1] > 0.9 or self.gain > 70):
                self.control.setCurrentIndex(0)
                self.gain_block.setValue(0)
            else:
                self.counter += len(input_items)
                if (self.counter > self.sweep_delay and self.stage == 0):
                    PMT_msg = pmt.from_bool(True)
                    self.message_port_pub(pmt.intern(self.portName), PMT_msg)
                    self.counter = self.sweep_delay
                    self.stage = 1

                if (self.counter > self.sweep_delay*1.5 and self.stage == 1):
                    self.counter = 0
                    self.stage = 0

                    self.gain += self.sweep_step
                    self.gain_block.setValue(int(self.gain))
        else:
            self.counter = 0
            self.stage = 0

        return len(input_items[0])