import random
import settings


class Food(object):
    def __init__(self, pos):
        self.pos = pos
        self.lifetime = settings.FOOD_LIVING_TIME
    
    def _die(self, World):
        World.Foods.remove(self)
    
    def iteration(self, World):
        self.lifetime -= 1
        if self.lifetime <= 0:
            self._die(World)  
    
    def __repr__(self):
        return f'Food x:{self.pos[0]} y:{self.pos[1]}'