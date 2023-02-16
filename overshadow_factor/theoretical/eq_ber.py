import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import seaborn as sns
import coding

sns.set_theme()

bers = 10**np.arange(-8, np.log10(0.5), 0.01)

BPSK = lambda R: 0.5 * special.erfc(np.sqrt(R * 10**(bers/10)))
PSK_M = lambda M, R: (1/np.log2(M))*special.erfc(np.sqrt(np.log2(M) * R * 10**(bers/10))*np.sin(np.pi/M))


shannon_limit = np.vectorize(lambda x: 0.5 if x > 0.19737 else 0.0)(bers) # value read from modulation graph, where BPSK crosses the -1.6dB Shannon limit

rs_test_v = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=4, parity_length=3, interleave_depth=1, symbol_size=1))
cadu_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=1020, parity_length=128, interleave_depth=4)) # This is the wrong interleave_depth
ccsds_8_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=239*5, parity_length=8*5, interleave_depth=5))
ccsds_16_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=223*5, parity_length=32*5, interleave_depth=5))
hamming_v = np.vectorize(coding.hamming_7_4)

# Plot the graphs
# TODO: plot QAM

fig, axs = plt.subplots(1, 1, subplot_kw={"yscale": "log", "xscale": "log"})
#plt.setp(axs, ylim=[1E-14, 0.6])
#plt.setp(axs, xlim=[1E-7, 0.6])

axs.title.set_text("BPSK/QPSK")

# TODO: concatenated codings
# TODO: soft decoding gain

axs.plot(bers, bers, label="No coding")
axs.plot(bers, shannon_limit, label="Theoretical maximum coding gain, assuming BPSK")
#axs.plot(bers, rs_test_v(bers), label="(7,4) Hamming code, hard decisions")
#axs.plot(bers, cadu_rs(bers), label="CADU Reed-Solomon, hard decisions")

axs.plot(bers, cadu_rs(coding.conv_error_rate(BPSK, 1, 2)), label = "RS & CC Rate 1/2")
axs.plot(bers, cadu_rs(coding.conv_error_rate(BPSK, 3, 4)), label = "RS & CC Rate 3/4")
axs.plot(bers, cadu_rs(coding.conv_error_rate(BPSK, 7, 8)), label = "RS & CC Rate 7/8")


#axs.plot(bers, cadu_rs(bers), label="CADU Reed-Solomon, soft decisions")

#axs.plot(bers, ccsds_8_rs(bers), label="CCSDS E=8 Reed-Solomon")
#axs.plot(bers, ccsds_16_rs(bers), label="CCSDS E=16 Reed-Solomon")

#axs.plot(bers, coding.conv_error_rate(bers, 1, 2), label = "CC Rate 1/2")
#axs.plot(bers, coding.conv_error_rate(bers, 3, 4), label = "CC Rate 3/4")
#axs.plot(bers, coding.conv_error_rate(bers, 7, 8), label = "CC Rate 7/8")

#axs.plot(bers, ccsds_16_rs(coding.conv_error_rate(BPSK, 1, 2)), label = "RS & CC Rate 1/2")
#axs.plot(bers, ccsds_16_rs(coding.conv_error_rate(BPSK, 3, 4)), label = "RS & CC Rate 3/4")
#axs.plot(bers, ccsds_16_rs(coding.conv_error_rate(BPSK, 7, 8)), label = "RS & CC Rate 7/8")

#axs.plot(bers, shannon_limit, label="Theoretical Shannon limit")

axs.legend()
plt.xlabel('Bit Error Rate')
plt.ylabel('Equivalent Bit Error Rate')
plt.show()
