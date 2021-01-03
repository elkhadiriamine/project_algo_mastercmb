# -*- coding: utf-8 -*-
"""
Created on Sun Oct 25 10:37:29 2020

@author: user
"""
import matplotlib.pyplot as plt
from scipy.fftpack import fft
import librosa 
import speech_recognition as sr
import pyaudio
from googletrans import Translator, constants
from librosa import display
import struct
from pprint import pprint

r=sr.Recognizer()
with sr.Microphone() as source:
    print("go!")
    input_=r.listen(source)
    with open("microphone-results.wav", "wb") as f:
        f.write(input_.get_wav_data())
        try:
            result=r.recognize_google(input_, language="fr-FR")
            print("you said :{} ".format(result))
            translator = Translator() #init our translator
            #translate a text to another language (by default)
            translation = translator.translate(str(result),dest='ar')
            print(translation)
            print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")
        except:
            print("please repeat again")


with open('recognized.txt',mode='w')as file:
    file.write("Recognized_speech:")
    file.write(result)
    print('ready')


def plot_sound(): 
    amplitudes,frequencies=librosa.load("microphone-results.wav") 
    plt.subplot(211) 
    display.waveplot(y=amplitudes,sr=frequencies)
# calcul de la transformee de Fourier et des frequences
    fourier =fft(amplitudes)
# affichage de la transformee de Fourier
    plt.subplot(212)
    plt.plot(fourier)
    plt.grid() 
    plt.xlabel("frequency domaine")
    plt.ylabel("Magnitude")
    plt.legend()
    plt.show()

plot_sound()

amplitudes,frequencies=librosa.load("microphone-results.wav") 
plt.specgram(amplitudes[0:1000000],NFFT=5000,Fs=frequencies,noverlap=400,cmap="magma_r")
plt.colorbar()
plt.show()















