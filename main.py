import pygame, pygame_gui, math, random, sys
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton, UILabel, UIPanel

debug = False
if sys.gettrace() is None:
    pass
else:
    debug = True

# Initializing pygame
pygame.init()

# Initial screen manipulations
screen_width = 1280
screen_height = 720
icon = pygame.transform.scale(pygame.image.load('snow.png'),(200, 200))
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Nuclear Wind 1.0a")
pygame.display.set_icon(icon)

# Sound library
hover_sound = pygame.mixer.Sound('data/sounds/hover.wav')
confirm_sound = pygame.mixer.Sound('data/sounds/Confirm.wav')
main_menu_sound = pygame.mixer.Sound('data/sounds/mainmenu.mp3')
hover_sound_1 = pygame.mixer.Sound('data/sounds/main_menu/Retro1.mp3')
hover_sound_2 = pygame.mixer.Sound('data/sounds/main_menu/Retro2.mp3')
walk_sound = pygame.mixer.Sound('data/sounds/movement/Steps.wav')
debug_active_sound = pygame.mixer.Sound('data/sounds/synth.wav')

# Image library
bg = pygame.image.load("data/sprites/bg.jpg")
plains_tile = pygame.image.load('data/sprites/tiles/plains.png')

# GUI managers
main_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
menu_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
options_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')
text_manager = pygame_gui.UIManager((screen_width, screen_height), 'theme.json')

# Variables
clock = pygame.time.Clock()
running = True
playing = False
main_menu = True
options = False
dt = 0
is_in_a_start_position = False
is_paused = False

# Game (Character) Variables
health = 0
hunger = 100

# Buttons and other shit
font_large = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)
button_width = 200
button_height = 50
button_list = []

# Map
map_data = [["forest", "plains", "plains", "road", "forest", "forest"],
            ["plains", "city", "road", "road", "plains", "forest"],
            ["city", "city_center", "forest", "plains", "lake", "plains"],
            ["forest", "road", "plains", "forest", "forest", "forest"],
            ["forest", "road", "forest", "plains", "forest", "plains"],
            ["road", "road", "plains", "hill", "forest", "forest"]]

movement_button_width = 100
movement_button_height = 100
start_x = 35
start_y = 35
margin = 2.5

# Movement system addition

def distance(point1, point2):
    x1, y1 = point1
    x2, y2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

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
            manager=main_manager,
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

game_name = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 100, button_width, button_height),
    text='Nuclear Winter',
    manager=menu_manager,
    object_id=ObjectID(class_id='@main_label')
)

start_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 250, button_width, button_height),
    text='Start Game',
    manager=menu_manager
)

options_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 350, button_width, button_height),
    text='Options',
    manager=menu_manager
)

quit_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 450, button_width, button_height),
    text='Quit',
    manager=menu_manager
)

version_label = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 0.1, 500, button_width, button_height),
    text='1.0a',
    manager=menu_manager
)

# END OF MAIN MENU BUTTONS

# START OF OPTION MENU BUTTONS

options_label = UILabel(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 100, button_width, button_height),
    text='Options',
    manager=options_manager,
    object_id=ObjectID(class_id='@main_label')
)

options_exit_button = UIButton(
    relative_rect=pygame.Rect((screen_width - button_width) // 2, 500, button_width, button_height),
    text='Exit Options',
    manager=options_manager
)

# END OF OPTION MENU BUTTONS

# START OF MAIN GAME PANEL

main_panel = UIPanel(pygame.Rect(675, -3, 610, 730),
                     manager=main_manager)
UILabel(pygame.Rect(245, 10, 150, 30),
        text='Nuclear Wind 1.0a',
        manager=main_manager,
        container=main_panel)
UILabel(pygame.Rect(10, 45, 150, 30),
        text=f'Health: {health}',
        manager=main_manager,
        container=main_panel)
hunger_label = UILabel(pygame.Rect(10, 75, 150, 30),
        text=f'Hunger: {hunger}',
        manager=main_manager,
        container=main_panel)

# END OF MAIN GAME PANEL

# Just existing for one class
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# If debug mode is active then skip main menu
if debug:
    main_menu = False
    playing = True
    options = False
    debug_active_sound.play()

# Initialize player class and blah blah blah. I don't really give a shit
class Player(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image_down = pygame.transform.scale(pygame.image.load('data/sprites/player/down_idle.png'), (width, height))
        self.image_up = pygame.transform.scale(pygame.image.load('data/sprites/player/up_idle.png'), (width, height))
        self.image_left = pygame.transform.scale(pygame.image.load('data/sprites/player/side_idle.png'), (width, height))
        self.image_right = pygame.transform.flip(self.image_left, True, False)
        self.image = self.image_down
        self.rect = self.image.get_rect()
        self.rect.x = player_pos.x
        self.rect.y = player_pos.y

# Initialize player in graphics idk
player = pygame.sprite.Group()
player.add(Player(60, 75))

# That's when shit hits the fan. a.k.a. main code
while running:
    debug_0 = False
    debug_1 = False
    debug_2 = False
    debug_3 = False
    # Thingy for letting players quit the game,
    # since, I want them to leave me as fast as they can
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
                if not debug_0:
                    debug_0 = True
                    main_manager.set_visual_debug_mode(True)
                elif debug_0:
                    debug_0 = False
                    main_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_KP1:
                if not debug_1:
                    debug_1 = True
                    menu_manager.set_visual_debug_mode(True)
                elif debug_1:
                    debug_1 = False
                    menu_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_KP2:
                if not debug_2:
                    debug_2 = True
                    options_manager.set_visual_debug_mode(True)
                elif debug_2:
                    debug_2 = False
                    options_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_KP3:
                if not debug_3:
                    debug_3 = True
                    main_manager.set_visual_debug_mode(True)
                elif debug_3:
                    debug_3 = False
                    main_manager.set_visual_debug_mode(False)
            if event.key == pygame.K_i:
                if playing:
                    pass
                else:
                    pass
        # I don't fucking know why we're initializing all the gui managers HERE
        # but I guess we need to do it firstly, above everyone else (such a narcissist)
        main_manager.process_events(event)
        menu_manager.process_events(event)
        options_manager.process_events(event)
        text_manager.process_events(event)

    # Main game, not menu or other shit
    if playing and not options and not main_menu:
        if not is_in_a_start_position:
            for sprite in player.sprites():
                sprite.rect.center = buttons[13].rect.center
                is_in_a_start_position = True
        # Buttons and other events
        for event in pygame.event.get():
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                for button in buttons:
                    if event.ui_element == button:
                        for sprite in player.sprites():
                            # Calculate the distance between the sprite and the button
                            dist = distance(sprite.rect.center, button.rect.center)
                            # Define a threshold distance
                            threshold = 155  # Adjust this value as needed
                            # Check if the distance is within the threshold
                            if dist <= threshold:
                                sprite.rect.center = button.rect.center
                                walk_sound.play()
                                hunger -= 1
                                print(hunger)
                                hunger_label.hide()
                                hunger_label = UILabel(pygame.Rect(10, 75, 150, 30),
                                                       text=f'Hunger: {hunger}',
                                                       manager=main_manager,
                                                       container=main_panel)

        # Update menu, since, we NEED to do that.
        main_manager.update(dt)
        main_panel.update(dt)

        # just so the screen isn't black, yknow?
        screen.fill((255, 255, 255))  # Use RGB tuple for color

        # Draw rectangles (optional, for visualization)
        for i in buttons:
            pygame.draw.rect(screen, 'green', i.rect)

        # Draw UI before the character
        main_manager.draw_ui(screen)

        # draw the main mf who's going to die in the next minute or so
        player.draw(screen)

    # main menu
    elif main_menu:
        options = False
        # Just so the player doesn't go insane due to a lot of guitar sounds
        if not pygame.mixer.get_busy():
            main_menu_sound.play(-1)
            # also make it quieter so we don't blow out his ear drums
            main_menu_sound.set_volume(0.5)
        # Update the main menu gui
        menu_manager.update(dt)
        # Button thingy
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == start_button:
                        print("Start Game")
                        confirm_sound.play()
                        main_menu_sound.stop()
                        main_menu = False
                        playing = True
                    elif event.ui_element == options_button:
                        print("Options")
                        confirm_sound.play()
                        main_menu = False
                        options = True
                    elif event.ui_element == quit_button:
                        print("Quit!")
                        confirm_sound.play()
                        running = False
                elif event.user_type == pygame_gui.UI_BUTTON_ON_HOVERED:
                    if random.randint(0,10) >= 5:
                        hover_sound_1.play()
                    else:
                        hover_sound_2.play()
        screen.blit(bg, (0, 0))
        # Draw UI
        menu_manager.draw_ui(screen)

    # CAUTION! MY SMALL BRAIN STILL DIDN'T FIXED THIS
    elif options:
        main_menu = False

        options_manager.update(dt)

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    confirm_sound.play()
                    if event.ui_element == options_exit_button:
                        options = False
                        main_menu = True

        options_manager.draw_ui(screen)

    # Sadly our game is not for australians
    pygame.display.flip()
    # Delta time so our character just doesn't go running around
    # like crazy, at least, if we'll have some animations in future.
    dt = clock.tick(60) / 1000

# Yea-yea, the infinity loop, I'm not into that shit so just end his suffering.
pygame.quit()
