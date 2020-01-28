import os
import sys
import ffmpeg
root = 'train-clean-360_noise'
spks = os.listdir(root)


for spk in spks:
    spk_list = os.listdir(root + '/' + spk)
    for wav_dir in spk_list:
        wav_list = os.listdir(root + '/' + spk + '/' + wav_dir)
        for wav in wav_list:
            flac = root + '/' + spk + '/' + wav_dir + '/' + wav
            wav = root + '/' + spk + '/' + wav_dir + '/' + wav[:-4]+'wav'
            if flac.endswith(".flac"):
                os.system('ffmpeg -n -i ' + flac + ' ' +  wav)
