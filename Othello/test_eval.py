from time import sleep
from othello import Othello
import pygame
import numpy as np
import tensorflow.keras.models as models


model = models.load_model('./Othello/models/othello.h5')

pygame.init()
width = 320
height = 320
env = Othello(width, height, True)
state = env.reset()

isRunning = True
while isRunning:
    
    if env.is_black_turn:
        x = np.reshape(state, [1, 8, 8, 1])
        action = np.argmax(model.predict(x))
        action_pos = (action&0b111,action>>3)
        env.put_cell(action_pos)
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                isRunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    env.put_random_cell()

            if event.type == pygame.MOUSEBUTTONUP:
                env.put_click_pos(list(event.pos))

    state = env.state
    pygame.display.update()
    sleep(0.1)

pygame.quit()     