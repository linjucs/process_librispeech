import os
import sys
import ffmpeg

file1 = open('text', 'r') 
Lines = file1.readlines()
hashmap = {}
for line in Lines:
     list_ = line.split(' ', 1)
     hashmap[list_[0]] = list_[1] 
root = 'train-clean-360_mixed'
spks = os.listdir(root)
spks = sorted(spks)
f = open("wav.scp", "a")
u2s = open("utt2spk", 'a')
txt = open("new_text", 'a')
for spk in spks:
    spk_list = os.listdir(root + '/' + spk)
    spk_list = sorted(spk_list)
    for wav_dir in spk_list:
        wav_list = os.listdir(root + '/' + spk + '/' + wav_dir)
        wav_list = sorted(wav_list)
        for wav in wav_list:
            flac = root + '/' + spk + '/' + wav_dir + '/' + wav
            if flac.endswith(".wav"):
                #986-129388-0101
                #100-121669-0011 100-121669
                names = wav.split('_')
                f.write(wav[:-4] + ' ' + './corpus_libri/LibriSpeech'+ '/' + flac + '\n')
                u2s.write(wav[:-4] + ' ' + names[0][:-5] + '\n')
                txt.write(wav[:-4] + ' ' + hashmap[names[0]])
f.close()
u2s.close()
txt.close()
