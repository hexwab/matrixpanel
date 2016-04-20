#! /usr/bin/env python3

import time
import math
import numpy as np
from matrixscreen import MatrixScreen

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

def col(r,g,b):
    r = int(r * 256.0 - 0.5)
    g = int(g * 256.0 - 0.5)
    b = int(b * 256.0 - 0.5)
    return r | (g << 8) | (b << 16)

offset = 0.0
DT = 1/30

def draw(screen):
    global offset
    sz = 64
    scale = 0.5 * math.pi * 2.0 / float(sz)
    cx1 = 0.5*math.sin(offset/5)
    cy1 = 0.5*math.sin(offset/3)
    for y in range(0, sz):
        for x in range(0, sz):
            p = x / float(sz) - 0.5
            q = y / float(sz) - 0.5
            v = math.sin(10*(p*math.sin(offset/2)+q*math.cos(offset/3))+offset)
            cx = cx1 + p
            cy = cy1 + q
            v += math.sin(10*math.sqrt(cx*cx+cy*cy+0.5)+offset)
            color = color_plasma(v)
            screen[x, y] = color
    offset += DT

def main():
    next_tick = time.time()
    frames = 0
    m = MatrixScreen()
    if True:
        start = time.time()
        while (time.time() - start) < 300000000:
            now = time.time()
            if now > next_tick:
                print(frames)
                frames = 0
                next_tick += 1.0
            frames += 1
            draw(m.screen)
            m.send()
    else:
        m.screen[:] = 0
        m.send()

if __name__ == "__main__":
    main()
