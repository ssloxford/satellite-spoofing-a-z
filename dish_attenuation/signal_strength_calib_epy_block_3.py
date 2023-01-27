"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr
import pmt
import time


class blk(gr.sync_block):  # other base classes are basic_block, decim_block, interp_block
    """Embedded Python Block example - a simple multiply const"""

    def __init__(self, filename="", fmts=[], columns=[]):  # only default arguments here
        """arguments to this function show up as parameters in GRC"""
        self.vector_len = 2
        gr.sync_block.__init__(
            self,
            name='Value saver',   # will show up in GRC
            in_sig=[np.float32] * self.vector_len,
            out_sig=None
        )
        # if an attribute with the same name as a parameter is found,
        # a callback is registered (properties work, too).
        self.selectPortName = 'saveButton'
        self.message_port_register_in(pmt.intern(self.selectPortName))
        self.set_msg_handler(pmt.intern(self.selectPortName), self.handle_msg)

        self.fmts = fmts
        self.columns = columns
        self.last_values = np.zeros(self.vector_len)

        if(filename != ""):
            self.file = open(filename, "a")

    def handle_msg(self, msg):
        fmt = ("%s\t" + ("\t".join(self.fmts) + ("\t" if 0<len(self.fmts) else 0)) + ("%f\t"*self.vector_len) + "\n")
        self.file.write(fmt % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            *self.columns,
            *self.last_values)
        )

    def stop(self):
        self.file.close()

    def work(self, input_items, output_items):
        """example: multiply with constant"""
        self.last_values = [row[-1] for row in input_items]
        return len(input_items[0])
