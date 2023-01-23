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

# Generate the bit error rate heatmap from Figure 4
# Output in `out/Figure_4.pdf`

import typer
import numpy as np
from scipy import special
import matplotlib.pyplot as plt
import seaborn as sns
import importlib
import matplotlib.colors
import datetime
import os
from tqdm import tqdm

from lib.overshadowing_ber import attack_psk, attack_qam


def main(samples: int = int(2e5), M_PSK: int = 64):
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
    N = int(1e3)  # number of samples for each run # TODO: paper has 1E6
    EvN0dB_min = -1.6  # shannon limit

    # Calculate theoretical B/M-PSK values
    BPSK = lambda R: 0.5 * special.erfc(np.sqrt(R * 10 ** (EbN0dBs / 10)))
    PSK_M = lambda M, R: (1 / np.log2(M)) * special.erfc(
        np.sqrt(np.log2(M) * R * 10 ** (EbN0dBs / 10)) * np.sin(np.pi / M)
    )

    # Calculate the theoretical limit of max coding gain
    shannon_limit = np.vectorize(lambda x: 0.5 if x < EvN0dB_min else 0)(EbN0dBs)

    # Generate results - attacker-to-victim ratio against victim-to-noise ratio for 64-PSK
    EvN0dB_2dplot_step = 0.5
    EaEvdBs_2dplot_step = 0.1

    EvN0dBs_2dplot = np.arange(-25, 50.1, EvN0dB_2dplot_step)
    EaEvdBs_2dplot = np.arange(12, 35.1, EaEvdBs_2dplot_step)
    grid_plot_extent = [
        np.min(EvN0dBs_2dplot) - EvN0dB_2dplot_step / 2,
        np.max(EvN0dBs_2dplot) - EvN0dB_2dplot_step / 2,
        np.min(EaEvdBs_2dplot) - EaEvdBs_2dplot_step / 2,
        np.max(EaEvdBs_2dplot) - EaEvdBs_2dplot_step / 2,
    ]

    bers = []
    for EaEvdB in tqdm(EaEvdBs_2dplot):
        bers_inner = []
        a = 1 / (10 ** (EaEvdB / 20))
        for EvN0dB in EvN0dBs_2dplot:
            EaN0dB = EvN0dB + EaEvdB
            ber = attack_qam(M_PSK, samples, EaEvdB, EaN0dB, False)
            bers_inner.append(ber)
        bers.append(bers_inner)

    # Graph the results - each point coloured according to bit error rate
    plt.figure(figsize=(5, 4))
    plt.imshow(
        bers,
        cmap=sns.cm.rocket_r,
        extent=grid_plot_extent,
        origin="lower",
        aspect="auto",
        norm=matplotlib.colors.LogNorm(),
    )
    cbar = plt.colorbar()
    cbar.set_label("Bit Error Rate (BER)")
    plt.xlabel("$E_v/N_0$ [dB]")
    plt.ylabel("$E_a/E_v$ [dB]")
    plt.xlim(-20, 50)
    plt.ylim(15, 35)

    plt.tight_layout()

    plt.savefig("out/Figure_4.pdf", bbox_inches="tight")


if __name__ == "__main__":
    typer.run(main)
