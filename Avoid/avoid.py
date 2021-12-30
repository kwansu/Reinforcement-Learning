import time
import pygame
import random
import numpy as np
from base import BaseEnv
from avoid_objects import *


class Avoid(BaseEnv):
    def __init__(self, screen_width=300, screen_height=400, render=True, **kwargs):
        self.enable_render = render
        self.state_size = [1, 30, 30]
        self.action_size = 4
        self.action_type = "discrete"
        self.score = 0

        self.is_playing = True
        self.on_step = True
        self.step_count = 0
        self.falling_interval = 10
        self.width = 30
        self.height = 40
        self.play_height = 30
        self.width_rate = screen_width / self.width
        self.height_rate = screen_height / self.height
        
        player_sprite = pygame.image.load("./pygame/player.png")
        poop_sprite = pygame.image.load("./pygame/poop.png")
        # star_sprite = pygame.image.load("./pygame/star.png")
        background = pygame.image.load("./pygame/background_avoid.png")

        self.player = Player(sprite=player_sprite)
        self.falling_objs = []
        self.obj_pool = []

        for _ in range(6):
            falling_obj = FallingObject(poop_sprite)
            falling_obj.is_active = False
            self.falling_objs.append(falling_obj)

        if self.enable_render:
            pygame.init()
            self.window = pygame.display.set_mode((screen_width, screen_height))

            self.player_sprite = player_sprite
            self.poop_sprite = poop_sprite
            # self.star_sprite = star_sprite
            self.background = background
            self.previous_time = 0.0
            self.framerate = 0.05

    def reset(self):
        state = np.zeros([1, 1, 30, 30], dtype=np.uint8)
        self.score = 0
        self.step_count = 0

        for obj in self.falling_objs:
            obj.is_active = False

        half_width = int(self.width / 2)
        self.player.pos = np.array(
            [half_width, int(self.play_height - self.player.half_size[1] - 1)]
        )

        x = self.player.pos[0] - 1
        y = self.player.pos[1]
        for h in range(y - 2, y + 3):
            state[:, :, h, x : x + 3] = 1

        new_object = self.create_object()
        new_object.pos = [half_width, -1]
        return state

    def check_collision(self, player, object):
        d = abs(player.pos - object.pos) - (player.half_size + object.half_size)
        return d[0] < 0 and d[1] < 0

    def create_object(self):
        new_object = None
        if len(self.obj_pool) > 0:
            new_object = self.obj_pool.pop()
        else:
            new_object = FallingObject(self.poop_sprite)
            self.falling_objs.append(new_object)

        new_object.is_active = True
        return new_object

    def render(self):
        self.window.blit(self.background, [0, 0])

        for obj in self.falling_objs:
            if obj.is_active == False:
                continue
            self.window.blit(self.poop_sprite, 10 * (obj.pos - obj.half_size))

        self.window.blit(
            self.player_sprite, 10 * (self.player.pos - self.player.half_size)
        )
        pygame.display.update()

    def step(self, action):
        state = np.zeros([1, 1, 30, 30], dtype=np.uint8)
        is_termimal = False
        reward = 1

        self.player.pos = self.player.pos
        if action == 0:
            self.player.pos[0] -= 1
        elif action == 2:
            self.player.pos[0] += 1

        if self.player.pos[0] <= 1 or self.player.pos[0] >= 28:
            is_termimal = True
            reward = -1

        x = self.player.pos[0] - 1
        y = self.player.pos[1]
        for h in range(y - 2, y + 3):
            state[:, :, h, x : x + 3] = 1

        self.step_count += 1
        if self.step_count > self.falling_interval:
            self.step_count = 0
            new_object = self.create_object()
            new_object.pos = [random.randrange(1, 28), -1]

        for obj in self.falling_objs:
            if obj.is_active == False:
                continue

            obj.pos[1] += 1
            if obj.pos[1] >= self.play_height:
                if obj.pos[1] >= self.height:
                    obj.is_active = False
                    self.obj_pool.append(obj)
                continue
            else:
                state[:, :, int(obj.pos[1]), int(obj.pos[0])] = 1

            if self.check_collision(self.player, obj):
                self.is_playing = False
                is_termimal = True
                reward = 1

        if self.enable_render:
            for event in pygame.event.get():
                pass
            if pygame.display.get_active():
                cur_time = time.time()
                if cur_time - self.previous_time >= self.framerate:
                    self.previous_time = cur_time
                    self.render()

        if self.step_count >= 2000:
            is_termimal = True

        self.score += reward
        reward = np.expand_dims([reward], 0)
        is_termimal = np.expand_dims([is_termimal], 0)
        return (state, reward, is_termimal)

    def close(self):
        if self.enable_render:
            pygame.quit()
