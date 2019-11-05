from pico2d import *
from math import sin, cos
from project.game_code.object_code import game_world


class Bottle:
    image = None

    def __init__(self, x, y, phase, number):
        if Bottle.image is None:
            Bottle.image = load_image('sprite\\Effect\\bottle.png')
        self.x, self.y, self.phase, self.dir = x, y, phase, number * 45
        self.frame = 0
        self.frame_speed_control = 0
        self.velocity = 0.5 * phase

    def draw(self):
        self.image.clip_draw(self.frame * 0, 0, 0, 0, self.x, self.y, 40, 40)

    def update(self):
        self.frame_speed_control += 1
        if self.frame_speed_control > (60-self.phase*10):
            self.frame = (self.frame + 1) % 4
            self.frame_speed_control = 0

        self.x += 1
        self.y += self.y * cos(self.dir)

        if self.x < 0 or self.x > 960 or self.y < 0 or self.y > 550:
            game_world.remove_object(self)
