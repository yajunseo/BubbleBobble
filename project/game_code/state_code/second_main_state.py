import random
import json
import os
import time


from pico2d import *

from project.game_code.state_code import game_framework
from project.game_code.state_code import pause_state
from project.game_code.state_code import game_over_state
from project.game_code.state_code import store_state
from project.game_code.state_code import end_state
from project.game_code.state_code import first_main_state
from project.game_code.state_code import second_store_state
from project.game_code.management_code import game_world

from project.game_code.object_code.dragon import Dragon
from project.game_code.object_code.tadpole import Tadpole
from project.game_code.object_code.magician import Magician
from project.game_code.object_code.bubble import Bubble
from project.game_code.object_code.fire import Fire
from project.game_code.object_code.item_banana import Banana
from project.game_code.object_code.item_turnip import Turnip
from project.game_code.object_code.item_watermelon import Watermelon
from project.game_code.stage_code.pink_background import Background

name = "second_main_state"

dragon = None
background = None
tadpoles = None
magician = None
bubble = None
fire = None
is_magician_spawn = False
life = None
font = None
speed_item_count = None
bananas = None
turnips = None
watermelons = None
main_sound = None
boss_sound = None

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def bottom_collide(a, b, n):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    i = b.get_bb()
    for j in range(n):
        if left_a <= i[j][2] and right_a >= i[j][0]:
            if i[j][3] + 1 >= bottom_a >= i[j][3] - 1:
                return True
    return False


def enter():
    global dragon, background, tadpoles, magician, life, font, gold, fire, speed_item_count, is_magician_spawn, main_sound, boss_sound
    is_magician_spawn = False
    speed_item_count = store_state.get_speed_item()
    dragon = Dragon()
    dragon.life = store_state.get_life()
    background = Background()
    tadpoles = [Tadpole(45, 157, 1),Tadpole(915, 157, -1), Tadpole(915, 373, -1),
               Tadpole(45, 373, 1), Tadpole(500, 157, -1),Tadpole(280, 373, 1),
               Tadpole(500, 265, 1),Tadpole(700, 373, -1)]
    magician = Magician()
    life = load_image('sprite\\Character\\life.png')

    game_world.add_object(background, 0)
    game_world.add_objects(tadpoles, 1)
    game_world.add_object(dragon, 2)
    font = load_font('font.TTF', 28)

    main_sound = load_image('sprite\\state\\kpu_credit.png')
    main_sound = load_wav('sound\\mainstage.wav')
    main_sound.set_volume(50)
    main_sound.repeat_play()
    boss_sound = load_image('sprite\\state\\kpu_credit.png')
    boss_sound = load_wav('sound\\stage2_boss.wav')
    boss_sound.set_volume(50)


def exit():
    global boss_sound, main_sound, is_magician_spawn
    del boss_sound
    if not is_magician_spawn:
        del main_sound
    game_world.clear()


def pause():
    pass


def resume():
    pass


def handle_events():
    global bubble, speed_item_count, dragon
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            dragon.is_move = False
            game_framework.push_state(pause_state)
        else:
            dragon.handle_event(event)
            if event.type == SDL_KEYDOWN and event.key == SDLK_LCTRL:
                dragon.check_attack_delay_end_time = get_time() - dragon.check_attack_delay_start_time
                if dragon.check_attack_delay_end_time > (0.3 - speed_item_count*0.1):
                    dragon.sound_attack()
                    bubble = Bubble(dragon.x, dragon.y, dragon.dir)
                    game_world.add_object(bubble, 4)
                    dragon.check_attack_delay_end_time = 0
                    dragon.check_attack_delay_start_time = get_time()


def update():
    global is_magician_spawn, fire, bananas, turnips, watermelons, main_sound, boss_sound
    for game_object in game_world.all_objects():
        game_object.update()

    if dragon.is_fall:
        if bottom_collide(dragon, background, 12):
            dragon.stop()
        else:
            if not bottom_collide(dragon, background, 12):
                dragon.cancel_stop()

    for tadpole in tadpoles:
        if bottom_collide(tadpole, background, 12):
            tadpole.is_fall = False
        else:
            tadpole.is_fall = True
        if collide(dragon, tadpole):
            if not tadpole.is_beaten:
                if not dragon.is_beaten:
                    if dragon.life >= 0:
                        dragon.sound_beat()
                        dragon.life -= 1
                    dragon.is_beaten = True
                    dragon.invincible_start_time = get_time()
            else:
                if not tadpole.is_dead:
                    dragon.sound_kill_monster()
                    first_main_state.dragon.gold += 100
                    tadpole.is_dead = True
                    fruit_random_spawn_percent = random.randint(1, 200)
                    if fruit_random_spawn_percent <= 60:
                        bananas = Banana(tadpole.x, tadpole.y)
                        game_world.add_object(bananas, 6)
                        bananas.spawn_start_time = get_time()
                    elif fruit_random_spawn_percent <= 110:
                        turnips = Turnip(tadpole.x, tadpole.y)
                        game_world.add_object(turnips, 6)
                        turnips.spawn_start_time = get_time()
                    elif fruit_random_spawn_percent <= 140:
                        watermelons = Watermelon(tadpole.x, tadpole.y)
                        game_world.add_object(watermelons, 6)
                        watermelons.spawn_start_time = get_time()
                    tadpole.check_dead_motion_time = get_time()
                    tadpole.check_dead_motion_time = get_time()

    for tadpole in tadpoles:
        if tadpole.check_dead_motion_end_time > 1:
            game_world.remove_object(tadpole)

    if game_world.objects[6]:
        for i in game_world.objects[6]:
            if i.spawn_check_time > 1:
                i.is_spawn = True
        for i in game_world.objects[6]:
            if i.is_spawn:
                if collide(dragon, i):
                    dragon.sound_eat_fruit()
                    if i.number == 1:
                        first_main_state.dragon.gold += 50
                    elif i.number == 2:
                        first_main_state.dragon.gold += 100
                    else:
                        first_main_state.dragon.gold += 200
                    game_world.remove_object(i)

    if not game_world.objects[1]:
        if not is_magician_spawn:
            del main_sound
            boss_sound.repeat_play()
            game_world.add_object(magician, 3)
            is_magician_spawn = True

    if game_world.objects[4]:
        for tadpole in tadpoles:
            for i in game_world.objects[4]:
                if collide(i, tadpole):
                    if not tadpole.is_beaten:
                        game_world.remove_object(i)
                        tadpole.is_beaten = True

    # dragon -> bubble
    if game_world.objects[3]:
        if game_world.objects[4]:
            for i in game_world.objects[4]:
                if collide(i, magician):
                    game_world.remove_object(i)
                    if magician.hp >= 0:
                        magician.hp -= 1

                    else:
                        if not magician.is_lock:
                            magician.is_lock = True

        if magician.hp == 16:
            magician.second_phase_move_time_start = get_time()

        if not magician.is_lock:
            if magician.check_attack_end_time > (0.5 - (magician.phase * 0.1)):
                fire = Fire(magician.x, magician.y, magician.phase, magician.fire_number)
                game_world.add_object(fire, 5)
                magician.fire_number = (magician.fire_number + 1) % 16
                magician.check_attack_start_time = get_time()

        if collide(dragon, magician):
            if not magician.is_lock:
                if not dragon.is_beaten:
                    if dragon.life >= 0:
                        dragon.sound_beat()
                        dragon.life -= 1
                    dragon.is_beaten = True
                    dragon.invincible_start_time = get_time()
            else:
                if not magician.is_dead:
                    dragon.sound_kill_monster()
                    first_main_state.dragon.gold += 700
                    magician.check_dead_motion_start_time = get_time()
                    magician.is_dead = True

        if magician.check_dead_motion_end_time > 1:
            game_world.remove_object(magician)
            game_framework.change_state(second_store_state)

    if not magician.is_dead:
        if fire:
            for i in game_world.objects[5]:
                if collide(dragon, i):
                    if not dragon.is_beaten:
                        if dragon.life >= 0:
                            dragon.sound_beat()
                            dragon.life -= 1
                        dragon.is_beaten = True
                        dragon.invincible_start_time = get_time()
                        game_world.remove_object(i)
                else:
                    if i.x < 0 or i.x > 960 or i.y < 0 or i.y > 550:
                        game_world.remove_object(i)

    if dragon.life < 0:
        game_framework.change_state(game_over_state)

def draw():
    global font, gold
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    for i in range(dragon.life):
        life.draw(i*40+20, 580, 40, 40)
    font.draw(830, 580, '%d' % first_main_state.dragon.gold, (255, 255, 255))
    update_canvas()


def get_gold():
    return first_main_state.dragon.gold

def get_life():
    return first_main_state.dragon.life
