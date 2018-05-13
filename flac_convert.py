# coding: utf-8

import os
from glob import glob
import numpy as np
import subprocess
import argparse

from mutagen.flac import FLAC
from mutagen.flac import Picture as fimg
from mutagen.mp4 import MP4

parser = argparse.ArgumentParser(description='')
parser.add_argument('--data_dir', dest='data_dir',
                    default='.', help='path of the music data')
args = parser.parse_args()

if __name__ == '__main__':

    m4a_dir = '{}/m4a'.format(args.data_dir)
    wav_dir = '{}/wav'.format(args.data_dir)
    flac_dir = '{}/flac'.format(args.data_dir)

    if not os.path.exists(m4a_dir):
        print("Not m4a directory")
        os.sys.exit()

    if not os.path.exists(wav_dir):
        print("Not m4a directory")
        os.sys.exit()

    if not os.path.exists(flac_dir):
        os.mkdir(flac_dir)

    m4a_path = glob('{}/*.m4a'.format(m4a_dir))
    wav_path = glob('{}/*.wav'.format(wav_dir))
    flac_path = []

    for path in m4a_path:
        flac_path.append('{}/'.format(flac_dir) +
                         os.path.basename(path[:-4]) + '.flac')

    if len(m4a_path) != len(wav_path):
        print("no match m4a,wav")
        os.sys.exit()

    print(wav_path)
    print(flac_path)

    args = ['ffmpeg', '-i', m4a_path[0], 'cover.jpg']
    try:
        subprocess.check_output(args)
    except:
        print("not output cover")

    for i in range(len(wav_path)):
        args = ['ffmpeg', '-i', wav_path[i], '-ac',
                '2', '-acodec', 'flac', flac_path[i]]
        try:
            subprocess.check_output(args)
        except:
            print("wav to flac error")

        args = ['ffmpeg', '-i', m4a_path[i], '-ac',
                '2', '-acodec', 'flac', 'tag.flac']
        try:
            subprocess.check_output(args)
        except:
            print("convert tag flac error")

        # read tag info
        tag_info = FLAC('tag.flac')
        key_list = tag_info.keys()

        # write tag info
        audio_flac = FLAC(flac_path[i])
        audio_flac.clear()
        for key in key_list:
            audio_flac[key] = tag_info[key]

        # write cover image info
        img = fimg()
        img.type = 3
        img.mime = 'image/jpg'
        img.desc = 'front cover'
        img.colors = 0
        img.data = open('cover.jpg', mode='rb').read()
        audio_flac.add_picture(img)

        # save music info
        audio_flac.save()

        # remove cover image
        args = ['rm', './tag.flac']
        try:
            subprocess.check_output(args)
        except:
            print("remove tag flac error")

    # remove cover image
    args = ['rm', './cover.jpg']
    try:
        subprocess.check_output(args)
    except:
        print("remove cover image error")

    print("all convert success")
