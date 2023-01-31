import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import csv
import pandas
import seaborn as sns
from collections import defaultdict

sns.set_theme()

calc_vhf = lambda measurement, gain: 20.0562 * np.log10(float(measurement)) - 0.967 * float(gain) + 36.63
calc_uhf = lambda measurement, gain: 19.9905 * np.log10(float(measurement)) - 0.9618 * float(gain) + 35.86

def get_measurements(path):
    with open(path) as csvfile:
        df = pandas.read_csv(csvfile, delimiter="\t", index_col=False)

        # bin the measurements
        d = defaultdict(list)
        for row in df.to_dict(orient="records"):
            d[int(row["angle"])].append(calc_vhf(row['measurement'], row['gain']))

        # average the angles
        angles = []
        measurements = []
        offset = None
        for angle, values in d.items():
            print("loop")
            angles.append(angle/360 * np.pi * 2)
            measurement = sum(values)/len(values)
            measurements.append(measurement)
            print(angle)
            if int(angle) == 0:
                offset = measurement

        # normalise to zero
        measurements = list(map(lambda x: x-offset, measurements))

        #
        angles += list(map(lambda x: -x, angles))[::-1]
        measurements += measurements[::-1]

        return angles, measurements


# [x] average points
# [x] normalise to zero

fig, axs = plt.subplots(2, 2, subplot_kw={'projection': 'polar'})

axs[0][0].title.set_text("VHF Yagi Varied Pitch")
axs[0][0].plot(*get_measurements("test_yagi_roof_vhf_pitch.csv"))
axs[0][0].plot(*get_measurements("test_yagi_field_vhf_pitch.csv"))

axs[1][0].title.set_text("VHF Yagi Varied Azimuth")
axs[1][0].plot(*get_measurements("test_yagi_roof_vhf_azimuth.csv"))
axs[1][0].plot(*get_measurements("test_yagi_field_vhf_azimuth.csv"))

axs[0][1].title.set_text("UHF Yagi Varied Pitch")
axs[0][1].plot(*get_measurements("test_yagi_roof_uhf_pitch.csv"))
axs[0][1].plot(*get_measurements("test_yagi_field_uhf_pitch.csv"))

axs[1][1].title.set_text("UHF Yagi Varied Azimuth")
axs[1][1].plot(*get_measurements("test_yagi_roof_uhf_azimuth.csv"))
axs[1][1].plot(*get_measurements("test_yagi_field_uhf_azimuth.csv"))

fmt = lambda x, pos: "{:g}".format(np.degrees(x if x >= 0 and x <= np.pi else 2*np.pi - x))
for ax in [e for l in axs for e in l]:
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt))

fig.legend(("Urban Environment", "Open Field"))

plt.show()
