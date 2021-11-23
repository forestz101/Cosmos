"""
-------------------------------------------------------------------------------
Name:		game.py

Purpose:	Cosmos is a game where the objective is to jump higher and higher
            on the platforms without falling off!

Authors:    Zhou.F
            Zhuang.J  

Created:	17/06/2019
------------------------------------------------------------------------------
"""

import arcade
from random import randint

screen_width = 800
screen_height = 600

player_x = 60
player_y = 0
jump_h = 0
up = -20

hit_d = False
hit_l = False
hit_r = False

left_pressed = False
right_pressed = False
instructions_number = 0

start = False
intro = True
lost = False
direction = True
ascending = False

height_increments = [38, 72, 102, 128, 150]
lateral_direction = [1, -1]

block_height = [38, 110, 212]
block_left_side = [153, 353, 223]
block_right_side = [257, 457, 327]

shift = 0
block_count = 3
high_score = 0
time = 0
count = 0

# load sounds
splat_sound = arcade.load_sound("sounds/pihtas.mp3")
whoosh_sound = arcade.load_sound("sounds/whoosh.mp3")
meep_sound = arcade.load_sound("sounds/meepbeep.mp3")

# load images
texture_stars = arcade.load_texture("images/starrr.png")
texture_ship = arcade.load_texture("images/zoomwoom.png")
texture_died = arcade.load_texture("images/splotplat.png")

texture_spicy = arcade.load_texture("images/chilli.png")
texture_pepper = arcade.load_texture("images/jalapeno.png")
texture_rocks = arcade.load_texture("images/space_rocks.png")
texture_planet_1 = arcade.load_texture("images/planet_1.png")
texture_planet_2 = arcade.load_texture("images/planet_2.png")
texture_planet_3 = arcade.load_texture("images/planet_3.png")

# start position for animations
ship_x = 0
ship_y = 550
char_x = 710
char_y = 470

planet_x = [0, 0, 0]
planet_y = [700, 700, 700]
planet_index = [0, 0, 0]
planet_speed = [0, 0, 0]
planets = [texture_planet_1, texture_planet_2, texture_planet_3]

play_whoosh = True
play_meep = True


def on_update(delta_time):
    """
    calls all functions and controls lateral payer movement

    :return: (int) the x position of the character
    """
    global left_pressed, right_pressed, player_x, start, block_count

    if not intro:
        start = True

    if left_pressed and not hit_l and start:
        player_x -= 8

    if right_pressed and not hit_r and start:
        player_x += 8

    if start:
        reset(block_height, block_left_side, block_right_side, planet_index)
        check_hit()
        jumping()
        new_platforms(block_left_side, block_right_side, block_height)
        shifting()
        planet(planet_x, planet_y, planet_index, planet_speed)

    block_count = len(block_height) - 1


def check_hit():
    """
    detects collisions between the character and its environment

    :return: (bool) if the character has collided and where the collision occurred
    """
    global hit_d, hit_l, hit_r

    hit_d = False
    hit_r = False
    hit_l = False

    # checks to see if the character has hit the edge of the screen
    if player_x <= 20:
        hit_l = True
    if player_x >= 780:
        hit_r = True

    # a loop to check if the character has hit any platform or the bottom of the screen
    # gathers the coordinates of obstacles from related lists (block_height, block_left_side, Block_right_side)
    for i in range(beginning, count + 1):
        if block_left_side[i] < player_x < block_right_side[i] and jump_h + player_y == block_height[i]:
            hit_d = True
        elif player_y + jump_h <= 0:
            hit_d = True


def jumping():
    """
        uses a quadratic equation to animate a jumping motion

        :return: (float) the vertical position of the character
    """
    global hit_d, jump_h, player_y, up, count

    # resets the base from which the character will jump from once it has landed on a platform
    # keeps track of how many platforms the character has landed on
    if hit_d and up > 0:
        if jump_h != 0:
            count += 1
        up = -20
        player_y += jump_h
        jump_h = 0

    jump_h = 0.5 * -up ** 2 + 200
    up += 1


def new_platforms(left, right, height):
    """
    randomly generates new platforms for the character to land on

    :param left: the list of variables defining the left side of the platforms
    :param right: the list of variables defining the right side of the platforms
    :param height: the list of variables defining the height of the platforms
    :return: (int, list) the new horizontal and vertical positions of the platforms
    """

    # generate a new platform only if the player is within 350 pixels of the highest platform
    if (height[block_count] - player_y) < 350:

        # ensures that no platforms are generated completely off the screen
        if left[block_count] <= 180:
            lateral_v = 1
            new_height = height[block_count] + height_increments[randint(2, 4)]
        elif right[block_count] >= 540:
            lateral_v = -1
            new_height = height[block_count] + height_increments[randint(2, 4)]
        else:
            lateral_v = lateral_direction[randint(0, 1)]
            new_height = height[block_count] + height_increments[randint(0, 4)]

        lateral_d = randint(8, 20) * 10

        # appends new values to lists
        height.append(new_height)
        left.append(left[block_count] + lateral_d * lateral_v)
        right.append(right[block_count] + lateral_d * lateral_v)


def planet(x, y, index, speed):
    """
    randomly generates planets in new locations

    :param x: list of x positions of the planets
    :param y: list of y positions of the planets
    :param index: list that tells the program which planets have been displayed
    :param speed: list of how fast the planets move down the screen
    :return: (int, list) the locations of the planets
    """

    # randomly decides to display a planet if that particular planet is not already displayed
    # randomly generates coordinates for the planets as well as how fast they will move
    for i in range(3):
        if index[i] == 0:
            if randint(0, 600) == 450:
                y[i] = 700
                index[i] = 1
                x[i] = randint(50, screen_width - 50)

                # prevents overlapping planets
                overlap = True
                while overlap:
                    overlap = False
                    for n in range(3):
                        if n == i or index[n] == 0:
                            pass
                        elif x[n] - 100 < x[i] < x[n] + 100:
                            x[i] = randint(80, screen_width - 80)
                            overlap = True

                speed[i] = randint(3, 15) / 10

    # moves planets down
    for i in range(3):
        if ascending and index[i] == 1:
            y[i] -= 1 * speed[i]

    # deletes planets once they fall below the screen
    for i in range(3):
        if y[i] < -50:
            index[i] = 0


def shifting():
    """
        shift the screen down as the player progresses up through the game

        :return: (int) the amount in which the program will shift the screen down
    """
    global shift, ascending

    if player_y - shift > 200:
        shift += 5
        ascending = True
    else:
        ascending = False


def reset(height, right, left, index):
    """
        reset values to restart the game once the player has lost

        :param left: the list of variables defining the left side of the platforms
        :param right: the list of variables defining the right side of the platforms
        :param height: the list of variables defining the height of the platforms
        :param index: list that tells the program which planets have been displayed
        :return: (int, bool) the original values of all parameters
    """
    global player_y, player_x, jump_h, intro, start, up, shift, lost, count, block_count

    # if the character falls below the screen, reset all game parameters and display the losing screen
    if player_y + jump_h - shift < 0:

        arcade.play_sound(splat_sound)

        start = False
        intro = True
        lost = True

        # delete all the information about previously generated platforms
        for i in range(block_count - 2):
            del height[3]
            del right[3]
            del left[3]

        # resets planets
        for i in range(3):
            index[i] = 0

        # resets parameters for the location of the character
        player_y = 0
        player_x = 60
        jump_h = 0
        up = -20
        shift = 0
        count = 0

        block_count = len(block_height) - 1


def on_draw():
    """
    updates all the visual aspects of the game and renders appropriate graphics
    """
    global beginning

    arcade.start_render()

    # background
    arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, 1 * texture_stars.width,
                                  1 * texture_stars.height, texture_stars, 0)

    # draws planets
    for i in range(3):
        if planet_index[i] == 1:
            arcade.draw_texture_rectangle(planet_x[i], planet_y[i],
                                          0.27 * planets[i].width, 0.27 * planets[i].height, planets[i])

    arcade.draw_rectangle_filled(400, 300, 800, 600, [0, 0, 0, 70])

    # displays only the last 8 platforms to save computing power
    if block_count < 8:
        beginning = 0
    else:
        beginning = block_count - 8

    # draws the platforms
    for i in range(beginning, block_count):
        arcade.draw_texture_rectangle(block_left_side[i] + 52, block_height[i] - 5 - shift, 0.3 * texture_rocks.width,
                                      0.3 * texture_rocks.height, texture_rocks, 0)

    character(player_x, player_y + jump_h - shift + 30)

    score()
    menu()
    instructions_1()
    losing_screen()


def character(x, y):
    """
    keeps track of the player's score and their high score

    :param x: x coordinate of the character
    :param y: y coordinate of the character
    """
    global direction

    if left_pressed:
        direction = False
    if right_pressed:
        direction = True

    # makes the character face the direction of travel
    if direction:
        arcade.draw_texture_rectangle(x, y, 0.15 * texture_spicy.width, 0.15 * texture_spicy.height, texture_spicy)
    if not direction:
        arcade.draw_texture_rectangle(x, y, 0.15 * texture_pepper.width, 0.15 * texture_pepper.height, texture_pepper)


def whoosh():
    """
    plays sound once
    """
    global play_whoosh

    if play_whoosh:
        arcade.play_sound(whoosh_sound)
        play_whoosh = False


def meep():
    """
    plays sound once
    """
    global play_meep

    if play_meep:
        arcade.play_sound(meep_sound)
        play_meep = False


def score():
    """
    keeps track of the player's score and their high score

    :return: (int) current and high score of the player
    """
    global high_score

    arcade.draw_rectangle_filled(400, 580, 800, 80, [0, 0, 0, 100])

    # tracks the score of the player based on the y value of the character
    if start:
        arcade.draw_text("{0:^10}".format(str(int(player_y))), 340, 550, arcade.color.ASH_GREY, 36,
                         font_name='Comic Sans MS')
        text_enter = "Click ENTER for instructions"
        arcade.draw_text(text_enter, 450, 30, arcade.color.WHITE, 18, font_name='Comic Sans MS')

    # updates the high score
    if player_y > high_score:
        high_score = int(player_y)


def menu():
    """
    sets up the menu screen
    """

    # if the game is not running, display the menu screen
    if intro and instructions_number == 0:
        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, 1 * texture_stars.width,
                                      1 * texture_stars.height, texture_stars, 0)
        arcade.draw_texture_rectangle(700, 500, 0.8 * texture_ship.width, 0.8 * texture_ship.height, texture_ship, -25)

        arcade.draw_rectangle_filled(400, 320, 400, 70, arcade.color.ORANGE, 0)
        text_start = "{0:^27}".format("Click SPACE to start!")
        arcade.draw_text(text_start, 220, 305, arcade.color.WHITE, 24, font_name='Comic Sans MS')

        high_score_txt = "High score: " + str(high_score)
        arcade.draw_text(high_score_txt, 330, 110, arcade.color.WHITE, 24, font_name='Comic Sans MS')

        arcade.draw_rectangle_filled(400, 220, 480, 70, arcade.color.ORANGE, 0)
        text_instru = "Click ENTER for instructions"
        arcade.draw_text(text_instru, 190, 210, arcade.color.WHITE, 24, font_name='Comic Sans MS')
        arcade.draw_texture_rectangle(300, 390, 0.2 * texture_spicy.width, 0.2 * texture_spicy.height, texture_spicy)


def instructions_1():
    """
    animates and displays the instruction screens

    :return: (int) the coordinates of the ship and character
    """
    global ship_x, ship_y, char_x, char_y, play_whoosh, play_meep, instructions_number

    if 0 < instructions_number < 4:
        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, texture_stars.width,
                                      texture_stars.height, texture_stars, 0)

    # displays the first set on instructions
    if instructions_number == 1:
        # moves the ship towards the right
        if ship_x != 700 and char_y != 100:
            arcade.draw_rectangle_filled(470, 100, 50, 50, arcade.color.BLACK)
            ship_x += 10
            ship_y -= 1

        # stops the ship, draws the light triangle, and moves the character down
        elif ship_x == 700 and char_y != 100:
            arcade.draw_triangle_filled(710, 500, 400, 200, 700, 100, arcade.color.BABY_BLUE)
            arcade.draw_texture_rectangle(700, 480, 0.8 * texture_ship.width, 0.8 * texture_ship.height,
                                          texture_ship, -25)
            meep()
            char_x -= 3
            char_y -= 5
            arcade.draw_texture_rectangle(char_x, char_y, 0.15 * texture_spicy.width,
                                          0.15 * texture_spicy.height, texture_spicy)

        # moves the ship off the screen, draws the first text panel
        else:
            ship_x += 10
            ship_y -= 1
            arcade.draw_texture_rectangle(490, 100,
                                          0.2 * texture_spicy.width, 0.2 * texture_spicy.height, texture_spicy)
            text_panel_1()

        arcade.draw_texture_rectangle(ship_x, ship_y, 0.8 * texture_ship.width, 0.8 * texture_ship.height,
                                      texture_ship, -25)
        whoosh()

    # draws the second text panel
    if instructions_number == 2:
        text_panel_2()
        arcade.draw_texture_rectangle(600, 260, 0.3 * texture_spicy.width, 0.3 * texture_spicy.height, texture_spicy)

    # draws the third text panel
    if instructions_number == 3:
        text_panel_3()
        arcade.draw_texture_rectangle(500, 260, 0.3 * texture_spicy.width, 0.3 * texture_spicy.height, texture_spicy)

    # resets the text panels
    if instructions_number > 3:
        instructions_number = 0
        ship_x = 0
        ship_y = 550
        char_x = 710
        char_y = 470
        play_meep = True
        play_whoosh = True


def text_panel_1():
    """
    the first instruction panel
    """

    arcade.draw_rectangle_filled(230, 210, 270, 70, arcade.color.ORANGE)
    text_hi = "This is Sploogy"
    arcade.draw_text(text_hi, 100, 200, arcade.color.WHITE, 24, font_name='Comic Sans MS')

    text_next = "Press ENTER to continue"
    arcade.draw_text(text_next, 100, 150, arcade.color.WHITE, 20, font_name='Comic Sans MS')


def text_panel_2():
    """
    the second instruction panel
    """

    arcade.draw_rectangle_filled(310, 470, 460, 160, arcade.color.ORANGE)
    text_help = "Help Sploogy explore the" '\n' "universe by jumping higher" '\n' "and higher on the blocks"
    arcade.draw_text(text_help, 100, 500, arcade.color.WHITE, 24, font_name='Comic Sans MS')

    arcade.draw_rectangle_filled(260, 180, 350, 100, arcade.color.ORANGE)
    text_move = "Press left and right" '\n' "arrows to move"
    arcade.draw_text(text_move, 100, 190, arcade.color.WHITE, 24, font_name='Comic Sans MS')

    text_next = "Press ENTER to continue"
    arcade.draw_text(text_next, 200, 100, arcade.color.WHITE, 20, font_name='Comic Sans MS')


def text_panel_3():
    """
    the third instruction panel
    """

    arcade.draw_rectangle_filled(360, 180, 550, 100, arcade.color.ORANGE)
    text_go = "Let's Go!"
    text_press = "Press 'ENTER' to return to menu"
    arcade.draw_text(text_go, 100, 190, arcade.color.WHITE, 24, font_name='Comic Sans MS')
    arcade.draw_text(text_press, 100, 140, arcade.color.WHITE, 24, font_name='Comic Sans MS')


def losing_screen():
    """
    sets up the losing screen

    :return: (int) the time until the screen will revert to the main menu
    """
    global time, lost

    # draw the losing screen
    if lost:
        time += 1

        arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2, 1 * texture_stars.width,
                                      1 * texture_stars.height, texture_stars, 0)
        arcade.draw_rectangle_filled(400, screen_height // 2, 400, 100, arcade.color.WHITE)
        text_start = "Whoops, You Slipped and Died"
        arcade.draw_text(text_start, 230, 290, arcade.color.BLACK, 20)
        arcade.draw_texture_rectangle(400, 150, 0.5 * texture_died.width, 0.5 * texture_died.height, texture_died, 0)

    # the losing screen will disappear in one second and revert to the menu screen without user interference
    # if the user presses the space bar they will immediately start a new game
    if time > 90:
        time = 0
        lost = False
    elif start:
        time = 0
        lost = False


def on_key_press(key, modifiers):
    """
    detects if any keys have been pressed

    :return: (bool) the specific key that has been pressed
    """
    global right_pressed, left_pressed, intro, instructions_number

    if key == arcade.key.LEFT:
        left_pressed = True
    if key == arcade.key.RIGHT:
        right_pressed = True
    if key == arcade.key.SPACE:
        intro = False
    if key == arcade.key.ENTER:
        instructions_number += 1


def on_key_release(key, modifiers):
    """
    detects if any keys have been released

    :return: (bool) the specific key that has been released
    """
    global right_pressed, left_pressed

    if key == arcade.key.LEFT:
        left_pressed = False
    if key == arcade.key.RIGHT:
        right_pressed = False


def setup():
    """
    opens a window and sets up the window
    """

    arcade.open_window(800, 600, "My Arcade Game")
    arcade.set_background_color(arcade.color.BLUE_GRAY)
    arcade.draw_texture_rectangle(screen_width // 2, screen_height // 2,
                                  screen_width, screen_width, texture_stars, 0)
    arcade.schedule(on_update, 1/60)

    # Override arcade window methods
    window = arcade.get_window()
    window.on_draw = on_draw
    window.on_key_press = on_key_press
    window.on_key_release = on_key_release

    arcade.run()


if __name__ == '__main__':
    setup()
