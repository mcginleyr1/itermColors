#!/usr/bin/env python
"""

Set terminal tab / decoration color by the server name.

Get a random colour which matches the server name and use it for the tab colour
Benefit is that each server gets a distinct color which you do not need
to configure beforehand.

"""
import contextlib
import pickle
import random
import socket
import sys

import husl

__credits__ = ["Mikko Ohtamaa", "Antti Haapala"]

USAGE = """
Colorize terminal tab based on the current host name.

Usage: rainbow-parade.py PATH NAME 

"""
color_dict = {}

FILENAME = 'colors'

def load_colordict(path):
    try:
        with contextlib.closing(open(path + FILENAME, 'r')) as color_file:
            return pickle.load(color_file)
    except IOError:
        return {}


def save_color(path, name, hsl):
    color_dict[name] = hsl
    with contextlib.closing(open(path + FILENAME, 'w')) as color_file:
        pickle.dump(color_dict, color_file,)

def get_random_by_string(s):
    """
    Get always the same 0...1 random number based on an arbitrary string
    """
    random.seed(s)
    return (random.randint(0, 360), random.randint(0, 100), random.randint(0, 100))


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
    H, S, L = get_color(path, name)
    
    color = husl.husl_to_rgb(H, S, L)
   
    decorate_terminal(color)

def get_color(path, name):
    color_dict = load_colordict(path)

    hsl =  color_dict.get(name, None)
    if not hsl:
        hsl = get_random_by_string(name)
        save_color(path, name, hsl)
    return hsl 

def main():
    """
    based on http://www.toholampi.fi/tiedostot/119_yleisesite_englanti_naytto.pdf
    """
    name = socket.gethostname() 
    if len(sys.argv) > 1:
        path = sys.argv[1]

    if len(sys.argv) > 2:
        name = sys.argv[2]

    colorize_border(path, name)


if __name__ == "__main__":
    main()
