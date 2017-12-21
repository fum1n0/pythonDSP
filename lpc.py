#coding:utf-8

import os
from signal_function import *
from pylab import *


if __name__ == "__main__":
    print(os.getcwd())
    # 音声をロード
    wav, fs = wavread("lpc.wav")
    #t = np.arange(0.0, len(wav) / fs, 1/fs)

    nfft = 1024   # FFTのサンプル数
    tfft = 512
    lpcOrder = 46 # lpc次数
    p = 0.97         # プリエンファシス係数
    fscale = []
    for i in range(nfft):
        fscale.append(i*fs/nfft)

    length = (int)((len(wav)-nfft)/tfft)
   
    for l in range (0,length):
        # 音声波形を切り出す
        s = wav[l*tfft : l*tfft+nfft]
        #s = wav[90624: 90624+nfft]
    
        # プリエンファシスフィルタをかける
        #s = preEmphasis(s, p)

        # ハミング窓をかける
        hammingWindow = np.hamming(len(s))
        s = s * hammingWindow

        # LPC係数を求める
        #r = autocorr(s, lpcOrder + 1)
        r = autocorr_fft(s)
        a, e  = LevinsonDurbin(r, lpcOrder)

        #print("*** result ***")
        #print("a:")
        #print(a)
        #print("e:")
        #print(e)

        # オリジナル信号の対数スペクトル
        spec = np.abs(np.fft.fft(s))
        spec /= nfft
        logspec = 20 * np.log10(spec+1e-10)
        plot(fscale, logspec, "b", linewidth=1)
        #plot(logspec)

        # LPC対数スペクトル
        w, h = scipy.signal.freqz(np.sqrt(e+1e-10), a+1e-10, nfft, "whole")
        lpcspec = np.abs(h)
        lpcspec /= nfft
        loglpcspec = 20 * np.log10(lpcspec+1e-10)
        plot(fscale, loglpcspec, "r", linewidth=2)
        #plot(loglpcspec, "r", linewidth=4)

        l ,s = scipy.signal.freqz(1.0, a+1e-10, nfft, "whole")
        aspec = np.abs(s)
        aspec /= nfft
        logaspec = 20 * np.log10(aspec+1e-10)
        plot(fscale, logaspec, "g", linewidth=1)
        #plot(logaspec, "g", linewidth=2)

        xlim((0, fs/2))
        ylim((-90,0))
        #xlim((0, nfft/2))
        #show()
        pause(.01)
        cla()