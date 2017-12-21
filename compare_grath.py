#coding:utf-8
import wave
import numpy as np
import scipy.io.wavfile
import scipy.signal
import scipy.fftpack
from pylab import *
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import csv
from lpc_net import LpcNet


if __name__ == "__main__":


    x_test = []
    t_test = []

    xte = open('test_x.csv', 'r')
    reader = csv.reader(xte)
    for row in reader:
        x_test.append(row)
    xte.close()

    tte = open('test_t.csv', 'r')
    reader = csv.reader(tte)
    for row in reader:
        t_test.append(row)
    tte.close()

    x_test = (np.array(x_test)).astype(np.float32)
    t_test = (np.array(t_test)).astype(np.float32)

    network = LpcNet(input_size=116, output_size=46, hidden_size=100)
    network.load_params()

    nfft = 1024
    fs = 44100
    fscale = []
    for i in range(nfft):
        fscale.append(i*fs/nfft)

    sub = np.zeros(47)

    for l in range(0, x_test.shape[0]):
        
        t = np.insert(t_test[l], 0, 1)
        """
        w1 ,h1 = scipy.signal.freqz(1.0, t, nfft, "whole")
        aspec = np.abs(h1)
        aspec /= nfft
        logaspec = 20 * np.log10(aspec)
        plot(fscale, logaspec, "g", linewidth=4)
        #plot(logaspec, "g", linewidth=2)
        """

        x = np.array([x_test[l]])
        x = x.astype(np.float32)
        x.transpose()
        net_a = network.predict(x)
        net_a = np.insert(net_a, 0, 1)
       
        """
        w2, h2 = scipy.signal.freqz(1.0, net_a, nfft, "whole")
        netspec = np.abs(h2)
        netspec /= nfft
        lognetspec = 20 * np.log10(netspec)
        plot(fscale, lognetspec, "r", linewidth=2)
        """

        """
        xlim((0, fs/2))
        ylim((-90,0))
        pause(.01)
        cla()
        """
        
        sub += sqrt(pow((t-net_a),2))
    
    sub /= t_test.shape[0]
    plot(sub)
    show()
    













