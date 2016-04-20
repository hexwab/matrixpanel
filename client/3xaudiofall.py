#! /usr/bin/env python3
import random
from rec import SwhRecorder
from matrixscreen import MatrixScreen
import numpy as np
import time

class Game:
    def __init__(self):
        self.color1 = np.zeros((21, 64), dtype=np.uint32)
        self.color2 = np.zeros((21, 64), dtype=np.uint32)
        self.color3 = np.zeros((21, 64), dtype=np.uint32)
        self.offset = 0
        self.palette = [None] * 256
        self.palette2 = [None] * 256
        self.palette3 = [None] * 256

    def loop(self):
        ys=game.SR.fft(minHz=300, maxHz=2500)
        ys2=game.SR2.fft(minHz=300, maxHz=2500)
        ys3=game.SR3.fft(minHz=300, maxHz=2500)

        yscale = 4 # higher means more sensitive
        yoffs = 55 # noise floor. lower means display more low-level noise

        row = np.zeros(64, dtype=np.uint32)

        for i in range(64):
            y = int((ys[i]-yoffs)*yscale)
            y = max(0, min(y, 255))
            row[i] = y
        self.color1 = np.roll(self.color1, 1, axis=0)
        self.color1[0, :] = row[:]

        for i in range(64):
            y = int((ys2[i]-yoffs)*yscale)
            y = max(0, min(y, 255))
            row[i] = y
        self.color2 = np.roll(self.color2, 1, axis=0)
        self.color2[0, :] = row[:]

        for i in range(64):
            y = int((ys3[i]-yoffs)*yscale)
            y = max(0, min(y, 255))
            row[i] = y
        self.color3 = np.roll(self.color3, 1, axis=0)
        self.color3[0, :] = row[:]
        
        game.offset = (game.offset + 1) & 63
        for x in range(21):
            for y in range(64):
                ll = self.color1[x, y]
                game.matrix.screen[y, x] = game.palette[ll]
        for x in range(20):
            for y in range(64):
                ll = self.color2[x, y]
                game.matrix.screen[y, x+22] = game.palette2[ll]
        for x in range(21):
            for y in range(64):
                ll = self.color3[x, y]
                game.matrix.screen[y, x+43] = game.palette3[ll]

        game.matrix.send()
    
def inter(x,y,t):
    return x + (y-x) * t

def inter3(x,y,t):
    return (inter(x[0],y[0],t),
            inter(x[1],y[1],t),
            inter(x[2],y[2],t))

def color_int(t):
    return int(t[0]) + (int(t[1])<<16) + (int(t[2])<<8)

def main():
    global game

    game = Game()
    game.SR=SwhRecorder()
    game.SR.setup(3)
    game.SR.continuousStart()
    game.SR2=SwhRecorder()
    game.SR2.setup(4)
    game.SR2.continuousStart()
    game.SR3=SwhRecorder()
    game.SR3.setup(5)
    game.SR3.continuousStart()
    game.matrix = MatrixScreen()
    
    # PALETTES = [[(0,0,64),
    #            (0,255,0),
    #            (255,0,0),
    #            (255,0,0)]
    #             ,
    #             [(0,32,16),
    #              (0,255,255),
    #              (255,255,0),
    #              (255,255,255)]
    #             ,
    #             [(64,0,0),
    #              (0,0,0),
    #              (128,0,255),
    #              (255,255,255)]
    #             ]

    PALETTES = [[(0,0,0),
               (96,0,0),
               (96,255,0),
               (255,128,255)]
                ,
                [(0,32,0),
                 (0,128,32),
                 (255,64,0),
                 (0,255,255)]
                ,
                 [(0,0,0),
                  (0,0,128),
                  (128,0,255),
                  (255,255,128)]
                ]

    # PALETTES = [[(0,0,0),
    #            (255,0,0),
    #            (0,255,0),
    #            (0,0,255)]
    #             ,
    #             [(0,0,0),
    #              (0,255,0),
    #              (0,0,255),
    #              (255,0,0)]
    #             ,
    #              [(0,0,0),
    #               (0,0,255),
    #               (255,0,0),
    #               (0,255,0)]
    #             ]

    for i in range(85):
        for j in range(3):
            game.palette[i+j*0x55] = color_int(
                inter3(PALETTES[0][j], PALETTES[0][j+1],i/85.0))
            game.palette[255] = color_int(PALETTES[0][3])
            game.palette2[i+j*0x55] = color_int(
                inter3(PALETTES[1][j], PALETTES[1][j+1],i/85.0))
            game.palette2[255] = color_int(PALETTES[1][3])
            game.palette3[i+j*0x55] = color_int(
                inter3(PALETTES[2][j], PALETTES[2][j+1],i/85.0))
            game.palette3[255] = color_int(PALETTES[2][3])

    next_tick = time.time() + 1.0
    frames = 0;
    start = time.time()
    try:
        while time.time() - start < 300:
            #time.sleep(0.01)
            game.loop()
            frames += 1
            if time.time() > next_tick:
                print(frames)
                next_tick += 1.0
                frames = 0
    finally:
        game.matrix.screen[:] = 0
        game.matrix.send()
        game.SR.continuousEnd()

#this calls the 'main' function when this script is executed
if __name__ == '__main__': main()
