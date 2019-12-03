from pico2d import *
from project.game_code.state_code import game_framework
from project.game_code.state_code import first_main_state
from project.game_code.state_code import title_state


name = "TitleState"
image = None
count = None
font = None

def enter():
    global image, count, font
    count = 0
    image = load_image('sprite\\state\\title1.png')
    font = load_font('font.TTF', 26)


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
                game_framework.change_state(first_main_state)


def draw():
    global count
    clear_canvas()
    count += 1
    image.draw(480, 300, 960, 600)
    if count <= 60:
        font.draw(180, 190, 'press SPACEBAR to start', (255, 0, 0))
    else:
        font.draw(180, 190, 'press SPACEBAR to start', (255, 187, 100))
        if count >= 120:
            count = 0
    update_canvas()


def update():
    pass


def pause():
    pass


def resume():
    pass
