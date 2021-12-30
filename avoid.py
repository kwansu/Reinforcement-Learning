from avoid_objects import *
from time import sleep
import numpy as np
import pygame
import random


class Avoid:
    def __init__(self, width, height, render=True, **kwargs):
        self.enable_render = render
        self.is_playing = True
        self.on_step = True
        self.world_time = 0.0
        self.step_time = 0.0
        self.step_interval = 0.1
        self.poop_interval = 1.0
        self.width = 30
        self.height = 40
        self.player_height = 30
        self.width_rate = width/30
        self.height_rate = height/40
        self.state = np.zeros([30, 30, 1],dtype=int)

        self.player_sprite = pygame.image.load('./data/player.png')
        self.poop_sprite = pygame.image.load('./data/poop.png')
        self.star_sprite = pygame.image.load('./data/star.png')
        self.background = pygame.image.load('./data/backGround_avoid.png')

        self.player = Player(sprite=self.player_sprite)
        self.player.pos = np.array([self.width/2, self.player_height - 3])
        self.objects = []
        self.pooling_poops = []
        self.pooling_star = []

        for _ in range(6):
            poop = Poop_Star(self.poop_sprite)
            poop.is_active = False
            self.objects.append(poop)

        pygame.init()
        if render:
            self.window = pygame.display.set_mode((width, height))
        #self.clock = pygame.time.Clock()
        #self.is_running = True
        #self.is_stoped = False


    def reset(self):
        self.world_time = 0
        self.step_time = 0

        for obj in self.objects:
            obj.is_active = False

        halfWidth = int(self.width/2)
        self.player.pos = np.array([halfWidth, int(self.player_height - self.player.half_size[1]-1)])
        self.state.fill(0)

        #state[int(self.player.pos[0])*31 + int(self.player.pos[1])] = 1
        #self.player.updateState(state, self.width, self.player_height)
        x = self.player.pos[0]-1
        y = self.player.pos[1]
        for h in range(y-2, y+3):
            self.state[h, x:x+3] = 1

        new_object = self.create_object()
        new_object.pos = [halfWidth, -1]


    def check_collision(self, player, object):
        d = abs(player.pos - object.pos) - (player.half_size + object.half_size)
        return d[0] < 0 and d[1] < 0


    def create_object(self):
        new_object = None
        if len(self.pooling_poops) > 0:
            new_object = self.pooling_poops.pop()
        else:
            new_object = Poop_Star(self.poop_sprite)
            self.objects.append(new_object)

        new_object.is_active = True
        return new_object


    def render(self):
        self.window.blit(self.background, [0, 0])

        for obj in self.objects:
            if obj.is_active == False:
                continue

            self.window.blit(self.poop_sprite, 10*(obj.pos - obj.half_size))

        self.window.blit(self.player_sprite, 10*(self.player.pos - self.player.half_size))
        pygame.display.update()


    def step(self, action, state):
        reward = 1
        is_termimal = False
        state.fill(0)

        self.player.pos = self.player.pos
        if action == 0:
            # if self.player.pos[0] > 0:
            self.player.pos[0] -= 1
        elif action == 2:
            # if self.player.pos[0] < self.width:
            self.player.pos[0] += 1

        if self.player.pos[0] <= 1 or self.player.pos[0] >= 28:
            is_termimal = True
            reward = -1

        #self.player.updateState(state, self.width, self.player_height)
        x = self.player.pos[0]-1
        y = self.player.pos[1]
        for h in range(y-2, y+3):
            state[h, x:x+3] = 1

        self.world_time += self.step_interval
        if self.world_time > self.poop_interval:
            self.world_time = 0
            new_object = self.create_object()
            new_object.pos = [random.randrange(1, 28), -1]

        for obj in self.objects:
            if obj.is_active == False:
                continue

            obj.pos[1] += 1
            if obj.pos[1] >= self.player_height:
                if obj.pos[1] >= self.height:
                    obj.is_active = False
                    self.pooling_poops.append(obj)
                continue
            else:
                state[int(obj.pos[1]), int(obj.pos[0])] = 1

            if self.check_collision(self.player, obj):
                if obj.is_star == True:
                    reward += 1
                    pass
                else:
                    self.is_playing = False
                    is_termimal = True
                    reward = 1

            if self.enable_render:
                self.render()

        return reward, is_termimal
