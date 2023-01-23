import numpy as np
import matplotlib.pyplot as plt

def measure_power(iqs):
    return np.average(iqs.real**2 + iqs.imag**2)

def gaussian_noise(n, N0):
    sigma = np.sqrt(N0/2)
    return np.random.normal(0,sigma,n) + 1j * np.random.normal(0,sigma,n)

def measure_constellation_Eb(constellation_iq):
    bit_per_symbol = np.log2(len(constellation_iq))
    energy_per_symbol = measure_power(constellation_iq)
    energy_per_bit = energy_per_symbol / bit_per_symbol
    return energy_per_bit

def norm_constellation(constellation_iq):
    factor = np.sqrt(measure_constellation_Eb(constellation_iq))
    constellation_iq /= factor

    return constellation_iq, factor

def plot_constellation(cons):
    constellation = cons[0]
    bits = cons[1]
    plt.scatter(np.real(constellation), np.imag(constellation), c=range(len(constellation)))
    for c, b in zip(constellation, bits):
        plt.text(c.real, c.imag, bin(b))
    ax = plt.gca()
    ax.axis('equal')

def generate_psk_constellation(M):
    constellation, _ = norm_constellation(np.exp(1j * np.linspace(0, 2*np.pi, M, endpoint=False)))
    symbol_ids = np.array(range(M))
    symbol_bits = symbol_ids ^ (symbol_ids >> 1)
    return constellation, symbol_bits

def generate_qam_constellation(M):
    sqrtM = int(np.sqrt(M))
    bits_per_side = int(np.log2(sqrtM))
    sides = np.linspace(-1, 1, sqrtM, endpoint=True)
    constellation_i, constellation_q = np.meshgrid(sides, sides)
    constellation, factor = norm_constellation((constellation_i + 1j*constellation_q).flatten())

    symbol_ids = np.array(range(sqrtM))
    symbol_bits = symbol_ids ^ (symbol_ids >> 1)
    symbol_bits_r, symbol_bits_c = np.meshgrid(symbol_bits, symbol_bits)
    symbol_bits_full = (symbol_bits_r.flatten() << bits_per_side) + symbol_bits_c.flatten()

    return constellation, symbol_bits_full, (-1/factor, 2/(sqrtM-1)/factor)

psk_constellations = {
    2: generate_psk_constellation(2),
    4: generate_psk_constellation(4),
    8: generate_psk_constellation(8),
    16: generate_psk_constellation(16),
}

qam_constellations = {
    4: generate_qam_constellation(4),
    16: generate_qam_constellation(16),
    64: generate_qam_constellation(64),
    256: generate_qam_constellation(256),
}

def decode_psk_constellation(M, iq):
    return np.mod(np.rint(np.angle(iq) * M / (2*np.pi)), M).astype(int)

def decode_qam_constellation(M, iq):
    Msqrt = np.sqrt(M)
    _, _, gap = qam_constellations[M]
    column = np.clip(np.rint((np.real(iq) - gap[0]) / gap[1]), 0, Msqrt - 1)
    row = np.clip(np.rint((np.imag(iq) - gap[0]) / gap[1]), 0, Msqrt - 1)
    return (row * Msqrt + column).astype(int)

def random_iq(n, range):
    i = 2*range*np.random.random(n) - range
    q = 2*range*np.random.random(n) - range
    return i+1j*q

def plot_decode(M, iq, decoder):
    decoded = decoder(M, iq)
    plt.scatter(np.real(iq), np.imag(iq), c=decoded, s=1)

def generate_bit_accelerator_table(M):
    return np.array([bin(i).count("1") for i in range(M)])

BIT_ACCELERATOR_TABLE = generate_bit_accelerator_table(1024)

def measure_bit_errors(b1, b2):
    return np.sum(BIT_ACCELERATOR_TABLE[b1 ^ b2])

def attack_generic(constellation, decoder, M, n, EaEvdB, EaN0dB, align = False):
    #Ea is assumed to be one.
    attacker_samples = np.random.randint(0, M, n)
    total_iq = constellation[0][attacker_samples]

    if EaEvdB is not None:
        victim_samples = np.random.randint(0, M, n)
        victim_voltage_scale = 10**(-EaEvdB/20)
        victim_iq = constellation[0][victim_samples] * victim_voltage_scale
        if not align:
            victim_phases = (2*np.pi)*np.random.random(n)
            victim_iq *= np.exp(1j*victim_phases)
        
        total_iq += victim_iq

    if EaN0dB is not None:
        N0 = 10**(-EaN0dB/10)
        noise_iq = gaussian_noise(n, N0)

        total_iq += noise_iq

    decoded_samples = decoder(M, total_iq)

    attacker_bits = constellation[1][attacker_samples]
    decoded_bits = constellation[1][decoded_samples]

    bit_errors = measure_bit_errors(attacker_bits, decoded_bits)
    total_bits = np.log2(M) * n
    return bit_errors / total_bits

def attack_psk(M, n, EaEvdB, EaN0dB, align = False):
    return attack_generic(psk_constellations[M], decode_psk_constellation, M, n, EaEvdB, EaN0dB, align)

def attack_qam(M, n, EaEvdB, EaN0dB, align = False):
    return attack_generic(qam_constellations[M], decode_qam_constellation, M, n, EaEvdB, EaN0dB, align)