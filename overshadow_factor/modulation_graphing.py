import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import seaborn as sns
import coding



EbN0dBs = np.arange(-8,15, 0.1)

BPSK = 0.5 * special.erfc(np.sqrt(10**(EbN0dBs/10)))
BPSK_4_7 = 0.5 * special.erfc(np.sqrt( (4/7) * (10**(EbN0dBs/10)) ))
BPSK_1020_128 = 0.5 * special.erfc(np.sqrt( ((255-32)/255) * (10**(EbN0dBs/10)) ))

PSK_M = lambda M: (1/np.log2(M))*special.erfc(np.sqrt(np.log2(M) * 10**(EbN0dBs/10))*np.sin(np.pi/M))
PSK_16 = PSK_M(16)

rs_test_v = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=4, parity_length=3, interleave_depth=1))
ccsds_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=1020, parity_length=128, interleave_depth=4))
hamming_v = np.vectorize(coding.hamming_7_4)


# Plot the graphs
# TODO: graph Shannon limit

bpsk_plot = plt.plot(EbN0dBs, BPSK, label="BPSK/QPSK")
bpsk_hamming_plot = plt.plot(EbN0dBs, hamming_v(BPSK_4_7), label="BPSK/QPSK with hamming")
bpsk_rs_plot = plt.plot(EbN0dBs, rs_test_v(BPSK_4_7), label="BPSK/QPSK with RS test")
bpsk_rs_plot = plt.plot(EbN0dBs, ccsds_rs(BPSK_1020_128), label="BPSK/QPSK with RS CCSDS")
#psk_8_plot = plt.plot(EbN0dBs, PSK_M(8), label="8 PSK")
#psk_16_plot = plt.plot(EbN0dBs, PSK_M(16), label="16 PSK")
#psk_32_plot = plt.plot(EbN0dBs, PSK_M(32), label="32 PSK")
#psk_64_plot = plt.plot(EbN0dBs, PSK_M(64), label="64 PSK")
#psk_64_rs_plot = plt.plot(EbN0dBs, ccsds_rs(PSK_M(64)), label="64 PSK with RS CCSDS")

# Styling
sns.set_theme()

plt.legend()
plt.yscale("log")
plt.xlabel('Eb/N0, dB')
plt.ylabel('Bit Error Rate')
plt.show()
