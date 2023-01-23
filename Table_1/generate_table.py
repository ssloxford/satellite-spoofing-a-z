#!/usr/bin/python3

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation version 3.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program. If not, see <https://www.gnu.org/licenses/>.

# Generate the bit error rate plot from Table 1
# Output in `out/Table_1.csv`

import typer
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import seaborn as sns
import importlib
import matplotlib.colors
import datetime
import os

from lib.overshadowing_ber import attack_psk, attack_qam


def correct_floating_point(l):
    out = []
    zeroed = False
    for item in l:
        if zeroed:
            out.append(0)
        else:
            out.append(item)
            zeroed = item < 1e-6
    return out


def main(samples: int = int(1e6)):
    # Ensure output directory exists
    os.makedirs(os.getcwd() + "/out", exist_ok=True)

    # Configure style

    sns.set_theme(context="notebook", style="white")
    new_rc = {
        "xtick.bottom": True,
        "xtick.minor.bottom": True,
        "xtick.minor.visible": True,
        "xtick.top": False,
        "ytick.left": True,
        "ytick.minor.left": True,
        "ytick.minor.visible": True,
        "ytick.right": False,
        "grid.color": "#c0c0c0",
        "grid.linestyle": "-",
        "axes.grid": False,
    }
    plt.rcParams |= new_rc

    # Set SNR range
    EbN0dBs = np.arange(-5, 15, 0.1)

    EaEvdBs_range = np.arange(-15, 45, 0.1)
    EvN0dB_min = -1.6  # shannon limit

    # Calculate theoretical B/M-PSK values
    BPSK = lambda R: 0.5 * special.erfc(np.sqrt(R * 10 ** (EbN0dBs / 10)))
    PSK_M = lambda M, R: (1 / np.log2(M)) * special.erfc(
        np.sqrt(np.log2(M) * R * 10 ** (EbN0dBs / 10)) * np.sin(np.pi / M)
    )

    # Calculate the theoretical limit of max coding gain
    shannon_limit = np.vectorize(lambda x: 0.5 if x < EvN0dB_min else 0)(EbN0dBs)

    # Run a Monte-Carlo simulation of BER of signal-to-victim ratio, in the absence of noise
    qam16_unaligned_ber = np.array(
        [attack_qam(16, samples, EaEvdB, None, False) for EaEvdB in EaEvdBs_range]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 16QAM")

    qam64_unaligned_ber = np.array(
        [attack_qam(64, samples, EaEvdB, None, False) for EaEvdB in EaEvdBs_range]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 64QAM")

    qam256_unaligned_ber = np.array(
        [attack_qam(256, samples, EaEvdB, None, False) for EaEvdB in EaEvdBs_range]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 256QAM")

    bpsk_unaligned_ber = np.array(
        [attack_psk(2, samples, EaEvdB, None, False) for EaEvdB in EaEvdBs_range]
    )
    print(f"{datetime.datetime.now()}: finished unaligned BPSK")

    qpsk_unaligned_ber = np.array(
        [attack_psk(4, samples, EaEvdB, None, False) for EaEvdB in EaEvdBs_range]
    )
    print(f"{datetime.datetime.now()}: finished unaligned QPSK")

    psk8_unaligned_ber = np.array(
        [attack_psk(8, samples, EaEvdB, None, False) for EaEvdB in EaEvdBs_range]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 8PSK")

    # Run a Monte-Carlo simulation of BER of signal-to-victim ratio, at the Shannon limit of noise
    qam16_unaligned_ber_noise = np.array(
        [
            attack_qam(16, samples, EaEvdB, EaEvdB + EvN0dB_min, False)
            for EaEvdB in EaEvdBs_range
        ]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 16QAM")

    qam64_unaligned_ber_noise = np.array(
        [
            attack_qam(64, samples, EaEvdB, EaEvdB + EvN0dB_min, False)
            for EaEvdB in EaEvdBs_range
        ]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 64QAM")

    qam256_unaligned_ber_noise = np.array(
        [
            attack_qam(256, samples, EaEvdB, EaEvdB + EvN0dB_min, False)
            for EaEvdB in EaEvdBs_range
        ]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 256QAM")

    bpsk_unaligned_ber_noise = np.array(
        [
            attack_psk(2, samples, EaEvdB, EaEvdB + EvN0dB_min, False)
            for EaEvdB in EaEvdBs_range
        ]
    )
    print(f"{datetime.datetime.now()}: finished unaligned BPSK")

    qpsk_unaligned_ber_noise = np.array(
        [
            attack_psk(4, samples, EaEvdB, EaEvdB + EvN0dB_min, False)
            for EaEvdB in EaEvdBs_range
        ]
    )
    print(f"{datetime.datetime.now()}: finished unaligned QPSK")
    psk8_unaligned_ber_noise = np.array(
        [
            attack_psk(8, samples, EaEvdB, EaEvdB + EvN0dB_min, False)
            for EaEvdB in EaEvdBs_range
        ]
    )
    print(f"{datetime.datetime.now()}: finished unaligned 8PSK")

    # Graph the results
    fig, axs = plt.subplots(1, 1, subplot_kw={"yscale": "log"}, figsize=(6, 5))
    plt.setp(axs, ylim=[1e-7, 1])
    plt.setp(axs, xlim=[-5, 35])

    cutoffs = [
        [
            EaEvdBs_range[np.max(np.where(np.array(bpsk_unaligned_ber) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qpsk_unaligned_ber) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(psk8_unaligned_ber) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qam16_unaligned_ber) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qam64_unaligned_ber) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qam256_unaligned_ber) > 1e-6))],
        ],
        [
            EaEvdBs_range[np.max(np.where(np.array(bpsk_unaligned_ber_noise) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qpsk_unaligned_ber_noise) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(psk8_unaligned_ber_noise) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qam16_unaligned_ber_noise) > 1e-6))],
            EaEvdBs_range[np.max(np.where(np.array(qam64_unaligned_ber_noise) > 1e-6))],
            EaEvdBs_range[
                np.max(np.where(np.array(qam256_unaligned_ber_noise) > 1e-6))
            ],
        ],
    ]

    with open("out/Table_1.csv", "w") as f:
        f.write(
            ",\t".join(["BPSK", "QPSK", "8-PSK", "16-QAM", "64-QAM", "256-QAM"]) + "\n"
        )
        for row in cutoffs:
            f.write(",\t".join([("%.1f" % elem) for elem in row]) + "\n")


if __name__ == "__main__":
    typer.run(main)
