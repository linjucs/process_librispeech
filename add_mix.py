import os
import soundfile
import numpy as np
import argparse
import csv
import time
from scipy import signal
#import pickle
#import cPickle
import h5py
import glob
import shutil
import uuid
import random


def read_audio(path, target_fs=None):
    (audio, fs) = soundfile.read(path)
    if audio.ndim > 1:
        audio = np.mean(audio, axis=1)
    if target_fs is not None and fs != target_fs:
        audio = librosa.resample(audio, orig_sr=fs, target_sr=target_fs)
        fs = target_fs
    return audio, fs


def write_audio(path, audio, sample_rate):
    soundfile.write(file=path, data=audio, samplerate=sample_rate)



def get_amplitude_scaling_factor(s, n, snr, method='rms'):
    original_sn_rms_ratio = rms(s) / rms(n)
    target_sn_rms_ratio =  10. ** (float(snr) / 20.)    # snr = 20 * lg(rms(s) / rms(n))
    signal_scaling_factor = target_sn_rms_ratio / original_sn_rms_ratio
    return signal_scaling_factor


def additive_mixing(s, n):
    mixed_audio = s + n
    alpha = 1. / np.max(np.abs(mixed_audio))
    mixed_audio *= alpha
    s *= alpha
    n *= alpha
    return mixed_audio, s, n, alpha

def rms(y):
    return np.sqrt(np.mean(np.abs(y) ** 2, axis=0, keepdims=False))


noise_list = os.listdir("./noise_100_16k")  
fs = 16000
snr_list = [-5, 5, 0, 10, 15]
if __name__ == '__main__':
    root = 'train-clean-360_noise'
    out_root = 'train-clean-360_mixed'
    spks = os.listdir(root)
    for spk in spks:
        spk_list = os.listdir(root + '/' + spk)
        for wav_dir in spk_list:
            wav_list = os.listdir(root + '/' + spk + '/' + wav_dir)
            for wav in wav_list:
                if wav.endswith(".wav"):
                    random_num1 = random.randrange(0,len(noise_list))
                    random_num2 = random.randrange(0,len(snr_list))
                    wav_file = root + '/' + spk + '/' + wav_dir + '/' + wav
            
                    noise_path = os.path.join("./noise_100_16k/"+noise_list[random_num1])
                    noise_audio, _ = read_audio(noise_path, target_fs = fs)
                    speech_audio, _ = read_audio(wav_file, target_fs = fs)
                    noise_offset = speech_audio.shape[0]

                    if len(noise_audio) < len(speech_audio):
                        n_repeat = int(np.ceil(float(len(speech_audio)) / float(len(noise_audio))))
                        noise_audio_ex = np.tile(noise_audio, n_repeat)
                        noise_audio = noise_audio_ex[0 : len(speech_audio)]        
                    else:
                        noise_audio = noise_audio[0 : noise_offset]
                    scaler = get_amplitude_scaling_factor(speech_audio, noise_audio, snr= snr_list[random_num2])
                    speech = speech_audio * scaler
                    noise_audio = noise_audio.copy()
                    (mixed_audio, speech_audio, noise_audio, alpha) = additive_mixing(speech, noise_audio)
                    outdir = out_root + '/'  + spk + '/' + wav_dir
                    os.makedirs(outdir, exist_ok = True)
                    out_name =  wav[:-4] + '_' + noise_list[random_num1][:-4] + '_' + str(snr_list[random_num2]) + '.wav'
                    print("Processing ....", out_name)
                    write_audio(os.path.join(outdir + "/" + out_name), mixed_audio, fs) 
