#coding:utf-8

from signal_function import *
from pylab import *

if __name__ == "__main__":

    args = sys.argv # 音声ファイルのパス

    # 音声をロード
    wav, fs = wavread(args[1])
    
    nfft = 1024   # FFTのサンプル数
    tfft = 512
    lpcOrder = 46 # lpc次数
    p = 0.97         # プリエンファシス係数

    length = (int)((len(wav)-nfft)/tfft)

    signal = np.zeros(len(wav))
    error_signal = np.zeros(len(wav))
    pulse_signal = np.zeros(len(wav))

    for l in range(length):
        print(100.0*l/length)
        
        # 音声波形を切り出す
        s = wav[l*tfft : l*tfft+nfft]
        
       # ハミング窓をかける
        hammingWindow = np.hamming(len(s))
        s = s * hammingWindow

        # LPC係数を求める
        r = autocorr_fft(s)
        a, e  = LevinsonDurbin(r, lpcOrder)

        
        # 残差信号
        error = errorSignal(s,a)
        for i in range(0, len(error)):
            error_signal[(int)(tfft*l+i)] += error[i]
        

        # ピッチ周波数計算
        r_error = autocorr_fft(error)
        freq = calcPitchFreq(r_error, fs)

        # パルス波生成
        pulse = createPulse(freq, fs, len(s))
        #pulse *= np.average(np.absolute(error))
        pulse *= np.max(np.absolute(error))
        for i in range(0, len(pulse)):
            pulse_signal[(int)(tfft*l+i)] += pulse[i]
        
        # 値出力
        """
        for i in range(0, nfft):
            for j in range(1,len(a)):
                if j <= i :
                    error[i] -=  a[j] * error[i - j]
            
            signal[(int)(tfft*l+i)] += error[i]
        """

        for i in range(0, nfft):
            for j in range(1,len(a)):
                if j <= i :
                    pulse[i] -=  a[j] * pulse[i - j]
            
            signal[(int)(tfft*l+i)] += pulse[i]

        
    # 書き出し
    writeWave(error_signal, fs, "wav/error")
    writeWave(pulse_signal, fs, "wav/pulse")
    writeWave(signal, fs, "wav/lpc_vocoder")