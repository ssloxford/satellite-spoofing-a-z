import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import seaborn as sns

# Given a bit error rate, what's the probability that the packet doesn't decode?

def rs_error_rate(ber, data_length, parity_length, interleave_depth=1, symbol_size=8):
    symbol_correct_rate = (1 - ber)**symbol_size
    symbol_error_rate = 1 - (1 - ber)**symbol_size
    block_length = (data_length+parity_length)/interleave_depth
    print(f"block length: {block_length}")
    corruptible_symbols = int(parity_length/interleave_depth/2) # the number of corrupted symbols that can be corrected
    print(f"corruptible_symbols: {corruptible_symbols}")

    print(list(map(
        lambda e: (
        (symbol_correct_rate)**(block_length-e)
        * symbol_error_rate**e
        * special.comb(block_length, e)
        ),
        range(0, corruptible_symbols+1)
    )))

    block_correct_rate = np.sum(list(map(
        lambda e: (
            (symbol_correct_rate)**(block_length-e)
            * symbol_error_rate**e
            * special.comb(block_length, e)
        ),
        range(0, corruptible_symbols+1)
    )))
    print(f"block correct rate: {block_correct_rate}")


    block_error_rate = 1 - np.sum(list(map(
        lambda e: (
            (symbol_correct_rate)**(block_length-e)
            * symbol_error_rate**e
            * special.comb(block_length, e)
        ),
        range(0, corruptible_symbols+1)
    )))

    packet_correct_rate = (block_correct_rate)**interleave_depth
    packet_error_rate = 1 - (block_correct_rate)**interleave_depth
    # equivalent_ser is the ser we'd get without the code check
    len = (data_length + parity_length)*symbol_size*interleave_depth
    equivalent_ber = 1 - (packet_correct_rate)**(1/len)
    eq_ber_2 = packet_error_rate * 0.5

    return {
        "symbol_error_rate": symbol_error_rate,
        "block_correct_rate": block_correct_rate,
        "packet_correct_rate": packet_correct_rate,
        "equivalent_ber": eq_ber_2,
        "improvement rate": ber/equivalent_ber
    }

def rs_bit_error_rate(ber, data_length, parity_length, interleave_depth=1, symbol_size=8):
    return rs_error_rate(ber, data_length, parity_length, interleave_depth, symbol_size)["equivalent_ber"]


def hamming_7_4(ber):
    p0 = (1-ber)**7
    p1 = (1-ber)**6 * ber * 7
    return 0.5 * (1 - (p0 + p1))
