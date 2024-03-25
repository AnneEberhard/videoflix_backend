import os
import subprocess

def convert480p(source):   
    base_name, ext = os.path.splitext(source)
    new_file_name = base_name + '_480p.mp4'
    
    cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
    run = subprocess.run(cmd, capture_output=True)


def convert720p(source):    
    base_name, ext = os.path.splitext(source)
    new_file_name = base_name + '_720p.mp4'
    cmd = 'C:\\usr\\ffmpeg\\bin\\ffmpeg.exe -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)    
    run = subprocess.run(cmd, capture_output=True)
