#!/usr/bin/env python3
import numpy as np
from matrixscreen import MatrixScreen
import time

def life_step(X):
    """Game of life step using generator expressions"""
    nbrs_count = sum(np.roll(np.roll(X, i, 0), j, 1)
                     for i in (-1, 0, 1) for j in (-1, 0, 1)
                     if (i != 0 or j != 0))
    return (nbrs_count == 3) | (X & (nbrs_count == 2))


np.random.seed(0)
X = np.zeros((64, 64), dtype=bool)
r = np.random.random((64, 64))
#X[16:48, 16:48] = (r > 0.75)
X[0:64, 0:64] = (r > 0.75)
matrix = MatrixScreen()
cols = [0,0x8000e0]#,0x0]

def draw(screen):
    global X
    X = life_step(X)
    for i in range(0,64):
        for j in range(0,64):
            screen[i,j] = cols[X[i,j]]

def main():
    next_tick = time.time()
    frames = 0
    m = MatrixScreen()
    try:
        start = time.time()
        while (time.time() - start) < 43:
            draw(m.screen)
            m.send()
            time.sleep(1./40)
    except:
        m.screen[:] = 0
        m.send()

if __name__ == "__main__":
    main()
