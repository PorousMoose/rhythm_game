import json
import pygame
import random

from time import sleep

SIZE = WIDTH, HEIGHT = (800, 400)
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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

    # getting the first font is done for system cross-compatibily reasons
    letter_size = 100
    beat_width = WIDTH / 4
    font = pygame.font.SysFont(pygame.font.get_fonts()[0], letter_size)

    rhythm_surface_width = (beat_width * sum(rhythm_pattern)) + 100
    rhythm_surface = pygame.Surface((rhythm_surface_width, 100))

    for size in accumulator(rhythm_pattern):
        letter = font.render(random.choice(alphabet), True, WHITE, BLACK)
        rhythm_surface.blit(letter, (beat_width * size, 0))

    return rhythm_surface


def main():
    pygame.init()
    pygame.mixer.pre_init(44100, -16, 2, 2048)
    config = load_validate_settings()

    pygame.mixer.music.load("game_music.wav")
    rhythm_surface = generate_rhythm_surface(
        config["rhythm_pattern"], config["alphabet"]
    )

    beat_length = 60 / config["bpm"]
    pixels_per_beat = WIDTH / 4

    # speed is pixels to move text so that 4 beats of text are on screen at any moment
    speed = pixels_per_beat / (beat_length * FPS)

    screen = pygame.display.set_mode(SIZE)
    for tick in range(config["runtime"] * FPS):
        # start music as letters hit edge of screen
        if tick == (beat_length * FPS * 4):
            pygame.mixer.music.play()

        sleep(1 / FPS)
        screen.fill(BLACK)
        screen.blit(rhythm_surface, (WIDTH - (tick * speed), 125))
        pygame.display.flip()


if __name__ == "__main__":
    main()
