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

# Generate the IQ diagrams from Figure 1
# Output in `out/Figure_1a.pdf`, `out/Figure_1b.pdf`, `out/Figure_1c.pdf`

import typer
import numpy as np
import matplotlib.pyplot as plt
import math
import seaborn as sns
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import matplotlib.font_manager
from pathlib import Path
import matplotlib
import os


def iq_base(xmin, xmax, ymin, ymax):
    fig = plt.figure(figsize=((xmax - xmin) / (ymax - ymin) * 3, 3), frameon=False)
    ax = fig.add_subplot(1, 1, 1)

    plt.xlim(xmin, xmax)
    plt.ylim(ymin, ymax)
    plt.xticks(np.arange(-1, 1.01, 2))
    plt.yticks(np.arange(-1, 1.01, 2))

    ax.grid(False)
    ax.axis("equal")
    ax.spines["left"].set_position("zero")
    ax.spines["bottom"].set_position("zero")
    # removing the default axis on all sides:
    for side in ["bottom", "right", "top", "left"]:
        ax.spines[side].set_visible(False)

    # get width and height of axes object to compute
    # matching arrowhead length and width
    dps = fig.dpi_scale_trans.inverted()
    bbox = ax.get_window_extent().transformed(dps)
    width, height = bbox.width, bbox.height

    # manual arrowhead width and length
    hw = 1.0 / 40.0 * (ymax - ymin)
    hl = 1.0 / 40.0 * (xmax - xmin)
    lw = 1.0  # axis line width
    ohg = 0.3  # arrow overhang

    # compute matching arrowhead length and width
    yhw = hw / (ymax - ymin) * (xmax - xmin) * height / width
    yhl = hl / (xmax - xmin) * (ymax - ymin) * width / height

    # draw x and y axis
    ax.arrow(
        xmin,
        0,
        xmax - xmin,
        0.0,
        fc="k",
        ec="k",
        lw=lw,
        head_width=hw,
        head_length=hl,
        overhang=ohg,
        length_includes_head=True,
        clip_on=False,
    )

    ax.arrow(
        0,
        ymin,
        0.0,
        ymax - ymin,
        fc="k",
        ec="k",
        lw=lw,
        head_width=yhw,
        head_length=yhl,
        overhang=ohg,
        length_includes_head=True,
        clip_on=False,
    )
    plt.text(xmax - 0.08, -0.2, "I")
    plt.text(0.05, ymax - 0.12, "Q")


def main():
    # Ensure output directory exists
    os.makedirs(os.getcwd() + "/out", exist_ok=True)

    # Set style
    sns.set_theme(context="notebook", style="white")
    new_rc = {
        "xtick.bottom": True,
        "xtick.minor.bottom": True,
        "xtick.minor.visible": False,
        "xtick.top": False,
        "ytick.left": True,
        "ytick.minor.left": True,
        "ytick.minor.visible": False,
        "ytick.right": False,
        "grid.color": "#c0c0c0",
        "grid.linestyle": "-",
        "axes.grid": False,
        "font.family": "serif",
        "text.usetex": False,
    }
    plt.rcParams |= new_rc

    # Set colours

    bad_color = [0.8, 0.2, 0.2]
    good_color = [0.2, 0.8, 0.2]
    cdict = {
        "red": [
            [0, bad_color[0], bad_color[0]],
            [0.5, bad_color[0], good_color[0]],
            [1, good_color[0], good_color[0]],
        ],
        "green": [
            [0, bad_color[1], bad_color[1]],
            [0.5, bad_color[1], good_color[1]],
            [1, good_color[1], good_color[1]],
        ],
        "blue": [
            [0, bad_color[2], bad_color[2]],
            [0.5, bad_color[2], good_color[2]],
            [1, good_color[2], good_color[2]],
        ],
        "alpha": [[0, 1, 1], [0.5, 0, 0], [1, 1, 1]],
    }

    newcmp = LinearSegmentedColormap("testCmap", segmentdata=cdict, N=256)

    colcycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    # Define constants
    EaEvdB = 3
    EvN0dB = 6

    EaN0dB = EaEvdB + EvN0dB

    qpsk_constellation = np.array([1, 1j, -1, -1j])
    attacker_constellation = qpsk_constellation

    # Generate subfigure a)

    iq_base(-2.2, 2.2, -2.2, 2.2)

    ax_16qam = np.linspace(-1, 1, 4, True)
    constellation_16qam_i, constellation_16qam_q = np.meshgrid(ax_16qam, ax_16qam)
    constellation_16qam = np.array(
        constellation_16qam_i + 1j * constellation_16qam_q
    ).flatten()

    norm = np.average(constellation_16qam.real**2 + constellation_16qam.imag**2)
    constellation_16qam /= np.sqrt(norm / 4)

    norm = np.average(constellation_16qam.real**2 + constellation_16qam.imag**2)

    plt.scatter(
        np.real(constellation_16qam), np.imag(constellation_16qam), color=colcycle[0]
    )

    plt.xlim(-2.2, 2.2)
    plt.ylim(-2.2, 2.2)

    plt.arrow(
        0,
        0,
        np.real(constellation_16qam[11]),
        np.imag(constellation_16qam[11]),
        length_includes_head=True,
        color="black",
        head_width=0.07,
    )

    plt.plot(
        0.4 * np.cos(np.arange(0, np.arctan(1 / 3), 0.01)),
        0.4 * np.sin(np.arange(0, np.arctan(1 / 3), 0.01)),
        color="black",
    )
    plt.text(0.45, 0.045, "$\\phi$")
    plt.text(0.7, 0.3, "$A$")

    plt.tight_layout()
    plt.savefig("out/Figure_1a.pdf")

    # Generate subfigure b)

    victim_constellation_a = qpsk_constellation * 10 ** (-EaEvdB / 20)
    offset_victim_a = attacker_constellation[0] + victim_constellation_a

    iq_base(-1.2, 2.2, -1.2, 1.2)

    noise_x = np.arange(-3, 3, 0.02)
    noise_y = np.arange(-3, 3, 0.02)
    xx, yy = np.meshgrid(noise_x, noise_y)
    noise_sigma = 10 ** (-EaN0dB / 20) / np.sqrt(2)

    zzs = np.array(
        [
            np.exp(
                -((xx - np.real(pt)) ** 2 + (yy - np.imag(pt)) ** 2) / noise_sigma**2
            )
            for pt in offset_victim_a
        ]
    )
    zz = np.sum(zzs, axis=0)
    zzr = np.max(zz) * 1.2
    zz *= np.where(xx > np.abs(yy), 1, -1)
    plt.contourf(xx, yy, zz, cmap=newcmp, vmin=-zzr, vmax=zzr, levels=16)

    plt.plot([-2, 2], [-2, 2], c="gray")
    plt.plot([-2, 2], [2, -2], c="gray")

    lines = []

    colcycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    lines.append(
        plt.scatter(
            np.real(attacker_constellation),
            np.imag(attacker_constellation),
            color=colcycle[0],
        )
    )
    lines.append(
        plt.scatter(
            np.real(offset_victim_a), np.imag(offset_victim_a), color=colcycle[1]
        )
    )

    plt.legend(lines, ["Attacker", "Victim"])

    plt.xlim(-1.2, 2.2)
    plt.ylim(-1.2, 1.2)

    plt.tight_layout()
    plt.savefig("out/Figure_1b.pdf")

    # Generate subfigure c)

    iq_base(-1.2, 2.2, -1.2, 1.2)

    noise_x = np.arange(-3, 3, 0.02)
    noise_y = np.arange(-3, 3, 0.02)
    xx, yy = np.meshgrid(noise_x, noise_y)
    noise_sigma = 10 ** (-EaN0dB / 20) / np.sqrt(2)

    zzs = np.array(
        [
            np.exp(
                -((xx - np.real(pt)) ** 2 + (yy - np.imag(pt)) ** 2) / noise_sigma**2
            )
            for pt in [
                attacker_constellation[0]
                + qpsk_constellation[0] * 10 ** (-EaEvdB / 20) * np.exp(1j * ph)
                for ph in np.linspace(0, 2 * np.pi, 600)
            ]
        ]
    )
    zz = np.sum(zzs, axis=0)
    zzr = np.max(zz) * 1.2
    zz *= np.where(xx > np.abs(yy), 1, -1)
    plt.contourf(xx, yy, zz, cmap=newcmp, vmin=-zzr, vmax=zzr, levels=16)

    lines = []

    plt.plot([-2, 2], [-2, 2], c="gray")
    plt.plot([-2, 2], [2, -2], c="gray")

    lines.append(
        plt.scatter(
            np.real(attacker_constellation),
            np.imag(attacker_constellation),
            color=colcycle[0],
        )
    )

    plt.legend(lines, ["Attacker"])

    plt.xlim(-1.2, 2.2)
    plt.ylim(-1.2, 1.2)

    plt.tight_layout()
    plt.savefig("out/Figure_1c.pdf")


if __name__ == "__main__":
    typer.run(main)
