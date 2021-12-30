import numpy as np


class Object:
    def __init__(self, sprite, pos=[0, 0], is_active=True) -> None:
        self.pos = np.array(pos)
        self.half_size = np.array(sprite.get_size()) * 0.05
        self.is_active = is_active
    
    def update_state(self, state, width, height):
        start = self.pos - self.half_size
        end = self.pos + self.half_size
        
        for i in range(int(start[1]+1), int(end[1])):
            hi = i*width
            state[hi + int(start[0]) + 1: hi+int(end[0])] = 1


class Poop_Star(Object):
    def __init__(self, sprite) -> None:
        super().__init__(sprite=sprite)
        self.is_star = False

    def update(self, world, delta_time):
        self.pos[1] += 10 * delta_time
        if self.pos[1] > world.height:
            self.is_active = False
            world.pooling_poops.append(self)
        
        return self.pos


class Player(Object):
    def __init__(self, sprite) -> None:
        super().__init__(sprite=sprite)
        self.score = 0.0
