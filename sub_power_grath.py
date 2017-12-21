import wave
import numpy as np
import scipy.io.wavfile
import scipy.signal
import scipy.fftpack
from pylab import *
from signal_function import *

wav1, fs1 = wavread("voice_compare1.wav")
wav2, fs2 = wavread("voice_compare2.wav")

nfft = 2048   # FFTのサンプル数
tfft = 1024
lpcOrder = 46 # lpc次数
p = 0.97         # プリエンファシス係数
fscale = []
for i in range(nfft):
    fscale.append(i*fs1/nfft)

length = (int)((len(wav1)-nfft)/tfft)
sub = np.zeros(nfft)

for l in range (0,length):
    s1 = wav1[l*tfft : l*tfft+nfft]
    s2 = wav2[l*tfft : l*tfft+nfft]
    
    # プリエンファシスフィルタをかける
    #s1 = preEmphasis(s1, p)
    #s2 = preEmphasis(s2, p)
    # ハミング窓をかける
    hammingWindow = np.hamming(len(s1))
    s1 = s1 * hammingWindow
    hammingWindow = np.hamming(len(s2))
    s2 = s2 * hammingWindow

    # LPC係数を求める
    #r = autocorr(s, lpcOrder + 1)
    r1 = autocorr_fft(s1)
    a1, e1  = LevinsonDurbin(r1, lpcOrder)
    r2 = autocorr_fft(s2)
    a2, e2  = LevinsonDurbin(r2, lpcOrder)

    # LPC対数スペクトル
    w1, h1 = scipy.signal.freqz(np.sqrt(e1), a1, nfft, "whole")
    lpcspec1 = np.abs(h1)
    lpcspec1 /= nfft
    loglpcspec1 = 20 * np.log10(lpcspec1)
    #plot(fscale, loglpcspec1, "g", linewidth=4)

    w2, h2 = scipy.signal.freqz(np.sqrt(e2), a2, nfft, "whole")
    lpcspec2 = np.abs(h2)
    lpcspec2 /= nfft
    loglpcspec2 = 20 * np.log10(lpcspec2)
    #plot(fscale, loglpcspec2, "r", linewidth=2)
    
    sub += pow((loglpcspec1 - loglpcspec2), 2)

    #xlim((0, fs1/2))
    #ylim((-90,0))
    #pause(.001)
    #cla()

#cla()
sub /= length
xlim((0, fs1/2))
ylim((0,max(sub)))
plot(fscale, sub, "g", linewidth=2)
show()

