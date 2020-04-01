import random
import settings
import numpy as np
import pickle
import keras
from World import World
from deap.tools import cxTwoPoint, cxUniform, cxBlend, mutGaussian
from copy import deepcopy, copy
import time

def evaluate_ind(individual):
    return individual.totaltime

def mutate(weights):
    for W in weights:
        M = np.random.normal(settings.MU, settings.SIGMA, W.shape)
        P = np.random.choice(2, W.shape, p=[1-settings.INDPB, settings.INDPB])
        W += M * P

def save_scores(Scores):
    with open('score.txt', 'rb') as f:
        S, E = pickle.load(f)
    if E != 0:
        S = S + Scores
        E = len(S)
    else:
        E = len(Scores)
        S = Scores
    with open('score.txt', 'wb') as f:
        pickle.dump((S, E), f)

def save(world, Scores):
    A = list(map(lambda x: x.model.get_weights(), world.Population))
    with open('weights.txt', 'wb') as f:
        pickle.dump(A, f)
    save_scores(Scores)
    print('saved')

def load(world):
    with open('weights.txt', 'rb') as f:
        weights = pickle.load(f)
    for W, I in zip(weights, world.Population):
        I.model.set_weights(W)
    print('loaded')

def load_scores(Scores):
    with open('score.txt', 'rb') as f:
        S, E = pickle.load(f)
    return S, range(E)


def choose_best(population, n):
    l = settings.INITIAL_IND_NUM
    sorted_pop = sorted(population, key=lambda x: x.totaltime, reverse=True)
    sorted_pop = [x.model.get_weights() for x in sorted_pop]
    return sorted_pop[:n], sorted_pop[n:l-n], sorted_pop[l-n:]

def average_time(population):
    return sum(list(map(lambda x: x.totaltime, population))) / len(population)

def generate_world(population, IndividualClass, FoodClass):
    # choose best individual models
    bestpopulaton, middle, worst = choose_best(population, settings.BEST_IND_NUM)
    # sex between middle
    for i in range(len(middle), 2):
        middle[i], middle[i+1] = cxBlend(middle[i], middle[i+1], settings.ALPHA)
    newpopulation = bestpopulaton + middle + deepcopy(bestpopulaton)
    # mutate
    for weights in newpopulation:
        mutate(weights)
    # set weights
    keras.backend.clear_session()
    world = World(IndividualClass, FoodClass, settings.INITIAL_IND_NUM, settings.INITIAL_FOOD_NUM)
    for ind, weights in zip(world.Population, newpopulation):
        ind.model.set_weights(weights)
    return world