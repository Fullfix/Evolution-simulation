import random
import settings
import numpy as np
from Food import Food
from algorithm import create_model


class Individual(object):
    def __init__(self, pos):
        self.energy = settings.INITIAL_ENERGY
        self.pos = pos
        self.model = create_model()
        self.totaltime = 0
    
    def _die(self, World):
        World.Population.remove(self)
        World.Foods.append(Food(self.pos))
    
    def _create_input(self, World):
        x, y = self.pos
        field = World.Field
        X = []
        Xrange = np.array(range(x-2, x+3)) % settings.FIELD_SIZE
        Yrange = np.array(range(y-2, y+3)) % settings.FIELD_SIZE
        for i in Yrange:
            for j in Xrange:
                X.append(field[i][j])
        X.pop(12)
        X = np.array(X).reshape(1, 24)
        return X

    def _choose_dir(self, World):
        X = self._create_input(World)
        Y = self.model.predict(X)[0]
        i = sorted(range(8), key=lambda x: Y[x], reverse=True)[0]
        return settings.ALL_ACTIONS[i]
    
    def _eat_food(self, food, World):
        if self.pos == food.pos:
            self.energy += settings.ENERGY_BONUS
            if self.energy >= settings.MAX_ENERGY:
                self.energy = settings.MAX_ENERGY
            World.Foods.remove(food)
    
    def _move_pos(self, y, x, newy, newx, World):
        fieldpos = World.check_position([newx, newy])
        self.pos = [newx, newy]
        if fieldpos == 0:
            pass
        elif fieldpos == 2:
            for f in World.Foods:
                if f.pos == self.pos:
                    food = f
                    break
            self._eat_food(food, World)
        else:
            self.pos = [x, y]
    
    def move(self, direction, World):
        x, y = self.pos
        if direction == 'L':
            self._move_pos(y, x, y, (x-1)%settings.FIELD_SIZE, World)
        elif direction == 'R':
            self._move_pos(y, x, y, (x+1)%settings.FIELD_SIZE, World)
        elif direction == 'U':
            self._move_pos(y, x, (y-1)%settings.FIELD_SIZE, x, World)
        elif direction == 'D':
            self._move_pos(y, x, (y+1)%settings.FIELD_SIZE, x, World)
        elif direction == 'LU':
            self._move_pos(y, x, (y-1)%settings.FIELD_SIZE, (x-1)%settings.FIELD_SIZE, World)
        elif direction == 'UR':
            self._move_pos(y, x, (y-1)%settings.FIELD_SIZE, (x+1)%settings.FIELD_SIZE, World)
        elif direction == 'RD':
            self._move_pos(y, x, (y+1)%settings.FIELD_SIZE, (x+1)%settings.FIELD_SIZE, World)
        elif direction == 'DL':
            self._move_pos(y, x, (y+1)%settings.FIELD_SIZE, (x-1)%settings.FIELD_SIZE, World)
        self.totaltime += 1


    def make_action(self, World):
        if self.energy <= 0 or self.totaltime >= settings.IND_LIVING_TIME:
            self._die(World)
        else:
            direction = self._choose_dir(World)
            self.energy -= 1
            self.move(direction, World)
    
    def __repr__(self):
        return f'Individual x:{self.pos[0]} y:{self.pos[1]} energy:{self.energy}'
