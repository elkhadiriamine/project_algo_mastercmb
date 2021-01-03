# -*- coding: utf-8 -*-
"""
Created on Sun Jan  3 14:42:39 2021

@author: user
"""


import ffmpeg
import os,subprocess
import numpy as np
import speech_recognition as sr
import shlex

local_path = os.getcwd()
if os.path.exists(str(local_path) + "/output.mp4"):
    os.remove(str(local_path) + "/output.mp4")

cmd_video=('ffmpeg -f dshow -t 18 \
-i video="Integrated Camera":audio="Mikrofonarray (Intel® Smart Sound Technologie)" \
 -s 640x360 output.mp4')
process_recording = subprocess.Popen(cmd_video,shell=True)
process_recording.wait()


filename = 'output.mp4'
split_length = 6
logo = ffmpeg.input('logo.png')
for n in range(3):
        split_start = split_length * n
        pth, ext = filename.rsplit(".", 1)
        cmd = "ffmpeg -i {} -map 0 -ss {} -t {} {}-{}.{}".\
            format(filename, split_start, split_length, pth, n, ext)
        #process_split = subprocess.check_call(shlex.split(cmd), universal_newlines=True)
        process_split = subprocess.Popen(shlex.split(cmd), shell=True)
        process_split.wait()
        
        if os.path.exists(str(local_path) + "/audio.wav"):
            os.remove(str(local_path) + "/audio.wav")
        
        cmd = "ffmpeg -i {}-{}.{} -ab 160k -ac 2 -ar 44100 -vn audio.wav".\
            format(pth, n, ext, n)
        process_audio = subprocess.Popen(shlex.split(cmd), shell=True)
        process_audio.wait()
        r = sr.Recognizer()
        with sr.AudioFile('audio.wav') as source:
            audio = r.record(source)  # read the entire audio file
        subtitle = r.recognize_google(audio, language="fr-FR")
        
        finalfile = 'final-' + str(n) + '.mp4'
        stream = ffmpeg.input('output-{}.mp4'.\
            format(n))        
        stream = stream.overlay(logo)
        stream = stream.drawtext(
                fontsize='14',
                start_number=0,
                text=subtitle,
                fontcolor='yellow',
                escape_text=True,
                x=40,
                y=310)
        stream = ffmpeg.output(stream, finalfile)
        ffmpeg.run(stream)

stream_audio = ffmpeg.input('output.mp4').audio
split0 = ffmpeg.input('final-0.mp4')
split1 = ffmpeg.input('final-1.mp4')
split2 = ffmpeg.input('final-2.mp4')

if os.path.exists(str(local_path) + "/final.mp4"):
    os.remove(str(local_path) + "/final.mp4")

(
    ffmpeg
    .concat(split0, split1, split2)
    .output(stream_audio, 'final.mp4')
    .run()
)

if os.path.exists(str(local_path) + "/audio.wav"):
    os.remove(str(local_path) + "/audio.wav")
for n in range(3):
    if os.path.exists(str(local_path) + "/final-" + str(n) + ".mp4"):
        os.remove(str(local_path) + "/final-" + str(n) + ".mp4")
    if os.path.exists(str(local_path) + "/output-" + str(n) + ".mp4"):
        os.remove(str(local_path) + "/output-" + str(n) + ".mp4")

cmd_video=('ffplay final.mp4')
process_recording = subprocess.Popen(cmd_video,shell=True)
process_recording.wait()