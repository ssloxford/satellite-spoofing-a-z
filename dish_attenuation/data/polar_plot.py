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
        print(f"opening path {path}")
        df = pandas.read_csv(csvfile, delimiter="\t", index_col=False)

        # bin the measurements
        d = defaultdict(list)
        for row in df.to_dict(orient="records"):
            print(row)
            if "fspl" in row.keys():
                fspl = row["fspl"]
                print(f"adding fspl: {fspl}")
                d[int(row["angle"])].append(calc_vhf(row['measurement'], row['gain']) + int(row["fspl"]))
            else:
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
        measurements = list(map(lambda x: -45 if x-offset < -45 else x-offset, measurements)) # hack for plotting

        #
        angles += list(map(lambda x: -x, angles))[::-1]
        measurements += measurements[::-1]

        return angles, measurements


def single_slit(x, size, wavelength):
    a = (np.sin((np.pi * size * np.sin(x))/wavelength)**2) / ((np.pi * size * np.sin(x))/wavelength)**2
    return 10*np.log10(a)

angles = np.arange(-0.5*np.pi, 0.5*np.pi, 0.001)
plt.plot(angles, np.vectorize(lambda x: single_slit(x, 0.3, 3E8/11.7E9))(angles))
plt.show()

fig, axs = plt.subplots(3, 2, subplot_kw={'projection': 'polar'}, figsize=(8, 9))

axs[0][0].title.set_text("VHF Yagi Varied Elevation")
axs[0][0].plot(*get_measurements("test_yagi_roof_vhf_pitch.csv"))
axs[0][0].plot(*get_measurements("test_yagi_field_vhf_pitch.csv"))

axs[1][0].title.set_text("VHF Yagi Varied Azimuth")
axs[1][0].plot(*get_measurements("test_yagi_roof_vhf_azimuth.csv"))
axs[1][0].plot(*get_measurements("test_yagi_field_vhf_azimuth.csv"))

#axs[2][0].title.set_text("X Band Dish, Varied Azimuth")
#axs[2][0].plot(*get_measurements("test_dish_roof_x_old.csv"))

axs[0][1].title.set_text("UHF Yagi Varied Elevation")
axs[0][1].plot(*get_measurements("test_yagi_roof_uhf_pitch.csv"))
axs[0][1].plot(*get_measurements("test_yagi_field_uhf_pitch.csv"))

axs[1][1].title.set_text("UHF Yagi Varied Azimuth")
axs[1][1].plot(*get_measurements("test_yagi_roof_uhf_azimuth.csv"))
axs[1][1].plot(*get_measurements("test_yagi_field_uhf_azimuth.csv"))


plt.setp(axs, ylim=[-45, 0])


#axs[2][1].title.set_text("Large Dish, Varied Aximuth")
#axs[2][1].plot(*get_measurements("test_bigdish.csv"))

fmt = lambda x, pos: "{:g}".format(np.degrees(x if x >= 0 and x <= np.pi else 2*np.pi - x))
for ax in [e for l in axs for e in l]:
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(fmt))

fig.legend(("Urban Environment", "Open Field"), loc="lower center", bbox_to_anchor=(0.5, 0))
fig.tight_layout()

#plt.savefig("polar.pdf", bbox_inches='tight')
plt.show()
