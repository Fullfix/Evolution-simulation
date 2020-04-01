from World import World
from Individual import Individual
from Food import Food
from copy import copy
from genetic import generate_world, average_time, save, load, load_scores
import pickle
import matplotlib.pyplot as plt
import settings
import keras

if settings.SHOW:
    from Gui import draw_world
    import pygame

world = World(Individual, Food, settings.INITIAL_IND_NUM, settings.INITIAL_FOOD_NUM)
if settings.LOAD_NN:
    load(world)
else:
    with open('score.txt', 'wb') as f:
        pickle.dump(([], 0), f)
Scores = []
for e in range(settings.EPOCHS):
    initialPopulation = copy(world.Population)
    if settings.SHOW:
        if settings.FPS:
            clock = pygame.time.Clock()
    run = True
    n = 0
    while run:
        if settings.SHOW:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
        
            draw_world(world)
        world.run_move(Individual, Food)
        if world.Population == []:
            run = False
        n += 1
        if settings.SHOW:
            if settings.FPS:
                clock.tick(settings.FPS)
    av_time = average_time(initialPopulation)
    Scores.append(av_time)
    print(f'epoch {e}; total time {n}; average time {av_time}')
    del world
    world = generate_world(initialPopulation, Individual, Food)
    if e % 10 == 9:
        save(world, Scores)
        Scores = []

if not settings.SHOW:
    Scores, Epochs = load_scores(Scores)
    plt.plot(Epochs, Scores)
    plt.show()