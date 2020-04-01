import pygame
import settings
from Food import Food
from Individual import Individual

def find_ind(world, pos):
    return next(x for x in world.Population if x.pos == pos)

def find_food(world, pos):
    return next(x for x in world.Foods if x.pos == pos)

pygame.init()
pygame.font.init()
win = pygame.display.set_mode((1000, 1000))

OBJECT_SIZE = 1000 // settings.FIELD_SIZE
FONT_SIZE = OBJECT_SIZE // 2
RED_COLOR = (255, 0, 0)
GREEN_COLOR = (0, 255, 0)
GREY_COLOR = (150, 150, 150)
BLACK_COLOR = (0, 0, 0)
MIN_SATURATION = 50

myfont = pygame.font.SysFont('Roboto', FONT_SIZE)

def draw_world(world):
    field = world.Field
    pygame.display.set_caption(f'totaltime: {world.totaltime}')
    win.fill(GREY_COLOR)
    for i in range(len(field)):
        for j in range(len(field[i])):
            rect = [OBJECT_SIZE * j, OBJECT_SIZE * i, OBJECT_SIZE, OBJECT_SIZE]
            if field[i][j] == 0:
                color = GREY_COLOR
            elif field[i][j] == 1:
                ind = find_ind(world, [j, i])
                text = myfont.render(str(ind.energy), 0, GREY_COLOR)
                color = list(GREEN_COLOR)
                color[1] = (color[1] - MIN_SATURATION) * (ind.energy / settings.MAX_ENERGY) + MIN_SATURATION
            elif field[i][j] == 2:
                food = find_food(world, [j, i])
                text = myfont.render(str(food.lifetime), 0, GREY_COLOR)
                color = RED_COLOR
            pygame.draw.rect(win, color, rect)
            if settings.SHOW_NUMBERS:
                if field[i][j] in [1, 2]:
                    w, h = text.get_rect().width, text.get_rect().height
                    x_pad = (OBJECT_SIZE - w) // 2
                    y_pad = (OBJECT_SIZE - h) // 2
                    win.blit(text, (rect[0] + x_pad, rect[1] + y_pad))

    pygame.display.update()