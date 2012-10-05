#!/usr/bin/env python
"""

Set terminal tab / decoration color by the server name.

Get a random colour which matches the server name and use it for the tab colour
Benefit is that each server gets a distinct color which you do not need
to configure beforehand.

"""
import colorsys
import contextlib
import pickle
import random
import socket
import sys

__credits__ = ["Mikko Ohtamaa", "Antti Haapala"]

USAGE = """
Colorize terminal tab based on the current host name.

Usage: rainbow-parade.py [0-1.0] [0-1.0] # Lightness and saturation values

An iTerm 2 example (recolorize dark grey background and black text):

    rainbow-parade.py 0.7 0.4
"""
color_dict = {}

FILENAME = 'colors'

def load_colordict(path):
    try:
        with contextlib.closing(open(path + FILENAME, 'r')) as color_file:
            return pickle.load(color_file)
    except IOError:
        return {}


def save_color(path, name, color):
    color_dict[name] = color
    with contextlib.closing(open(path + FILENAME, 'w')) as color_file:
        pickle.dump(color_dict, color_file,)

def get_random_by_string(s):
    """
    Get always the same 0...1 random number based on an arbitrary string
    """
    random.seed(s)
    return random.random()


def decorate_terminal(color):
    """
    Set terminal tab / decoration color.
    Please note that iTerm 2 only
    """

    r, g, b = color
    sys.stdout.write("\033]6;1;bg;red;brightness;%d\a" % int(r * 255))
    sys.stdout.write("\033]6;1;bg;green;brightness;%d\a" % int(g * 255))
    sys.stdout.write("\033]6;1;bg;blue;brightness;%d\a" % int(b * 255))
    sys.stdout.flush()

def colorize_border(path, name):
    """
    Colorize terminal tab by your server name.
    """
    value = get_color(path, name)

    color = colorsys.hls_to_rgb(value, value, value)
    
    decorate_terminal(color)

def get_color(path, name):
    color_dict = load_colordict(path)

    color =  color_dict.get(name, None)
    if not color:
        color = get_random_by_string(name)
        save_color(path, name, color)
    return color

def main():
    """
    From Toholampi with love http://www.toholampi.fi/tiedostot/119_yleisesite_englanti_naytto.pdf
    """
    name = socket.gethostname() 
    if len(sys.argv) > 1:
        path = sys.argv[1]

    colorize_border(path, name)


if __name__ == "__main__":
    main()
