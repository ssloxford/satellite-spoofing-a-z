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

# Generate the IQ diagrams from Figure 7
# Output in `out/Figure_7.pdf`

import typer
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os

def fspl(d_m, f_MHz):
    return -1 * (20 * np.log10(d_m) + 20 * np.log10(f_MHz) - 27.55)


def main():
    # Ensure output directory exists
    os.makedirs(os.getcwd() + "/out", exist_ok=True)

    # Equipment table
    equipment_1600 = {
        "1.6GHz, Module Amplifier, Omnidirectional Antenna": {
            "output_power": 7,
            "antenna_eirp": 12,
            "frequency": 1600,
        },
        "1.6GHz, Custom IC Amplifier, Omnidirectional Antenna": {
            "output_power": 10,
            "antenna_eirp": 12,
            "frequency": 1600,
        },
    }

    equipment_8100 = {
        "8.1GHz, Module Amplifier, Stealthy Antenna": {
            "output_power": 4,
            "antenna_eirp": 0,
            "frequency": 8100,
        },
        "8.1GHz, Module Amplifier, High Gain Antenna": {
            "output_power": 4,
            "antenna_eirp": 38,
            "frequency": 8100,
        },
        "8.1GHz, Custom IC Amplifier, Stealthy Antenna": {
            "output_power": 10,
            "antenna_eirp": 0,
            "frequency": 8100,
        },
        "8.1GHz, Custom IC Amplifier, High Gain Antenna": {
            "output_power": 10,
            "antenna_eirp": 38,
            "frequency": 8100,
        },
    }

    equipment_11700 = {
        "11.7GHz, Module Amplifier, Stealthy Antenna": {
            "output_power": 4,
            "antenna_eirp": 20,
            "frequency": 11700,
        },
        "11.7GHz, Custom IC Amplifier, Stealthy Antenna": {
            "output_power": 3,
            "antenna_eirp": 20,
            "frequency": 11700,
        },
    }
    equipment_19700 = {
        "19.7GHz, Custom IC Amplifier, Stealthy Antenna": {
            "output_power": 10,
            "antenna_eirp": 34,
            "frequency": 19700,
        },
    }

    distances = np.array(list(range(1, 8000, 5)))
    x_unit = 1000  # km

    def process(equipment):
        results = {}
        for n, x in equipment.items():
            results[n] = list(
                map(
                    lambda d: x["output_power"]
                    + x["antenna_eirp"]
                    + fspl(d, x["frequency"]),
                    distances,
                )
            )
        return results

    colcycle = plt.rcParams["axes.prop_cycle"].by_key()["color"]

    fig, axs = plt.subplots(2, 2, figsize=(10, 11))
    # plt.xlim(1/x_unit, 8000/x_unit)
    # plt.ylim(-140, 0)
    plt.setp(
        axs,
        xlim=(1 / x_unit, 8000 / x_unit),
        ylim=(-150, 0),
        xticks=range(0, 9),
        xticklabels=list(map(lambda x: str(float(x)), range(0, 9))),
    )

    axs[0][0].set_title("L band, 1.6GHz")
    for n, res in process(equipment_1600).items():
        axs[0][0].plot(distances / x_unit, res, label=n)
    axs[0][0].hlines([-152.8, -142.2], 0, 10, linestyle="dashed", label="GPS L1")
    axs[0][0].hlines(
        [-142, -131.4],
        0,
        10,
        linestyle="dashed",
        color=mcolors.TABLEAU_COLORS["tab:orange"],
        label="Iridium-NEXT",
    )
    axs[0][0].legend()
    axs[0][0].margins(x=0)

    axs[1][0].set_title("X band, 8.1GHz")
    for n, res in process(equipment_8100).items():
        axs[1][0].plot(distances / x_unit, res, label=n)
    axs[1][0].hlines(
        [-134.7, -108.2],
        0,
        10,
        linestyle="dashed",
        label="Terra/Aqua (Direct Broadcast",
    )
    axs[1][0].hlines(
        [-139.4, -112.9],
        0,
        10,
        linestyle="dashed",
        color=mcolors.TABLEAU_COLORS["tab:orange"],
        label="Planet Labs Dove (QPSK)",
    )
    axs[1][0].margins(x=0)
    axs[1][0].legend()

    axs[0][1].set_title("Ku band, 11.7GHz")
    for n, res in process(equipment_11700).items():
        axs[0][1].plot(distances / x_unit, res, label=n)
    axs[0][1].hlines(
        [-98.75, -75.15], 0, 10, linestyle="dashed", label="Starlink (64-QAM)"
    )
    axs[0][1].hlines(
        [-118.75, -87.75],
        0,
        10,
        linestyle="dashed",
        color=mcolors.TABLEAU_COLORS["tab:orange"],
        label="Starlink (BPSK)",
    )
    axs[0][1].margins(x=0)
    axs[0][1].legend()

    axs[1][1].set_title("Ka band, 19.7GHz")
    for n, res in process(equipment_19700).items():
        axs[1][1].plot(distances / x_unit, res, label=n)
    axs[1][1].hlines([-108.5, -74.1], 0, 10, linestyle="dashed", label="Alphasat")
    axs[1][1].margins(x=0)
    axs[1][1].legend()

    fig.add_subplot(111, frameon=False)

    plt.tick_params(
        labelcolor="none",
        which="both",
        top=False,
        bottom=False,
        left=False,
        right=False,
    )
    plt.ylabel("Attacker received power [dBW]")
    plt.xlabel("Attacker distance from victim receiver [km]")

    plt.tight_layout()
    plt.savefig("out/Figure_7.pdf")


if __name__ == "__main__":
    typer.run(main)
