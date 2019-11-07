import random
import json
import os

from pico2d import *

from project.game_code.state_code import game_framework
from project.game_code.state_code import pause_state
from project.game_code.object_code import game_world

from project.game_code.object_code.dragon import Dragon
from project.game_code.object_code.walker import Walker
from project.game_code.object_code.drunk import Drunk
from project.game_code.stage_code.background import Background

name = "main_state"

dragon = None
background = None
walkers = None
drunk = None


def enter():
    global dragon, background, walkers, drunk
    dragon = Dragon()
    background = Background()
    walkers = [Walker(230, 150, 1), Walker(740, 150, -1), Walker(500, 410, -1),
               Walker(510, 410, 1), Walker(320, 240, -1), Walker(650, 240, 1),
               Walker(230, 330, 1), Walker(740, 330, -1)]
    drunk = Drunk()

    game_world.add_object(background, 0)
    game_world.add_object(dragon, 1)
    game_world.add_objects(walkers, 2)
    game_world.add_object(drunk, 3)


def exit():
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_state(pause_state)
        else:
            dragon.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()
