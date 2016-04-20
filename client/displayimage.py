#! /usr/bin/env python3

import time
import math
import numpy as np
from matrixscreen import MatrixScreen
import os, sys
from PIL import Image
from webcolors import rgb_to_hex

                        
def pos_modf(val):
    val = math.modf(val)[0]
    if val < 0:
        return val + 1.0
    return val

def color_plasma(val):
    val = pos_modf(val) * 3.0
    if val < 1.0:
        r = val
        g = 1.0 - r
        b = 0.0
    elif val < 2.0:
        b = val - 1.0
        r = 1.0 - b
        g = 0.0
    else:
        g = val - 2.0
        b = 1.0 - g
        r = 0.0
    r = int(r * 256.0 - 0.5)
    g = int(g * 256.0 - 0.5)
    b = int(b * 256.0 - 0.5)
    return r | (g << 8) | (b << 16)

def draw(screen, pix):
    sz = 64
    for x in range(0, sz):
        for y in range(0, sz):
            rgb = pix[x,y]
            r, g, b = rgb
            #screen[x,y] = 0xaeaeae
            val = (hex(r) + hex(g)[2:] + hex(b)[2:]).strip()
            screen[x, y] = r | (b << 8) | (g << 16)
            #print(val + "-")

def main():
    next_tick = time.time()
    frames = 0
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = "m64.BMP"
    if len(sys.argv) > 2:
        timeout = int(sys.argv[2])
    else:
        timeout = 10

    im = Image.open(filename)
    pix = im.load()
    m = MatrixScreen()
    try:
        start = time.time()
        while (time.time() - start) < timeout:
            now = time.time()
            if now > next_tick:
                print(frames)
                frames = 0
                next_tick += 1.0
            frames += 1
            draw(m.screen, pix)
            m.send()
            time.sleep(0.1)
    except:
        m.screen[:] = 0
        m.send()
        raise

if __name__ == "__main__":
    main()
