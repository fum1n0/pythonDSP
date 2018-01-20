#coding:utf-8

from signal_function import *
from pylab import *

if __name__ == "__main__":

    args = sys.argv # 音声ファイルのパス
    num = len(args) - 1

    wav_list = []
    fs_list = []
    length_list = [] 

    # 音声をロード
    if(len(args)<=2):
        print("no mix")
        sys.exit()
    else:
        for i in range(1,len(args)):
            wav, fs = wavread(args[i])
            # 正規化
            wav = wav * (1.0/num) * np.amax(np.absolute(wav))
            length_list.append(len(wav))
            wav_list.append(wav.tolist())
            fs_list.append(fs)
    
    # 0 padding
    max_length = max(length_list)
    for i in range(num):
        if i != np.argmax(np.array(length_list)):
            length = len(wav_list[i])
            for j in range (length, max_length):
                wav_list[i].append(0)

    # mix
    signal = np.sum(np.array(wav_list), axis=0)

    # write
    print("len: " + str(len(signal)/min(fs_list)) + "[sec]")
    print("fs: " + str(min(fs_list)))
    writeWave(signal, min(fs_list), name="wav/mix")






