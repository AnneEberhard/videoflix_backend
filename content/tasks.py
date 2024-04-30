import os
import subprocess


def convert480p(source):
    """
    converts video file into the smaller 480p format
    :param source: The path to the source video file.
    :type source: str
    """
    base_name, ext = os.path.splitext(source)
    new_file_name = base_name + '_480p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd480 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    subprocess.run(cmd, capture_output=True)


def convert720p(source):
    """
    converts video file into the smaller 720p format
    :param source: The path to the source video file.
    :type source: str
    """
    base_name, ext = os.path.splitext(source)
    new_file_name = base_name + '_720p.mp4'
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source, new_file_name)
    subprocess.run(cmd, capture_output=True)
