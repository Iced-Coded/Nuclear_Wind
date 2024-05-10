import pygame

pygame.mixer.init()


# Image library
class ImageLibrary:
    bg = pygame.transform.smoothscale(pygame.image.load("data/sprites/bg.jpg"), (1280, 720))
    plains_tile = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/plains.png'), (100, 100))
    forest_time = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/forest.png'), (100, 100))
    road_right = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/road_right.png'), (100, 100))
    road_down = pygame.transform.rotate(road_right, 90)
    road_up = pygame.transform.flip(road_down, False, True)
    lake = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/lake.png'), (100, 100))
    road_left_up = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/road_turn.png'), (100, 100))
    road_down_right = pygame.transform.flip(road_left_up, True, True)


# Sound library
class SoundsLibrary:
    # Sounds, Music and etc
    hover_sound = pygame.mixer.Sound('data/sounds/hover.wav')
    confirm_sound = pygame.mixer.Sound('data/sounds/Confirm.wav')
    main_menu_sound = pygame.mixer.Sound('data/sounds/mainmenu.mp3')
    hover_sound_1 = pygame.mixer.Sound('data/sounds/main_menu/Retro1.mp3')
    hover_sound_2 = pygame.mixer.Sound('data/sounds/main_menu/Retro2.mp3')
    walk_sound = pygame.mixer.Sound('data/sounds/movement/Steps.wav')
    debug_active_sound = pygame.mixer.Sound('data/sounds/synth.wav')
    power_up_sound = pygame.mixer.Sound('data/sounds/Powerup.wav')
    hurt_sound = pygame.mixer.Sound('data/sounds/Hurt.wav')
    ambient_sound = pygame.mixer.Sound('data/sounds/MoozE-S.A.D.mp3')

    # Sound Channels
    pygame.mixer.set_num_channels(3)
    main_channel = pygame.mixer.Channel(0)
    music_channel = pygame.mixer.Channel(1)
    ambient_channel = pygame.mixer.Channel(2)
