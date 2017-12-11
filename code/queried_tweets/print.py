import matplotlib.pyplot as plt
import numpy as np

import csv
import os
import re

def print_all():
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    for idx, filename in enumerate(os.listdir('predictions')):
        pts = [float(x[1]) for x in csv.reader(open('predictions/'+filename))]
        key = filename.split('_prediction')[0]
    
        plt.subplot(4,4, idx + 1)
        plt.hist(pts, bins=30)
        plt.xlim([-0.2, 1.2])
        avg = np.mean(pts)
        plt.title(re.sub('_', ' ', key) + ' (avg={0:.2f})'.format(avg))
    plt.show()

def get_extremes(n=5, fname='extremes.txt'):
    '''
    returns top n most likely to be positive and negative tweets
    for each key, and saves it in fname
    ''' 

    f = open(fname, 'w')
    for idx, filename in enumerate(os.listdir('predictions')):
        pts = [float(x[1]) for x in csv.reader(open(
                'predictions/'+filename))]

        key = filename.split('_prediction')[0]

        f.write('=====================\n')
        f.write('>>> key: {}\n'.format(key))

        pairs = zip(pts, range(len(pts)))

        pairs.sort()

        pos_idxs = [x[1] for x in pairs[-n:]]

        tweets = [x for x in csv.reader(open(
            'second_pass_preprocess/{}_second_pass.csv'.format(key),'r'))]

        f.write('>>> {} most likely negative\n'.format(n))
        for sentiment, idx in pairs[:n]:
            f.write('({0:.5f}) '.format(sentiment) + tweets[idx][0]+'\n')

        f.write('>>> {} most likely positive\n'.format(n))
        for sentiment, idx in pairs[-n:]:
            f.write('({0:.5f}) '.format(sentiment) + tweets[idx][0]+'\n')

        f.write('\n')

if __name__ == '__main__':
    #print_all()
    get_extremes()
