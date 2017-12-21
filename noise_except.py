#coding:utf-8

from pylab import *
from signal_function import *

if __name__ == "__main__":

    w, fs = wavread("noise.wav")
    writeWave(w, fs, "mono")
    nframe = 1024
    tframe = 512

    length = int((len(w) - tframe)/tframe)

    e = np.zeros(len(w))
   
    for l in range(0,length):
        signal = w[l*tframe : l*tframe + nframe]
        hammingWindow = np.hamming(len(signal))
        signal = signal * hammingWindow

        auto = sig.correlate(signal, signal, "same") 
        #auto /= len(signal)

        for i in range(0, nframe):
            e[l*tframe + i] += auto[i]


    writeWave(signal=e, sf=fs)
   
