import numpy as np
from copy import copy
import random
import settings

class World(object):
    def __init__(self, IndividualClass, FoodClass, num_ind, num_food):
        self.Population = []
        self.Foods = []
        self.spawn_population(IndividualClass, num_ind)
        self.spawn_food(FoodClass, num_food)
        self.totaltime = 0

    def _spawn_random_food(self, FoodClass):
        spawned = False
        while not spawned:
            x = np.random.randint(0, settings.FIELD_SIZE)
            y = np.random.randint(0, settings.FIELD_SIZE)
            fieldpos = self.check_position([x, y])
            if fieldpos == 0:
                spawned = True
                food = FoodClass([x, y])
                self.Foods.append(food)
        return food
    
    def _spawn_random_ind(self, IndividualClass):
        spawned = False
        while not spawned:
            x = np.random.randint(0, settings.FIELD_SIZE)
            y = np.random.randint(0, settings.FIELD_SIZE)
            fieldpos = self.check_position([x, y])
            if  fieldpos == 0:
                spawned = True
                individual = IndividualClass([x, y])
                self.Population.append(individual)
        return individual
    
    def check_position(self, pos):
        for individual in self.Population:
            if individual.pos == pos:
                return 1
        for food in self.Foods:
            if food.pos == pos:
                return 2
        return 0

    @property
    def Field(self):
        field = [[0 for i in range(settings.FIELD_SIZE)] for j in range(settings.FIELD_SIZE)]
        for individual in self.Population:
            field[individual.pos[1]][individual.pos[0]] = 1
        for food in self.Foods:
            field[food.pos[1]][food.pos[0]] = 2
        return field


    def spawn_food(self, FoodClass, num):
        for i in range(num):
            self._spawn_random_food(FoodClass)
    
    def spawn_population(self, IndividualClass, num):
        for i in range(num):
            self._spawn_random_ind(IndividualClass)
    
    def run_move(self, IndividualClass, FoodClass):
        for individual in copy(self.Population):
            individual.make_action(self)
        for food in copy(self.Foods):
            food.iteration(self)
        for i in range(settings.FOOD_SPAWN_NUM):
            if random.random() <= settings.FOOD_SPAWN_PROBABILITY:
                self._spawn_random_food(FoodClass)
        self.totaltime += 1