import matplotlib.pyplot as plt

import csv
import os

for idx, filename in enumerate(os.listdir('predictions')):
    pts = [float(x[1]) for x in csv.reader(open('predictions/'+filename))]
    key = filename.split('_')[0]

    plt.subplot(3,4, idx + 1)
    plt.hist(pts, bins=30)
    plt.title(key)
plt.show()
