"""
Embedded Python Blocks:

Each time this file is saved, GRC will instantiate the first class it finds
to get ports and parameters of your block. The arguments to __init__  will
be the parameters. All of them are required to have default values!
"""

import numpy as np
from gnuradio import gr


class blk(gr.decim_block):
    def __init__(self, batch_length = 65536):
        gr.decim_block.__init__(self,
            name="Decimating Averages",
            in_sig=[np.float32],
            out_sig=[np.float32,np.float32],
            decim = batch_length)

        self.set_relative_rate(1.0/batch_length)
        self.batch_length = batch_length

    def work(self, input_items, output_items):
        n_out_items = len(input_items[0]) // self.batch_length
        for i in range(0, n_out_items):
            output_items[0][i] = np.average(input_items[0][i*self.batch_length:(i+1)*self.batch_length])
            output_items[1][i] = np.sqrt(
                (np.average(np.square(input_items[0][i*self.batch_length:(i+1)*self.batch_length])) -
                output_items[0][i]*output_items[0][i])
            )
            pass
        return n_out_items