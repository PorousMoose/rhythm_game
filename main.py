import json
import pygame
import random
import re

from time import sleep

SIZE = WIDTH, HEIGHT = (800, 600)
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

PYGAME_KEY_MAP = {
    "a": pygame.K_a,
    "b": pygame.K_b,
    "c": pygame.K_c,
    "d": pygame.K_d,
    "e": pygame.K_e,
    "f": pygame.K_f,
    "g": pygame.K_g,
    "h": pygame.K_h,
    "i": pygame.K_i,
    "j": pygame.K_j,
    "k": pygame.K_k,
    "l": pygame.K_l,
    "m": pygame.K_m,
    "n": pygame.K_n,
    "o": pygame.K_o,
    "p": pygame.K_p,
    "q": pygame.K_q,
    "r": pygame.K_r,
    "s": pygame.K_s,
    "t": pygame.K_t,
    "u": pygame.K_u,
    "v": pygame.K_v,
    "w": pygame.K_w,
    "x": pygame.K_x,
    "y": pygame.K_y,
    "z": pygame.K_z,
}


def load_validate_settings():
    with open("config.json") as f:
        raw_settings = f.read()

    config = json.loads(raw_settings)
    for v in ("bpm", "alphabet", "rhythm_pattern"):
        if v not in config:
            raise Exception(f"{v} missing from config")

    if type(config["bpm"]) not in (float, int):
        raise Exception("bpm must be a number")

    if type(config["runtime"]) is not int:
        raise Exception("runtime must be a whole number")

    if type(config["alphabet"]) is not str:
        raise Exception("alphabet must be a string")

    if not re.match(r"[a-zA-Z]+", config["alphabet"]):
        raise Exception("alphabet must only be letters")

    if type(config["rhythm_pattern"]) is not list or any(
        type(v) not in (int, float) for v in config["rhythm_pattern"]
    ):
        raise Exception("rhythm_pattern must be list of numbers")

    return config


def generate_rhythm_surface(rhythm_pattern, alphabet):
    def accumulator(l):
        total = 0
        yield total
        for x in l:
            total += x
            yield total

    letter_size = 100
    beat_width = WIDTH / 4
    # getting the first font is done for system cross-compatibily reasons
    font = pygame.font.SysFont(pygame.font.get_fonts()[0], letter_size)

    rhythm_surface_width = (beat_width * sum(rhythm_pattern)) + 100
    rhythm_surface = pygame.Surface((rhythm_surface_width, 100))
    letters = []
    spacers = []

    for size in accumulator(rhythm_pattern):
        letter = random.choice(alphabet)
        letters.append(letter.lower())
        letter_surface = font.render(letter.upper(), True, BLACK, WHITE)
        spacer = beat_width * size
        spacers.append(spacer + WIDTH)
        rhythm_surface.blit(letter_surface, (spacer, 0))

    return (rhythm_surface, letters, spacers)


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    config = load_validate_settings()

    screen = pygame.display.set_mode(SIZE)
    indicator_rectangle = pygame.Surface((60, 200))
    indicator_rectangle.fill(WHITE)
    score_font = pygame.font.SysFont(pygame.font.get_fonts()[0], 50)

    pygame.mixer.music.load("game_music.wav")

    rhythm_surface, letters, spacers = generate_rhythm_surface(
        config["rhythm_pattern"], config["alphabet"]
    )
    collision_window_width = 20

    beat_length = 60 / config["bpm"]
    pixels_per_beat = WIDTH / 4

    # speed is pixels to move text so that 4 beats of text are on screen at any moment
    speed = pixels_per_beat / (beat_length * FPS)

    listen_for_keys = False
    letter_found = False
    hits = 0
    total_letters  =len(letters)

    for tick in range(config["runtime"] * FPS):
        # start music as letters hit edge of screen
        if tick == (beat_length * FPS * 4):
            pygame.mixer.music.play()

        sleep(1 / FPS)
        screen.fill(BLACK)
        screen.blit(indicator_rectangle, (0, 0))
        screen.blit(indicator_rectangle, (0, 400))
        screen.blit(rhythm_surface, (WIDTH - (tick * speed), 225))
        scoreboard = score_font.render(f'You hit {hits}/{total_letters}', True, WHITE, BLACK)
        escape_notice = score_font.render('Press escape to quit', True, WHITE, BLACK)
        screen.blit(scoreboard, (150, 60))
        screen.blit(escape_notice, (150, 120))


        spacers = [spacer - speed for spacer in spacers]

        events = pygame.event.get()
        # determine if we're in a 'collision window' where pushing the right key is a hit
        if spacers:
            if spacers[0] < collision_window_width / 2 and not listen_for_keys:
                listen_for_keys = True
                letter_found = False

            # determine if we have left the collision window
            if spacers[0] < 0 - (collision_window_width / 2) and listen_for_keys:
                letters.pop(0)
                spacers.pop(0)
                listen_for_keys = False
        else:
            listen_for_keys = False

        keyboard = pygame.key.get_pressed()
        if keyboard[pygame.K_ESCAPE]:
            return
        if listen_for_keys and not letter_found:
            for k, v in PYGAME_KEY_MAP.items():
                if keyboard[v]:
                    letter_found = True
                    if k == letters[0]:
                        hits += 1

        pygame.event.clear()

        pygame.display.flip()


if __name__ == "__main__":
    main()
