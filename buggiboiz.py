__author__ = 'yournamehere'
import pygame, random


class Buggiboi:
    def __init__(self):
        """
        This is where we set up the variables for this particular object as soon as it is created.
        """
        self.x = random.randrange(400,600)
        self.y = random.randrange(0,600)
        self.vx = random.randrange(50,500)
        self.vy = random.randrange(50,500)
        self.i_am_alive = True

    def draw_self(self, surface):
        """
        It is this object's responsibility to draw itself on the surface. It will be told to do this often!
        :param surface:
        :return: None
        """
        pygame.draw.rect(surface, pygame.Color("green"), (self.x - 5, self.y - 5, 10, 10))

    def step(self, delta_T):
        """
        In order to change over time, this method gets called very often. The delta_T variable is the amount of time it
        has been since the last time we called "step()" usually about 1/20 -1/60 of a second.
        :param delta_T:
        :return: None
        """
        self.x = self.x + self.vx * delta_T
        self.y = self.y + self.vy * delta_T
        if self.x < 400:
            self.x = 400
            self.vx = self.vx * -1

        if self.x > 600:
            self.vx = self.vx * -1

        if self.y < 0:
            self.vy = self.vy * -1
        if self.y > 600:
            self.vy = self.vy * -1
    def is_dead(self):
        """
        lets another object know whether this object is still live and on the board. Used by the main loop to clear objects
        in need of removal.
        :return: True or False - is this object dead?
        """
        if self.i_am_alive:
            return False
        else:
            return True
        # alternative (1-line) version of this function:
        #  "return not self.i_am_alive"


    def die(self):
        """
        change the status of this object so that it is dead.
        :return: None
        """
        self.i_am_alive = False