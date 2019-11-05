from pico2d import *
from project.game_code.state_code import game_framework
from project.game_code.state_code import main_state

name = "TitleState"
image = None


def enter():
    global image
    image = load_image('sprite\\title.png')


def exit():
    global image
    del (image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()

            elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_SPACE):
                game_framework.change_state(main_state)


def draw():
    clear_canvas()
    image.draw(480, 300, 960, 600)
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
