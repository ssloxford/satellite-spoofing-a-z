# We can't assume that the attacker is able
# Several scenarios:
# * not phase aligned
# * phase aligned
# * hard decoding
# * soft decoding

# We take an attacker symbol as well as a victim symbol, and we overlay them according to the distribution of phases
# We get out the probability that, for a given SNR, the attacker's symbol is decoded
# We then further discuss how soft decoding can help as well
# # Add a gaussian offset for a given SNR per bit value
# Requires M (PSK level) to convert between SNR per bit and SNR per symbol
# Assuming no noise on tndarrayhe channel

import numpy as np
import typing

import matplotlib.pyplot as plt

# Simple PSK

# s = a + g*v
# s - decoded symbol
# a - attacker's symbol
# v - victim symbol
# g - SNR

def generate_psk_points(M=4, offsets=0, snr=1):
    attacker_symbol = (1, 0) # (I,Q)
    polar_victim_symbols = [(i*(2*np.pi))/M for i in range(M)]

    offset_constant = (2*np.pi)/M/(offsets+1) if offsets > 0 else 0

    print(f"offset_constant: {offset_constant}")

    for i in range(offsets):
        polar_victim_symbols += list(map(lambda x: x+(offset_constant*(i+1)), polar_victim_symbols))

    print(f"polar_victim_symbols: {polar_victim_symbols}")

    # convert polar victim symbols into cartesian coordinates
    I = lambda x: np.cos(x)
    Q = lambda x: np.sin(x)

    victim_symbols = [(I(x), Q(x)) for x in polar_victim_symbols]

    print(f"victim_symbols: {victim_symbols}")

    decoded_symbols = [(snr*i + attacker_symbol[0], snr*q + attacker_symbol[1]) for (i, q) in victim_symbols]
    return decoded_symbols

def gaussian_jam_offset(s: typing.Union[np.ndarray, np.csingle], EaEvdB: float, M: int):
    if s is np.csingle:
        size = 1
    else:
        size = len(s)
    n = (np.random.normal(size=size) + np.random.normal(size=size)*1j)/np.sqrt(2) # 0dB variance gaussian noise, complex
    EbN0dB = -EaEvdB # log law reciprocal
    EsN0dB = EbN0dB + 10*np.log10(np.log2(M)) # standard conversion between Es and Eb in log form
    return s + 10**(-EsN0dB/20)*n # root power ratio, because it's an IQ plot (voltage/voltage plot)

# Add a gaussian offset for a given SNR per bit value
# Requires M (PSK level) to convert between SNR per bit and SNR per symbol
def gaussian_offset(s: typing.Union[np.ndarray, np.csingle], EbN0dB: float, M: int):
    if s is np.csingle:
        size = 1
    else:
        size = len(s)
    n = (np.random.normal(size=size) + np.random.normal(size=size)*1j)/np.sqrt(2) # 0dB variance gaussian noise, complex
    Es_N0_dB = EbN0dB + 10*np.log10(np.log2(M)) # standard conversion between Es and Eb in log form
    return s + 10**(-Es_N0_dB/20)*n # root power ratio, because it's an IQ plot (voltage/voltage plot)

# TODO: understand units of a
# a - the amplitude of the victim signal on the channel
def psk_offset(s: typing.Union[np.ndarray, np.csingle], a: float):
    # pick a random point on the circle, and add it on
    if s is np.csingle:
        size = 1
    else:
        size = len(s)

    point = np.random.uniform(0, 2*np.pi, size=size)
    i = np.cos(point) * a
    q = np.sin(point) * a
    return s + i + q*1j

# Offset symbol s by a precisely aligned victim symbol in M-PSK of relative amplitude a
def psk_offset_aligned(s: typing.Union[np.ndarray, np.csingle], a: float, M: int):
    if s is np.csingle:
        size = 1
    else:
        size = len(s)

    victim_symbols = encode_m_psk(np.random.randint(0, M, size=size).astype(int), M)
    return s + victim_symbols*a

# gray code mapping
def bin_to_gray(x):
    return x ^ (x >> 1)

# returns the number of bit differences between x and y
def bit_errors(x: np.ndarray, y: np.ndarray):
    return np.vectorize(lambda x, y: bin(x ^ y).count("1"))(x, y)

# Encode the nth symbol in PSK
def encode_m_psk(n, M):
    offset_constant = ((2*np.pi)/M)
    return np.vectorize(lambda x: np.cos(offset_constant*x) + 1j*np.sin(offset_constant*x))(n)

def decode_m_psk_hard(s, M):
    angles = np.vectorize(
        lambda x: np.mod(np.arctan2(x.imag, x.real), 2*np.pi)
    )(s)

    m_angle = (2*np.pi)/M
    return np.mod(np.rint(angles/m_angle).astype(int), M)

# QAM

def qam_offset_aligned(s: typing.Union[np.ndarray, np.csingle], a: float, M: int):
    if s is np.csingle:
        size = 1
    else:
        size = len(s)

    victim_symbols = encode_m_qam(np.random.randint(0, M, size=size).astype(int), M)
    return s + victim_symbols*a

def qam_offset(s: typing.Union[np.ndarray, np.csingle], a: float, M: int):
    if s is np.csingle:
        size = 1
    else:
        size = len(s)

    # generate a random phase, and rotate by that angle
    # Generate a victim symbol
    victim_symbols = encode_m_qam(np.random.randint(0, M, size=size).astype(int), M)*a
    #print(f"victim_symbols: {victim_symbols}")

    # Cartesian to polar
    radius = np.vectorize(lambda x: np.sqrt(x.imag**2 + x.real**2))(victim_symbols)
    point = np.random.uniform(0, 2*np.pi, size=size)
    angle = np.angle(victim_symbols) + point

    # Polar to cartesian
    real = np.cos(angle)*radius
    imag = np.sin(angle)*radius

    return np.array(list(map(lambda r, c, s2: r + s2.real + 1j*c + s2.imag * 1j, real, imag, s)))


def encode_m_qam(n, M): # M has to be an even power of 2, for now: 16, 64, 256
    side_length = np.sqrt(M)
    rows, cols = np.divmod(n, side_length)

    # scale down the row/col to have total side length 1, and add on the half-square offset
    rows = 2*(rows / side_length) + (1/side_length) - 1
    cols = 2*(cols / side_length) + (1/side_length) - 1

    return np.array(list(map(lambda r, c: r + 1j*c, rows, cols)))

def decode_m_qam_hard(s, M):
    side_length = np.sqrt(M)
    n = np.rint(((s + (1 + 1j) - (1/side_length + (1/side_length)*1j)) / 2) * side_length)
    return np.mod(np.vectorize(lambda x: int(x.real*side_length + x.imag))(n), M)

# TODO: en/decoding APSK

def run_simulation(noise_func, N: int, M: int):
    encoded_symbols = encode_m_psk(np.random.randint(0, M, size=N).astype(int), M)
    decoded_symbols = decode_m_psk_hard(encoded_symbols, M)
    decoded_noisy_symbols = decode_m_psk_hard(noise_func(encoded_symbols), M)
    return np.mean(
        np.vectorize(
            lambda s1, s2: bit_errors(bin_to_gray(s1), bin_to_gray(s2))
        )(decoded_symbols, decoded_noisy_symbols)
    )/np.log2(M) # log2(M) = bits per symbol

def run_qam_simulation(noise_func, N: int, M: int):
    symbols = np.random.randint(0, M, size=N).astype(int)
    #print(f"symbols: {symbols}")
    encoded_symbols = encode_m_qam(symbols, M)
    decoded_symbols = decode_m_qam_hard(encoded_symbols, M)
    #print(f"decoded_symbols: {decoded_symbols}")
    decoded_noisy_symbols = decode_m_qam_hard(noise_func(encoded_symbols), M)
    #print(f"decoded_noisy_symbols: {decoded_noisy_symbols}")
    return np.mean(
        np.vectorize(
            lambda s1, s2: bit_errors(bin_to_gray(s1), bin_to_gray(s2))
        )(decoded_symbols, decoded_noisy_symbols)
    )/np.log2(M)

# model BER in to BER out
# EbEvdB - signal-to-victim ratio in dBs
def run_ber_simulation(EbEvdB: float, N: int, M: int):
    a = 1/(10**(EbEvdB/20))

    unaligned_ber = run_simulation(
        lambda x: psk_offset(x, a), N, M
    )

    aligned_ber = run_simulation(
        lambda x: psk_offset(x, a, M), N, M
    )

    return (unaligned_ber, aligned_ber)

# TODO: (stretch goal) demodulate QAM

# test plots

if __name__ == "__main__":
    points = [complex(0,0)]*100
    gaussian = gaussian_offset(points, 0, 4)
    psk = psk_offset(points, 1)
    psk_aligned = psk_offset_aligned(points, 1, 4)
    qam = qam_offset(points, 1, 16)
    qam_aligned = qam_offset_aligned(points, 1, 16)

    # Generate random QAM
    #qam_points = encode_m_qam(np.random.randint(0, 64, 1000), 64)

    fig, ax = plt.subplots()
    #ax.set_xlim(-1,1)
    #ax.set_ylim(-1,1)

    ax.plot(0, 0, marker='o')

    ax.plot(list(map(lambda x: x.real, gaussian)), list(map(lambda x: x.imag, gaussian)), linestyle='None', marker='o')
    ax.plot(list(map(lambda x: x.real, psk)), list(map(lambda x: x.imag, psk)), linestyle='None', marker='o')
    ax.plot(list(map(lambda x: x.real, psk_aligned)), list(map(lambda x: x.imag, psk_aligned)), linestyle='None', marker='o')
    ax.plot(list(map(lambda x: x.real, qam_aligned)), list(map(lambda x: x.imag, qam_aligned)), linestyle='None', marker='o')
    ax.plot(list(map(lambda x: x.real, qam)), list(map(lambda x: x.imag, qam)), linestyle='None', marker='o')
    plt.show()
