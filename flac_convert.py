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
parser.add_argument('--tag_ex', dest='tag_ex',
                    default='m4a', help='ectension of the tag file')
parser.add_argument('--move_tag', dest='move_tag', type=bool,
                    default='False', help=' move tag file to tag dir')
parser.add_argument('--move_wav', dest='move_wav', type=bool,
                    default='False', help=' move wav file to tag dir')

args = parser.parse_args()

if __name__ == '__main__':

    # file dir path
    tag_dir = '{}/{}'.format(args.data_dir, args.tag_ex)
    wav_dir = '{}/wav'.format(args.data_dir)
    flac_dir = '{}/flac'.format(args.data_dir)

    # tag dir path check
    if not os.path.exists(tag_dir):
        os.mkdir(tag_dir)

    if args.move_tag:  # move tag file to tag dir
        from_path = '{}/*.{}'.format(args.data_dir, args.tag_ex)
        to_path = '{}/'.format(tag_dir)
        cli_args = ['mv', from_path, to_path]
        try:
            subprocess.check_output(cli_args)
        except:
            print("not move " + args.tag_ex + " file")

    # wav dir path check
    if not os.path.exists(wav_dir):
        os.mkdir(wav_dir)

    if args.move_wav:  # move wav file to wav dir
        from_path = '{}/*.wav'.format(args.data_dir)
        to_path = '{}/'.format(wav_dir)
        cli_args = ['mv', from_path, to_path]
        try:
            subprocess.check_output(cli_args)
        except:
            print('not move wav file')

    # flac dir check
    if not os.path.exists(flac_dir):
        os.mkdir(flac_dir)

    # file path glob
    tag_path = glob('{}/*.{}'.format(tag_dir, args.tag_ex))
    wav_path = glob('{}/*.wav'.format(wav_dir))
    flac_path = []
    for path in tag_path:
        flac_path.append('{}/'.format(flac_dir) +
                         os.path.basename(path[:-4]) + '.flac')

    if len(tag_path) != len(wav_path):
        print('no match num {},wav'.format(args.tag_ex))
        os.sys.exit()

    print(wav_path)
    print(flac_path)

    # output cover image
    cli_args = ['ffmpeg', '-i', tag_path[0], 'cover.jpg']
    try:
        subprocess.check_output(cli_args)
    except:
        print("not output cover")

    # convert
    for i in range(len(wav_path)):

        # convert wav file to flac
        cli_args = ['ffmpeg', '-i', wav_path[i], '-ac',
                    '2', '-acodec', 'flac', flac_path[i]]
        try:
            subprocess.check_output(cli_args)
        except:
            print("wav to flac error")

        # convert tag file to flac
        cli_args = ['ffmpeg', '-i', tag_path[i], '-ac',
                    '2', '-acodec', 'flac', 'tag.flac']
        try:
            subprocess.check_output(cli_args)
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

        # remove flac tag file
        cli_args = ['rm', './tag.flac']
        try:
            subprocess.check_output(cli_args)
        except:
            print("remove tag flac error")

    # remove cover image
    cli_args = ['rm', './cover.jpg']
    try:
        subprocess.check_output(cli_args)
    except:
        print("remove cover image error")

    print("all convert success")
