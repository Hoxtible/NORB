__author__ = 'yournamehere'  # put your name here!!!

import pygame, sys, traceback, random, math
from pygame.locals import *

from shootyboi import Boi
from pewpewboi import Pew
from buggiboiz import Buggiboi
GAME_MODE_MAIN = 0
GAME_MODE_TITLE_SCREEN = 1

# import your classFiles here.

# =====================  setup()
def setup():
    """
    This happens once in the program, at the very beginning.
    """
    global buffer, objects_on_screen, objects_to_add, bg_color, game_mode
    global shootyboi, pew, pew_list, bug, bug_list, bugs_shot, shots_fired, game_over

    global mouse_location
    buffer = pygame.display.set_mode((600, 600))
    objects_on_screen = []  # this is a list of all things that should be drawn on screen.
    objects_to_add = [] #this is a list of things that should be added to the list on screen. Put them here while you
                        #   are in the middle of the loop, and they will be added in later in the loop, when it is safe
                        #   to do so.
    pew_list = []
    bug_list = []
    bg_color = pygame.Color("royalblue4")  # you can find a list of color names at https://goo.gl/KR7Pke
    game_mode = GAME_MODE_MAIN
    # Add any other things you would like to have the program do at startup here.
    mouse_location = [0,0]
    shootyboi = Boi()
    pew = Pew()
    bug = Buggiboi()
    game_over = False
    bugs_shot = 0
    shots_fired = 0
    objects_on_screen.append(shootyboi)
    for i in range(2):
        new_bug = Buggiboi()
        bug_list.append(new_bug)
        objects_on_screen.append(new_bug)

# =====================  loop()
def loop(delta_T):
    global clear_text
    """
     this is what determines what should happen over and over.
     delta_T is the time (in seconds) since the last loop() was called.
    """
    buffer.fill(bg_color) # wipe the screen with the background color.
    if game_mode == GAME_MODE_MAIN:
        animate_objects(delta_T)

        # place any other code to test interactions between objects here. If you want them to
        # disappear, set them so that they respond True to isDead(), and they will be deleted next. If you want to put
        # more objects on screen, add them to the global variable objects_to_add, and they will be added later in this
        # loop.


        clear_dead_objects()
        add_new_objects()
        draw_objects()
        if game_over == False:
            show_stats(delta_T) #optional. Comment this out if it annoys you.
        bug_shot()
        check_for_death()

    pygame.display.flip()  # updates the window to show the latest version of the buffer.


# =====================  animate_objects()
def animate_objects(delta_T):
    """
    tells each object to "step"...
    """
    global objects_on_screen
    for object in objects_on_screen:
        if object.is_dead(): #   ...but don't bother "stepping" the dead ones.
            continue
        object.step(delta_T)


# =====================  clear_dead_objects()
def clear_dead_objects():
    """
    removes all objects that are dead from the "objectsOnScreen" list
    """
    global objects_on_screen
    i = 0
    for object in objects_on_screen[:]:
        if object.is_dead():
            objects_on_screen.pop(i) # removes the ith object and pulls everything else inwards, so don't advance "i"
                                     #      ... they came back to you.
        else:
            i += 1
    global pew_list
    i = 0
    for pew in pew_list[:]:
        if pew.is_dead():
            pew_list.pop(i)  # removes the ith object and pulls everything else inwards, so don't advance "i"
            #      ... they came back to you.
        else:
            i += 1
    global bug_list
    i = 0
    for bug in bug_list[:]:
        if bug.is_dead():
            bug_list.pop(i)  # removes the ith object and pulls everything else inwards, so don't advance "i"
            #      ... they came back to you.
        else:
            i += 1

# =====================  add_new_objects()
def add_new_objects():
    """
    Adds all the objects in the list "objects to add" to the list of "objects on screen" and then clears the "to add" list.
    :return: None
    """
    global objects_to_add, objects_on_screen
    objects_on_screen.extend(objects_to_add)
    objects_to_add.clear()

# =====================  draw_objects()
def respawn_bug(amount_of_bugs):
    for i in range(amount_of_bugs):
        new_bug = Buggiboi()
        bug_list.append(new_bug)
        objects_on_screen.append(new_bug)
def draw_objects():
    """
    Draws each object in the list of objects.
    """
    for object in objects_on_screen:
        object.draw_self(buffer)

# =====================  show_stats()



def shoot(to_x,to_y):
    global objects_on_screen, pew, shootyboi, pew_list, shots_fired, game_over
    boi_x = shootyboi.x
    boi_y = shootyboi.y
    bullet = Pew()
    pygame.mixer.music.load('shootsound.mp3')
    pygame.mixer.play(0)
    objects_on_screen.append(bullet)
    pew_list.append(bullet)
    bullet.x = boi_x
    bullet.y = boi_y
    dx = abs(to_x - boi_x)
    dy = abs(to_y - boi_y)
    d = math.sqrt(dx*dx + dy*dy)
    if boi_x > to_x:

        bullet.vx = -dx
    else:
        bullet.vx = dx
    if boi_y > to_y:

        bullet.vy = -dy
    else:
        bullet.vy = dy

    print(bullet.vx)
    print(bullet.vy)
    shots_fired += 1
def bug_shot():
    global bugs_shot, bug_list, pew_list, objects_on_screen, shootyboi
    for bug in bug_list:
        for pew in pew_list:
            if abs((pew.x - 0)-(bug.x - 0)) <=12 and abs((pew.y - 0)-(bug.y - 0)) <=12: 
                 print("BANG BANG")
                 pew.die()
                 bug.die()
                 pygame.mixer.music.load('deathsound.mp3')
                 pygame.mixer.play(0)
                 bugs_shot += 1
                 respawn_bug(1)
        if abs((shootyboi.x - 0) - (bug.x - 0)) <= 12 and abs((shootyboi.y - 0) - (bug.y - 0)) <= 12:
            shootyboi.die()
            death_screen()

def death_screen():
    global objects_on_screen, clear_text
    clear_text = True
    game_over_text()
    for objects in objects_on_screen:
        objects.die()
def game_over_text():
    global shots_fired, bugs_shot
    stats_font = pygame.font.SysFont('Comic Sans MS', 60)
    game_string = "Game Over"  # build a string with the number of objects
    game_text_surface = stats_font.render(game_string, True, pygame.Color("Blue"))
    game_text_rect = game_text_surface.get_rect()
    game_text_rect.left = buffer.get_rect().left + 150  # move this box to the lower right corner
    game_text_rect.top = buffer.get_rect().top + 250
    buffer.blit(game_text_surface, game_text_rect)

    percent_font = pygame.font.SysFont('Comic Sans MS', 30)
    accuracy = bugs_shot/shots_fired *100
    percent_string = "Accuracy: {0}%".format(accuracy)  # build a string with the number of objects
    percent_text_surface = stats_font.render(percent_string, True, pygame.Color("Red"))
    percent_text_rect = game_text_surface.get_rect()
    percent_text_rect.left = buffer.get_rect().left + 100  # move this box to the lower right corner
    percent_text_rect.top = buffer.get_rect().top + 300
    buffer.blit(percent_text_surface, percent_text_rect)


def check_for_death():
    global shots_fired
    if shots_fired > 100:
        death_screen()



def show_stats(delta_T):

    """
    draws the frames-per-second in the lower-left corner and the number of objects on screen in the lower-right corner.
    Note: the number of objects on screen may be a bit misleading. They still count even if they are being drawn off the
    edges of the screen.
    :param delta_T: the time since the last time this loop happened, used to calculate fps.
    :return: None
    """
    bugs_text = str(bugs_shot)
    shot_text = str(shots_fired)
    white_color = pygame.Color(255,255,255)
    stats_font = pygame.font.SysFont('Comic Sans MS', 10)

    fps_string = "FPS: {0:3.1f}".format(1.0/delta_T) #build a string with the calculation of FPS.
    fps_text_surface = stats_font.render(fps_string,True,white_color) #this makes a transparent box with text
    fps_text_rect = fps_text_surface.get_rect()   # gets a copy of the bounds of the transparent box
    fps_text_rect.left = 10  # now relocate the box to the lower left corner
    fps_text_rect.bottom = buffer.get_rect().bottom - 10
    buffer.blit(fps_text_surface, fps_text_rect) #... and copy it to the buffer at the location of the box

    objects_string = "Objects: {0:5d}".format(len(objects_on_screen)) #build a string with the number of objects
    objects_text_surface = stats_font.render(objects_string,True,white_color)
    objects_text_rect = objects_text_surface.get_rect()
    objects_text_rect.right = buffer.get_rect().right - 10 # move this box to the lower right corner
    objects_text_rect.bottom = buffer.get_rect().bottom - 10
    buffer.blit(objects_text_surface, objects_text_rect)

    bugs_string = "Bugs Shot: {0}".format(bugs_text) # build a string with the number of objects
    bugs_text_surface = stats_font.render(bugs_string, True, white_color)
    bugs_text_rect = bugs_text_surface.get_rect()
    bugs_text_rect.right = buffer.get_rect().right - 10  # move this box to the lower right corner
    bugs_text_rect.top = buffer.get_rect().top + 10
    buffer.blit(bugs_text_surface, bugs_text_rect)

    shot_string = "Shots Fired: {0}".format(shot_text)  # build a string with the number of objects
    shot_text_surface = stats_font.render(shot_string, True, white_color)
    shot_text_rect = shot_text_surface.get_rect()
    shot_text_rect.left = buffer.get_rect().left + 10  # move this box to the lower right corner
    shot_text_rect.top = buffer.get_rect().top + 10
    buffer.blit(shot_text_surface, shot_text_rect)

# =====================  read_events()
def read_events():

    """
checks the list of events and determines whether to respond to one.
"""
    global mouse_location, pew_list
    events = pygame.event.get()  # get the list of all events since the last time
    for evt in events:
        if evt.type == QUIT:
            pygame.quit()
            raise Exception("User quit the game")
            # You may decide to check other events, like the mouse
            # or keyboard here.
        if evt.type == KEYDOWN:
            shootyboi.vx = 0
            shootyboi.vy = 0
            if evt.key == K_a:
                shootyboi.left_is_pressed = True
            if evt.key == K_d:
                shootyboi.right_is_pressed = True
            if evt.key == K_w:
                shootyboi.up_is_pressed = True
            if evt.key == K_s:
                shootyboi.down_is_pressed = True

        if evt.type == KEYUP:
            shootyboi.vx = 0
            shootyboi.vy = 0
            if evt.key == K_a:
                shootyboi.left_is_pressed = False
            if evt.key == K_d:
                shootyboi.right_is_pressed = False
            if evt.key == K_w:
                shootyboi.up_is_pressed = False
            if evt.key == K_s:
                shootyboi.down_is_pressed = False
        if evt.type == MOUSEBUTTONDOWN:
            if game_over == False:
                if len(pew_list) <= 3:
                    mouse_location = evt.pos
                    print("meme")
                    shoot(mouse_location[0],mouse_location[1])


# program start with game loop - this is what makes the loop() actually loop.
pygame.init()
try:
    setup()
    fpsClock = pygame.time.Clock()  # this will let us pass the deltaT to loop.
    while True:
        time_since_last_loop = fpsClock.tick(60) / 1000.0 # we set this to go up to as much as 60 fps, probably less.
        loop(time_since_last_loop)
        read_events()

except Exception as reason: # If the user quit, exit gracefully. Otherwise, explain what happened.
    if len(reason.args)>0 and reason.args[0] == "User quit the game":
        print ("Game Over.")
    else:
        traceback.print_exc()
