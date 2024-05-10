import pygame

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Variables
running = True
playing = False
main_menu = True
options = False
dt = 0
is_in_a_start_position = False
is_paused = False
dialogue = False

# Player var
health = 100
hunger = 100
food = 10

# initial screen manipulations

icon = pygame.transform.smoothscale(pygame.image.load('snow.png'), (200, 200))
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Nuclear Wind 1.0a")
pygame.display.set_icon(icon)
