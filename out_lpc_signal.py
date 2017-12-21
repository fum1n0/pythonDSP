
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import matplotlib.pyplot as plt
from signal_function import *


if __name__ == "__main__":

    args = sys.argv

    # 音声をロード
    wav, fs = wavread(args[1])
    
    nfft = 1024   # FFTのサンプル数
    tfft = 512
    lpcOrder = 46 # lpc次数
    p = 0.97         # プリエンファシス係数
  
    length = (int)((len(wav)-nfft)/tfft)

    signal = np.zeros(len(wav))
    error_signal = np.zeros(len(wav))
   
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
    
        # 値出力
        for i in range(0, nfft):
            for j in range(1,len(a)):
                if j <= i :
                    error[i] -=  a[j] * error[i - j]
            
            signal[(int)(tfft*l+i)] += error[i]

    # 書き出し
    writeWave(error_signal, fs, "error")
    writeWave(signal, fs, "a")



