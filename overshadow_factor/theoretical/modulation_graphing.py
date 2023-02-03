import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import seaborn as sns
import coding

sns.set_theme()

EbN0dBs = np.arange(-5, 15, 0.1)

BPSK = lambda R: 0.5 * special.erfc(np.sqrt(R * 10**(EbN0dBs/10)))
PSK_M = lambda M, R: (1/np.log2(M))*special.erfc(np.sqrt(np.log2(M) * R * 10**(EbN0dBs/10))*np.sin(np.pi/M))

shannon_limit = np.vectorize(lambda x: 0.5 if x < -1.6 else 0)(EbN0dBs)

rs_test_v = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=4, parity_length=3, interleave_depth=1, symbol_size=1))
cadu_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=1020, parity_length=128, interleave_depth=4)) # This is the wrong interleave_depth
ccsds_8_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=239*5, parity_length=8*5, interleave_depth=5))
ccsds_16_rs = np.vectorize(lambda ber : coding.rs_bit_error_rate(ber, data_length=223*5, parity_length=32*5, interleave_depth=5))
hamming_v = np.vectorize(coding.hamming_7_4)

# Plot the graphs
# TODO: plot QAM

fig, axs = plt.subplots(1, 1, subplot_kw={"yscale": "log"})
#fig, axs = plt.subplots(1, 2, subplot_kw={"yscale": "log"})
#plt.setp(axs, ylim=[1E-6, 1])
plt.setp(axs, ylim=[1E-9, 1])
plt.setp(axs, xlim=[0, 10])

axs.title.set_text("BPSK/QPSK")

axs.plot(EbN0dBs, BPSK(1), label="No coding")
#axs.plot(EbN0dBs, rs_test_v(BPSK(4/7)), label="(7,4) Hamming code, hard decisions")
#axs.plot(np.vectorize(coding.soft_decoding_bonus)(EbN0dBs), rs_test_v(BPSK(4/7)), label="(7,4) Hamming code, soft decisions")
#axs.plot(EbN0dBs, cadu_rs(BPSK(223/255)), label="CADU Reed-Solomon, hard decisions")
#axs.plot(coding.soft_decoding_bonus(EbN0dBs), cadu_rs(BPSK(223/255)), label="CADU Reed-Solomon, soft decisions")
#axs.plot(EbN0dBs, ccsds_8_rs(BPSK(239/255)), label="CCSDS E=8 Reed-Solomon")
#axs.plot(EbN0dBs, ccsds_16_rs(BPSK(223/255)), label="CCSDS E=16 Reed-Solomon")
axs.plot(EbN0dBs, coding.conv_error_rate(BPSK, 1, 2), label = "CC Rate 1/2")
axs.plot(EbN0dBs, coding.conv_error_rate(BPSK, 3, 4), label = "CC Rate 3/4")
axs.plot(EbN0dBs, coding.conv_error_rate(BPSK, 7, 8), label = "CC Rate 7/8")

axs.plot(EbN0dBs, ccsds_16_rs(coding.conv_error_rate(BPSK, 1, 2)), label = "RS & CC Rate 1/2")
axs.plot(EbN0dBs, ccsds_16_rs(coding.conv_error_rate(BPSK, 3, 4)), label = "RS & CC Rate 3/4")
axs.plot(EbN0dBs, ccsds_16_rs(coding.conv_error_rate(BPSK, 7, 8)), label = "RS & CC Rate 7/8")

axs.plot(EbN0dBs, shannon_limit, label="Theoretical Shannon limit")

#axs[1].title.set_text("8-PSK")
#axs[1].plot(EbN0dBs, PSK_M(8, 1), label="No coding")
#axs[1].plot(EbN0dBs, rs_test_v(PSK_M(8, 4/7)), label="(7,4) Hamming code, hard decisions")
#axs[1].plot(np.vectorize(coding.soft_decoding_bonus)(EbN0dBs), rs_test_v(PSK_M(8, 4/7)), label="(7,4) Hamming code, soft decisions")
#axs[1].plot(EbN0dBs, cadu_rs(PSK_M(8, 223/255)), label="CADU Reed-Solomon, hard decisions")
#axs[1].plot(coding.soft_decoding_bonus(EbN0dBs), cadu_rs(PSK_M(8, 223/255)), label="CADU Reed-Solomon, soft decisions")
#axs[1].plot(EbN0dBs, ccsds_8_rs(PSK_M(8, 239/255)), label="CCSDS E=8 Reed-Solomon")
#axs[1].plot(EbN0dBs, ccsds_16_rs(PSK_M(8, 223/255)), label="CCSDS E=16 Reed-Solomon")
#axs[1].plot(EbN0dBs, shannon_limit, label="Theoretical Shannon limit")

axs.legend()
plt.xlabel('Eb/N0, dB')
plt.ylabel('Bit Error Rate')
plt.show()
