import json
import math
import random
import sys
from datetime import datetime

import pygame
import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel, UIPanel

debug = False
if sys.gettrace() is None:
    pass
else:
    debug = True

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Initializing pygame
pygame.init()

if debug:
    with open("log.txt", "a") as f:
        f.write(f"[{current_time}] Initialized pygame!\n")

# Initial screen manipulations
screen_width = 1280
screen_height = 720
icon = pygame.transform.smoothscale(pygame.image.load('snow.png'), (200, 200))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nuclear Wind 1.0a")
pygame.display.set_icon(icon)

if debug:
    with open("log.txt", "w") as f:
        f.write(f"[{current_time}] Initialized game window\n[{current_time}] Starting to initialize sounds library.\n")


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


if debug:
    with open("log.txt", "a") as f:
        f.write(
            f"[{current_time}] Sounds library successfully initialized.\n[{current_time}] Initializing image library.\n")


# Image library
class Image_Library:
    bg = pygame.transform.smoothscale(pygame.image.load("data/sprites/bg.jpg"), (1280, 720))
    plains_tile = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/plains.png'), (100, 100))
    forest_time = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/forest.png'), (100, 100))
    road_right = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/road_right.png'), (100, 100))
    road_down = pygame.transform.rotate(road_right, 90)
    road_up = pygame.transform.flip(road_down, False, True)
    lake = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/lake.png'), (100, 100))
    road_left_up = pygame.transform.smoothscale(pygame.image.load('data/sprites/tiles/road_turn.png'), (100, 100))
    road_down_right = pygame.transform.flip(road_left_up, True, True)


if debug:
    with open("log.txt", "a") as f:
        f.write(
            f"[{current_time}] Image library successfully initialized.\n[{current_time}] Initializing GUI Managers\n")


# GUI managers
class GUIs:
    main_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
    menu_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
    options_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
    text_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
    dialogue_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')


if debug:
    with open("log.txt", "a") as f:
        f.write(f"[{current_time}] GUI Managers successfully initialized.\n[{current_time}] Initializing Variables\n")

# Variables
clock = pygame.time.Clock()
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

# Buttons and other shit
font_large = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
button_width = 200
button_height = 50
button_list = []

# Map
map_data = [["forest", "plains", "plains", "road_up", "forest", "forest"],
            ["plains", "city", "road_right", "road_right_up", "plains", "forest"],
            ["city", "city_center", "forest", "plains", "lake", "plains"],
            ["forest", "road_down", "plains", "forest", "forest", "forest"],
            ["forest", "road_down", "forest", "plains", "forest", "plains"],
            ["road_right", "road", "plains", "hill", "forest", "forest"]]

movement_button_width = 100
movement_button_height = 100
start_x = 35
start_y = 35
margin = 2


# Movement system addition

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# GAME MOVEMENT SYSTEM START

if debug:
    with open("log.txt", "a") as f:
        f.write(
            f"[{current_time}] Variables successfully initialized.\n[{current_time}] Initializing Movement System.\n")

buttons = []
rects = []
for row_idx, row in enumerate(map_data):
    for col_idx, cell in enumerate(row):
        button = UIButton(
            relative_rect=pygame.Rect(start_x + col_idx * (movement_button_width + margin),
                                      start_y + row_idx * (movement_button_height + margin),
                                      movement_button_width,
                                      movement_button_height),
            text=cell,
            manager=GUIs.main_manager,
            object_id=ObjectID(class_id='@movement')
        )
        buttons.append(button)
        rect = pygame.Rect(start_x + col_idx * (movement_button_width + margin),
                           start_y + row_idx * (movement_button_height + margin),
                           movement_button_width,
                           movement_button_height)
        rects.append(rect)

# GAME MOVEMENT SYSTEM END

# START OF MAIN MENU BUTTONS

if debug:
    with open("log.txt", "a") as f:
        f.write(
            f"[{current_time}] Movement System successfully initialized.\n[{current_time}] Initializing Main Menu buttons.\n")

game_name = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 100, button_width, button_height),
    text='Nuclear Winter',
    manager=GUIs.menu_manager,
    object_id=ObjectID(class_id='@main_label')
)

start_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 250, button_width, button_height),
    text='Start Game',
    manager=GUIs.menu_manager
)

options_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 350, button_width, button_height),
    text='Options',
    manager=GUIs.menu_manager
)

quit_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 450, button_width, button_height),
    text='Quit',
    manager=GUIs.menu_manager
)

version_label = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 0.1, 500, button_width, button_height),
    text='1.0a',
    manager=GUIs.menu_manager
)

debug_label = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 0.1, 550, button_width, button_height),
    text='',
    manager=GUIs.menu_manager
)

# END OF MAIN MENU BUTTONS

# START OF OPTION MENU BUTTONS

if debug:
    with open("log.txt", "a") as f:
        f.write(
            f"[{current_time}] Main Menu buttons successfully initialized.\n[{current_time}] Initializing Options Menu buttons.\n")

options_label = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 100, button_width, button_height),
    text='Options',
    manager=GUIs.options_manager,
    object_id=ObjectID(class_id='@main_label')
)

options_exit_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 500, button_width, button_height),
    text='Exit Options',
    manager=GUIs.options_manager
)

# END OF OPTION MENU BUTTONS

# START OF MAIN GAME PANEL

if debug:
    with open("log.txt", "a") as f:
        f.write(
            f"[{current_time}] Options Menu buttons successfully initialized.\n[{current_time}] Initializing Main Game panel.\n")

main_panel = UIPanel(pygame.Rect(675, -3, 610, 730),
                     manager=GUIs.main_manager)
UILabel(pygame.Rect(245, 10, 150, 30),
        text='Nuclear Wind 1.0a',
        manager=GUIs.main_manager,
        container=main_panel)
UILabel(pygame.Rect(10, 45, 150, 30),
        text=f'Health: {health}',
        manager=GUIs.main_manager,
        container=main_panel)
hunger_label = UILabel(pygame.Rect(17, 75, 150, 30),
                       text=f'Hunger: {hunger}',
                       manager=GUIs.main_manager,
                       container=main_panel)
canned_food = UILabel(pygame.Rect(32, 106, 150, 30),
                      text=f'Canned Food: {food}',
                      manager=GUIs.main_manager,
                      container=main_panel)
eat_food = UIButton(pygame.Rect(45, 140, 150, 30),
                    text='Eat Canned Food',
                    manager=GUIs.main_manager,
                    container=main_panel)
dialogue_button = UIButton(relative_rect=pygame.Rect(45, 170, 150, 30),
                           text="Talk to NPCs",
                           manager=GUIs.main_manager,
                           container=main_panel)

# END OF MAIN GAME PANEL

# Pause menu

# pause_panel_bg = UIPanel(pygame.Rect(0, 0, 360, 480),
#                      manager=main_manager,
#                      anchors={'center':'center'})

# Pause Menu end

# Position of a player
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# If debug mode is active then skip main menu
if debug:
    main_menu = False
    playing = True
    options = False
    SoundsLibrary.debug_active_sound.play()

if debug:
    with open("log.txt", "a") as f:
        f.write(f"[{current_time}] Main Game panel successfully initialized.\n[{current_time}] Initializing Player.\n")


# Initialize player class and player's sprites (unused, but, deleting it might break the entire code)
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image_down = pygame.transform.scale(pygame.image.load('data/sprites/player/alex.png'),
                                                 (width, height))
        self.image_up = pygame.transform.scale(pygame.image.load('data/sprites/player/up_idle.png'), (width, height))
        self.image_left = pygame.transform.scale(pygame.image.load('data/sprites/player/side_idle.png'),
                                                 (width, height))
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.x = player_pos.x
        self.rect.y = player_pos.y
        self.health = health
        self.hunger = hunger
        self.food = food


# Initialize player in rendering
player = pygame.sprite.Group()
player.add(Player(60, 75))

options_button.disable()

# Main game code.
while running:

    def save(sprite):
        dic = {
            "Player_Pos": sprite.rect.center,
            "Health": health,
            "Hunger": hunger,
            "Canned_Food": food
        }

        json_object = json.dumps(dic, indent=4)

        # Writing to sample.json
        with open("save.json", "w") as outfile:
            outfile.write(json_object)


    def load(sprite):
        try:
            with open('save.json') as save_file:
                data = json.load(save_file)  # Load data and close file automatically
                sprite.health = data.get("Health", sprite.health)  # Set default if missing
                sprite.hunger = data.get("Hunger", sprite.hunger)
                sprite.rect.center = data.get("Player_Pos", sprite.rect.center)  # Handle as tuple
                sprite.food = data.get("Canned_Food", sprite.food)

        except FileNotFoundError:
            print("Save file not found. Continuing with default values.")

        print(f"Hunger: {sprite.hunger}")
        print(f"Health: {sprite.health}")
        print(f"Player Position: {sprite.rect.center}")
        print(f"Canned Food: {sprite.food}")


    debug_0 = False
    debug_1 = False
    debug_2 = False
    debug_3 = False
    # General event handler, like, quitting game and using debug things.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if playing and not main_menu or not options:
                    pass
                elif options:
                    options = False
                    main_menu = True
            if event.key == pygame.K_KP0:
                if not debug_0 and debug:
                    debug_0 = True
                    GUIs.main_manager.set_visual_debug_mode(True)
                elif debug_0 and debug:
                    debug_0 = False
                    GUIs.main_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_KP1:
                if not debug_1 and debug:
                    debug_1 = True
                    GUIs.menu_manager.set_visual_debug_mode(True)
                elif debug_1 and debug:
                    debug_1 = False
                    GUIs.menu_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_KP2:
                if not debug_2 and debug:
                    debug_2 = True
                    GUIs.options_manager.set_visual_debug_mode(True)
                elif debug_2 and debug:
                    debug_2 = False
                    GUIs.options_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_KP3:
                if not debug_3 and debug:
                    debug_3 = True
                    GUIs.main_manager.set_visual_debug_mode(True)
                elif debug_3 and debug:
                    debug_3 = False
                    GUIs.main_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_i:
                if playing:
                    pass
                else:
                    pass

        # Initiate GUI manager, and let it listen to events.
        GUIs.main_manager.process_events(event)
        GUIs.menu_manager.process_events(event)
        GUIs.options_manager.process_events(event)
        GUIs.dialogue_manager.process_events(event)

    # Pretty self-explanatory. Just a main game.
    if playing and not options and not main_menu:
        # Setting player's starting position.
        if not is_in_a_start_position:
            for sprite in player.sprites():
                sprite.rect.center = buttons[13].rect.center
                is_in_a_start_position = True
        # Buttons and other events
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == eat_food:
                    if food >= 1 and hunger <= 90:
                        food -= 1
                        hunger += random.randint(10, 25)
                        if hunger > 100:
                            hunger = 100
                        hunger_label.set_text(f'Hunger: {hunger}')
                        canned_food.set_text(f'Canned Food: {food}')
                    else:
                        pass
                for button in buttons:
                    if event.ui_element == button:
                        if event.ui_element == button:
                            for sprite in player.sprites():
                                # Calculate the distance between the sprite and the button
                                dist = distance(sprite.rect.center, button.rect.center)
                                # Define a threshold distance
                                threshold = 155  # Adjust this value as needed
                                # Check if the distance is within the threshold and if the button represents a different tile
                                if dist <= threshold and (
                                        sprite.rect.center[0] != button.rect.center[0] or sprite.rect.center[1] !=
                                        button.rect.center[1]):
                                    sprite.rect.center = button.rect.center
                                    SoundsLibrary.walk_sound.play()
                                    hunger_label.set_text(f'Hunger: {hunger}')
                                    if hunger >= 50:
                                        health += 1
                                    elif hunger <= 25:
                                        health -= random.randint(1, 3)
                                    save(sprite)
                                    load(sprite)
                                    if button.text == "forest":
                                        hunger -= random.randint(3, 5)
                                    elif button.text == "city":
                                        hunger -= random.randint(2, 4)
                                    elif button.text == "city_center":
                                        hunger -= random.randint(4, 6)
                                    elif button.text == "lake":
                                        hunger -= random.randint(3, 5)
                                    else:
                                        hunger -= 1


        # Function to handle dialogue
        def handle_dialogue():
            # Display dialogue or perform any action you want when talking to NPCs in the city center
            pass  # Replace this with your dialogue logic


        # Inside the event loop
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == dialogue_button:
                    # Check if the player is in the city center
                    if "city_center" in map_data[row_idx][col_idx]:
                        handle_dialogue()

        # Update menu, since, we NEED to do that.
        GUIs.main_manager.update(dt)
        # Disabled this because we don't use it.
        # GUIs.main_panel.update(dt)

        # Fill the background with white color.
        screen.fill((255, 255, 255))  # Use RGB tuple for color

        # Draw tiles of specific locations.
        for i in range(len(map_data)):
            for m in range(len(map_data[i])):
                tile_position = (start_x + i * (movement_button_width + margin),
                                 start_y + m * (movement_button_height + margin))
                if map_data[m][i] == "plains":
                    screen.blit(Image_Library.plains_tile, tile_position)
                elif map_data[m][i] == "forest":
                    screen.blit(Image_Library.forest_time, tile_position)
                elif map_data[m][i] == "road_right":
                    screen.blit(Image_Library.road_right, tile_position)
                elif map_data[m][i] == "road_down":
                    screen.blit(Image_Library.road_down, tile_position)
                elif map_data[m][i] == "road_up":
                    screen.blit(Image_Library.road_up, tile_position)
                elif map_data[m][i] == "lake":
                    screen.blit(Image_Library.lake, tile_position)
                elif map_data[m][i] == "road_right_up":
                    screen.blit(Image_Library.road_left_up, tile_position)
                else:
                    screen.blit(Image_Library.plains_tile, tile_position)

        # Draw UI before the character
        GUIs.main_manager.draw_ui(screen)

        # Draw the player above everyone.
        player.draw(screen)

    # Main menu
    elif main_menu:
        options = False
        # Set volume of a music, can be changed.
        if not pygame.mixer.get_busy():
            SoundsLibrary.main_menu_sound.play(-1)
            # Make the music quieter.
            SoundsLibrary.main_menu_sound.set_volume(0.5)
        if debug:
            debug_label.set_text("DEBUG")
        # Update the main menu gui
        GUIs.menu_manager.update(dt)
        # Buttons processor.
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        # print("Start Game")
                        SoundsLibrary.confirm_sound.play()
                        SoundsLibrary.main_menu_sound.stop()
                        main_menu = False
                        playing = True
                    elif event.ui_element == options_button:
                        SoundsLibrary.hurt_sound.play()
                        # print("Options")
                        # confirm_sound.play()
                        # main_menu = False
                        # options = True
                    elif event.ui_element == quit_button:
                        # print("Quit!")
                        SoundsLibrary.confirm_sound.play()
                        running = False
                elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    if random.randint(0, 10) >= 5:
                        SoundsLibrary.hover_sound_1.play()
                    else:
                        SoundsLibrary.hover_sound_2.play()
        screen.blit(Image_Library.bg, (0, 0))
        # Draw UI
        GUIs.menu_manager.draw_ui(screen)

    # TODO: FIX Options.
    # elif options:
    #    main_menu = False
    #
    #    options_manager.update(dt)
    #
    #    for event in pygame.event.get():
    #        if event.type == pygame.USEREVENT:
    #            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
    #                confirm_sound.play()
    #                if event.ui_element == options_exit_button:
    #                    options = False
    #                    main_menu = True

    #    options_manager.draw_ui(screen)

    # Flip the display.

    if dialogue or playing:
        if not SoundsLibrary.ambient_channel.get_busy():
            SoundsLibrary.ambient_channel.play(SoundsLibrary.ambient_sound, loops=-1)  # loops=-1 for infinite looping
            # Make the music quieter.
            SoundsLibrary.ambient_channel.set_volume(0.5)

    elif dialogue:
        pass

    pygame.display.flip()
    # Delta Time, like ticks and etc.
    dt = clock.tick(60) / 1000

# When we finish main code - exit the program. Either by pressing X, or QUIT or if some error happens.
pygame.quit()
