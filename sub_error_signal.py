import wave
import numpy as np
import scipy.io.wavfile
import scipy.signal
import scipy.fftpack
from pylab import *
from lpc import *

wav1, fs1 = wavread("voice_compare1.wav")
wav2, fs2 = wavread("voice_compare2.wav")

nfft = 4096   # FFTのサンプル数
tfft = 512
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
    s1 = preEmphasis(s1, p)
    s2 = preEmphasis(s2, p)
    # ハミング窓をかける
    hammingWindow = np.hamming(len(s1))
    s1 = s1 * hammingWindow
    hammingWindow = np.hamming(len(s2))
    s2 = s2 * hammingWindow

    # LPC係数を求める
    r1 = autocorr_fft(s1)
    a1, e1  = LevinsonDurbin(r1, lpcOrder)
    r2 = autocorr_fft(s2)
    a2, e2  = LevinsonDurbin(r2, lpcOrder)

    # 残差信号
    error1 = errorSignal(s1,a1)
    error2 = errorSignal(s2,a2)

    """
    spec1 = np.abs(np.fft.fft(error1))
    spec1 /= nfft
    logspec1 = 20 * np.log10(spec1)
    #plot(fscale, logspec1, "g", linewidth=2)

    spec2 = np.abs(np.fft.fft(error2))
    spec2 /= nfft
    logspec2 = 20 * np.log10(spec2)
    #plot(fscale, logspec2, "r", linewidth=2)
    """

    error1 = preEmphasis(error1, p)
    error2 = preEmphasis(error2, p)

    hammingWindow = np.hamming(len(error1))
    error1 = error1 * hammingWindow
    hammingWindow = np.hamming(len(error2))
    error2 = error2 * hammingWindow

    er1 = autocorr_fft(error1)
    er2 = autocorr_fft(error2)

    ae1, ee1 = LevinsonDurbin(er1, lpcOrder)
    ae2, ee2 = LevinsonDurbin(er2, lpcOrder)

    w1, h1 = scipy.signal.freqz(1.0, ae1, nfft, "whole")
    lpcspec1 = np.abs(h1)
    lpcspec1 /= nfft
    loglpcspec1 = 20 * np.log10(lpcspec1)
    plot(fscale, loglpcspec1, "g", linewidth=4)

    w2, h2 = scipy.signal.freqz(1.0, ae2, nfft, "whole")
    lpcspec2 = np.abs(h2)
    lpcspec2 /= nfft
    loglpcspec2 = 20 * np.log10(lpcspec2)
    plot(fscale, loglpcspec2, "r", linewidth=2)

    #sub += np.sqrt(pow((logspec1 - logspec2), 2))
    sub += np.sqrt(pow((loglpcspec1 - loglpcspec2), 2))
    
    
    xlim((0, fs1/2))
    ylim((-120,0))
    #ylim((-50.0, 50.0))
    pause(.001)
    cla()
    


"""
sub /= length
xlim((0, fs1/2))
ylim((0,max(sub)))
plot(fscale, sub, "g", linewidth=2)
show()
"""
