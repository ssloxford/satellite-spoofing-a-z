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

# Generate the IQ diagrams from Figure 6
# Output in `out/Figure_6.pdf`

import typer
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import pandas
import seaborn as sns
from collections import defaultdict
import os


calc_vhf = (
    lambda measurement, gain: 20.0562 * np.log10(float(measurement))
    - 0.967 * float(gain)
    + 36.63
)
calc_uhf = (
    lambda measurement, gain: 19.9905 * np.log10(float(measurement))
    - 0.9618 * float(gain)
    + 35.86
)

def get_measurements(path):
    with open(path) as csvfile:
        df = pandas.read_csv(csvfile, delimiter="\t", index_col=False)

        # bin the measurements
        d = defaultdict(list)
        for row in df.to_dict(orient="records"):
            if "fspl" in row.keys():
                fspl = row["fspl"]
                d[int(row["angle"])].append(
                    calc_vhf(row["measurement"], row["gain"]) + int(row["fspl"])
                )
            else:
                d[int(row["angle"])].append(calc_vhf(row["measurement"], row["gain"]))

        # average the angles
        angles = []
        measurements = []
        offset = None
        for angle, values in d.items():
            angles.append(angle / 360 * np.pi * 2)
            measurement = sum(values) / len(values)
            measurements.append(measurement)
            if int(angle) == 0:
                offset = measurement

        # normalise to zero
        measurements = list(
            map(lambda x: -45 if x - offset < -45 else x - offset, measurements)
        )  # hack for plotting

        #
        angles += list(map(lambda x: -x, angles))[::-1]
        measurements += measurements[::-1]

        return angles, measurements


def main():
    # Ensure output directory exists
    os.makedirs(os.getcwd() + "/out", exist_ok=True)

    sns.set_theme()

    fig, axs = plt.subplots(2, 2, subplot_kw={"projection": "polar"}, figsize=(8, 9))

    axs[0][0].title.set_text("VHF Yagi Varied Elevation")
    axs[0][0].plot(*get_measurements("Fig_6/data/test_yagi_roof_vhf_pitch.csv"))
    axs[0][0].plot(*get_measurements("Fig_6/data/test_yagi_field_vhf_pitch.csv"))

    axs[1][0].title.set_text("VHF Yagi Varied Azimuth")
    axs[1][0].plot(*get_measurements("Fig_6/data/test_yagi_roof_vhf_azimuth.csv"))
    axs[1][0].plot(*get_measurements("Fig_6/data/test_yagi_field_vhf_azimuth.csv"))

    axs[0][1].title.set_text("UHF Yagi Varied Elevation")
    axs[0][1].plot(*get_measurements("Fig_6/data/test_yagi_roof_uhf_pitch.csv"))
    axs[0][1].plot(*get_measurements("Fig_6/data/test_yagi_field_uhf_pitch.csv"))

    axs[1][1].title.set_text("UHF Yagi Varied Azimuth")
    axs[1][1].plot(*get_measurements("Fig_6/data/test_yagi_roof_uhf_azimuth.csv"))
    axs[1][1].plot(*get_measurements("Fig_6/data/test_yagi_field_uhf_azimuth.csv"))

    plt.setp(axs, ylim=[-45, 0])

    fmt = lambda x, pos: "{:g}".format(
        np.degrees(x if x >= 0 and x <= np.pi else 2 * np.pi - x)
    )
    for ax in [e for l in axs for e in l]:
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt))

    fig.legend(
        ("Urban Environment", "Open Field"), loc="lower center", bbox_to_anchor=(0.5, 0)
    )
    fig.tight_layout()

    plt.savefig("out/Figure_6.pdf", bbox_inches="tight")


if __name__ == "__main__":
    typer.run(main)
