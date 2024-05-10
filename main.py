import json
import math
import random
from datetime import datetime

import pygame_gui
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel, UIPanel

# Modules
from modules.libraries import ImageLibrary, SoundsLibrary
from modules.map import map_data
from modules.variables import *

now = datetime.now()
current_time = now.strftime("%H:%M:%S")

# Initializing pygame
pygame.init()


# GUI managers
class GUIs:
    main_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), './theme.json')
    menu_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), './theme.json')
    options_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), './theme.json')
    text_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), './theme.json')
    dialogue_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT), './theme.json')


clock = pygame.time.Clock()

# Buttons and other variables
font_large = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
button_width = 200
button_height = 50
button_list = []

# Movement system addition

movement_button_width = 100
movement_button_height = 100
start_x = 35
start_y = 35
margin = 2

# GAME MOVEMENT SYSTEM START

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


def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# START OF MAIN MENU BUTTONS

class Main_Menu_Buttons:
    game_name = UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, 100, button_width, button_height),
        text='Nuclear Winter',
        manager=GUIs.menu_manager,
        object_id=ObjectID(class_id='@main_label')
    )

    start_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, 250, button_width, button_height),
        text='Start Game',
        manager=GUIs.menu_manager
    )

    options_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, 350, button_width, button_height),
        text='Options',
        manager=GUIs.menu_manager
    )

    quit_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, 450, button_width, button_height),
        text='Quit',
        manager=GUIs.menu_manager
    )

    version_label = UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 0.1, 500, button_width, button_height),
        text='1.0a',
        manager=GUIs.menu_manager
    )

    debug_label = UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 0.1, 550, button_width, button_height),
        text='',
        manager=GUIs.menu_manager
    )


class Options_Elements:
    label = UILabel(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, 100, button_width, button_height),
        text='Options',
        manager=GUIs.options_manager,
        object_id=ObjectID(class_id='@main_label')
    )

    exit_button = UIButton(
        relative_rect=pygame.Rect((SCREEN_WIDTH - button_width) // 2, 500, button_width, button_height),
        text='Exit Options',
        manager=GUIs.options_manager
    )


class Main_Panel_Elements:
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

# pause_panel_bg = UIPanel(pygame.Rect(0, 0, 360, 480),
#                      manager=main_manager,
#                      anchors={'center':'center'})

# Pause Menu end

# Position of a player
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


# Initialize player class and player's sprites (unused, but, deleting it might break the entire code)
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image_down = pygame.transform.scale(pygame.image.load('data/sprites/player/alex.png'),
                                                 (width, height))
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

Main_Menu_Buttons.options_button.disable()

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
        else:
            pass
        # Buttons and other events
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == Main_Panel_Elements.eat_food:
                    if food >= 1 and hunger <= 90:
                        food -= 1
                        hunger += random.randint(10, 25)
                        if hunger > 100:
                            hunger = 100
                        Main_Panel_Elements.hunger_label.set_text(f'Hunger: {hunger}')
                        Main_Panel_Elements.canned_food.set_text(f'Canned Food: {food}')
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
                                    Main_Panel_Elements.hunger_label.set_text(f'Hunger: {hunger}')
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
                if event.ui_element == Main_Panel_Elements.dialogue_button:
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
                    screen.blit(ImageLibrary.plains_tile, tile_position)
                elif map_data[m][i] == "forest":
                    screen.blit(ImageLibrary.forest_time, tile_position)
                elif map_data[m][i] == "road_right":
                    screen.blit(ImageLibrary.road_right, tile_position)
                elif map_data[m][i] == "road_down":
                    screen.blit(ImageLibrary.road_down, tile_position)
                elif map_data[m][i] == "road_up":
                    screen.blit(ImageLibrary.road_up, tile_position)
                elif map_data[m][i] == "lake":
                    screen.blit(ImageLibrary.lake, tile_position)
                elif map_data[m][i] == "road_right_up":
                    screen.blit(ImageLibrary.road_left_up, tile_position)
                else:
                    screen.blit(ImageLibrary.plains_tile, tile_position)

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
        # Update the main menu gui
        GUIs.menu_manager.update(dt)
        # Buttons processor.
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == Main_Menu_Buttons.start_button:
                        SoundsLibrary.confirm_sound.play()
                        SoundsLibrary.main_menu_sound.stop()
                        main_menu = False
                        playing = True
                    elif event.ui_element == Main_Menu_Buttons.options_button:
                        SoundsLibrary.hurt_sound.play()
                    elif event.ui_element == Main_Menu_Buttons.quit_button:
                        SoundsLibrary.confirm_sound.play()
                        running = False
                elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    if random.randint(0, 10) >= 5:
                        SoundsLibrary.hover_sound_1.play()
                    else:
                        SoundsLibrary.hover_sound_2.play()
        screen.blit(ImageLibrary.bg, (0, 0))
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

    if dialogue or playing:
        if not SoundsLibrary.ambient_channel.get_busy():
            SoundsLibrary.ambient_channel.play(SoundsLibrary.ambient_sound, loops=-1)  # loops=-1 for infinite looping
            # Make the music quieter.
            SoundsLibrary.ambient_channel.set_volume(0.5)

    elif dialogue:
        pass

    # Flip the display.
    pygame.display.flip()
    # Delta Time, like ticks and etc.
    dt = clock.tick(60) / 1000

# When we finish main code - exit the program. Either by pressing X, or QUIT or if some error happens.
pygame.quit()
