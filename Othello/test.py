from time import sleep
from othello2 import Othello
import pygame
import numpy as np

pygame.init()
width = 320
height = 320
env = Othello(width, height, True)
env.reset()

for _ in range(10000):
    env.put_random_cell()

isRunning = True
while isRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                env.put_random_cell()

        if event.type == pygame.MOUSEBUTTONUP:
            env.put_click_pos(list(event.pos))

    pygame.display.update()
    sleep(0.01)

pygame.quit()