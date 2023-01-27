import csv
import matplotlib.pyplot as plt
import numpy as np


def fitPlaneLTSQ(XYZ):
    (rows, cols) = XYZ.shape
    G = np.ones((rows, 3))
    G[:, 0] = XYZ[:, 0]  #X
    G[:, 1] = XYZ[:, 1]  #Y
    Z = XYZ[:, 2]
    (a, b, c),resid,rank,s = np.linalg.lstsq(G, Z)
    return (a,b,c)


data = []
with open("./test_2.csv", 'r') as file:
  csvreader = csv.reader(file, delimiter='\t')
  for row in csvreader:
    drow = [float(s) for s in row[3:6]]
    if drow[2] > 0.001:
        data.append(drow)

data = np.array(data)

data[:,0] = data[:,0]
data[:,2] = np.log10(data[:,2])

a,b,c = fitPlaneLTSQ(data)

print(a, b, c)

print("Rx(dBm) = " + str(1/a) + " * log10(amplitude) - "+ str(b/a) + " * gain - "+ str(c/a))

plt.figure(figsize=(8,12))
plt.scatter(data[:,0], data[:,1], c=data[:,0]-(data[:,2]/a - b/a*data[:,1] - c/a))
plt.colorbar()
plt.show()