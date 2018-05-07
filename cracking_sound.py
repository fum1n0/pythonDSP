# coding:utf-8

import os
import argparse
import sys
import wave
import numpy as np
import scipy.io.wavfile
import scipy.signal as sig


parser = argparse.ArgumentParser(description='')
parser.add_argument('--data_path', dest='data_path',
                    default='source.wav', help='path of the wav data')
parser.add_argument('--multi', dest='multi', type=float,
                    default=10.0, help='multi amp rate')
args = parser.parse_args()


def wavread(filename):
    wf = wave.open(filename, "r")
    fs = wf.getframerate()
    data = wf.readframes(wf.getnframes())
    if wf.getnchannels() == 2:
        x = np.frombuffer(data, dtype="int16") / 32768.0  # (-1, 1)に正規化
        left = x[::2]
        right = x[1::2]
        x = (left + right)/2.0
    else:
        x = np.frombuffer(data, dtype="int16") / 32768.0  # (-1, 1)に正規化
    wf.close()
    return x, float(fs)


def writeWave(signal, sf, name="write", multi=1.0):

    mx = max(max(signal), abs(min(signal)))
    if multi == 1.0:
        if 1.0 < mx:
            signal *= 32768.0/mx
        else:
            signal *= 32768.0
    else:
        signal *= 32768.0 * multi

    signal = signal.astype(np.int16)
    save_wav = wave.Wave_write(name+".wav")
    save_wav.setnchannels(1)
    save_wav.setsampwidth(2)
    save_wav.setframerate(sf)
    save_wav.writeframes(signal)
    save_wav.close()


if __name__ == "__main__":

    if not os.path.exists(args.data_path):
        print("wrong data path")
        sys.exit()

    check_wav = args.data_path[-4:]

    if check_wav != ".wav":
        print("not wav file")
        sys.exit()

    wav, fs = wavread(args.data_path)
    writeWave(wav, fs, os.path.basename(
        args.data_path[:-4])+"_cracking", args.multi)
