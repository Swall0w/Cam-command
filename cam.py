#!/usr/bin python
# -*- coding: utf-8 -*-
from PIL import Image
import sys
import os
import math
import argparse

def get_terminal_size():
    terminal_size = os.popen('stty size').read().split()
    # return the sizes in list
    return terminal_size

def set_parameter_string(default, IsTrueValue):
    '''
        Initializing parameter with default value or True value.
        If the IsTrueValue is None, initialize with default value.
        Or not, initialize with IsTrueValue
    '''
    return IsTrueValue if IsTrueValue else default

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Show some image files')
    parser.add_argument(dest='filenames', metavar='filename', nargs='*')
    parser.add_argument('-s','--split', dest='splits', action='store', help='Value of display splitting by input images. Type an integer number.')
    parser.add_argument('-p', '--pat', dest='pattern', action='store', help='A displayed mark. The default  parameter is a white space.')

    args = parser.parse_args()

    img = Image.open(args.filenames[0])
    imgW = img.size[0]
    imgH = img.size[1]
    imgh = img.size[1]

    TerminalSize = get_terminal_size()
    terminaly = int(TerminalSize[0])
    terminalx = int(TerminalSize[1])

    img = img.resize(( imgW, round(imgH*2/3) ))
    splitNum = set_parameter_string('1',args.splits)
    terminalY = round((terminaly -1)/int(splitNum))
    img.thumbnail((terminalx, terminalY), Image.ANTIALIAS)
    convertedImgW = img.size[0]
    convertedImgH = img.size[1]

    ascii_markNum = '38' if args.pattern else '48' 
    ascii_markString = 'm'+args.pattern[0] if args.pattern else 'm ' 

    if(img.mode == "RGB" or img.mode == "RGBA"):
        for y in range(0, convertedImgH):
            for x in range(0, convertedImgW):
                offset = y * convertedImgW + x
                xy = (x, y)
                rgb = img.getpixel(xy) 
                rgbR = rgb[0]
                rgbG = rgb[1]
                rgbB = rgb[2]
                outline = "\033[" + ascii_markNum +";2;" + str(rgbR) + ";" + str(rgbG) + ";" + str(rgbB) + ascii_markString 
                sys.stdout.write(outline)
            sys.stdout.write("\033[0m\n")
