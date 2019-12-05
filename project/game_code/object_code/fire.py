from pico2d import *
import time
from math import sin, cos
from project.game_code.management_code import game_world
from project.game_code.state_code import game_framework


TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

pi = 3.14159256


class Fire:
    image = None

    def __init__(self, x, y, phase, number):
        if Fire.image is None:
            Fire.image = load_image('sprite\\Effect\\fireEffect.png')
        self.x, self.y, self.phase, self.dir = x, y, phase, number * 22.5
        self.frame = 0
        self.velocity = 0.5 * phase

    def draw(self):
 #       draw_rectangle(*self.get_bb())
        if int(self.frame) == 0:
            self.image.clip_draw(0, 0, 8, 14, self.x, self.y, 40, 40)
        elif int(self.frame) == 1:
            self.image.clip_draw(8, 0, 8, 14, self.x, self.y, 40, 40)
        else:
            self.image.clip_draw(16, 0, 8, 14, self.x, self.y, 40, 40)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

        self.x += math.sin(self.dir * pi / 180)
        self.y += math.cos(self.dir * pi / 180)


    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

