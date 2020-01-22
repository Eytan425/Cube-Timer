"""Name: Philips Xu 
   Date: June 2, 2018
   Description: Sprites for Rubik's Cube Timer.
"""
import pygame, math, random

class Timer(pygame.sprite.Sprite):
    '''This class inherits from the Sprite class and displays a time.'''

    def __init__(self, size, x_pos, y_pos, colour, screen):
        '''This method initializes the Timer class and sets the numerous
        data attributes associated with the object.'''

        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        # Initialize instance variables
        self.__screen = screen
        self.__size = size
        self.__centerx = x_pos
        self.__top = y_pos
        self.__colour = colour
        self.__time = 0
        self.__timing = False
        self.__counting_down = False
        self.__done_counting = False
        self.__initial_time = 0
        self.__font = pygame.font.Font("Bungee-Regular.ttf", self.__size)

    def start_timer(self):
        '''Begin timer.'''

        self.__time = 0
        self.__timing = True
        self.__initial_time = pygame.time.get_ticks()

    def start_countdown(self):
        '''Indicates that the timer is counting down, not up.'''

        self.start_timer()
        self.__counting_down = True

    def get_timing(self):
        '''Returns whether the timer is running or not.'''
        return self.__timing

    def get_time(self):
        '''Get current time.'''
        return self.__time/1000.0

    def stop(self):
        '''Stop timing.'''
        self.__timing = False

    def hide(self):
        '''Hide timer.'''
        self.__top = -100

    def show(self):
        '''Display timer on screen.'''
        self.__top = self.__screen.get_height()/2

    def update(self):
        '''This method updates the message, renders the font and
        initializes the rect attributes for the Timer class.'''

        # Updates time (in milliseconds)
        if self.__timing:
            self.__time += pygame.time.get_ticks() - self.__initial_time
            self.__initial_time = pygame.time.get_ticks()


        # Set as timer (counting down only)
        if self.__counting_down:
            self.__time = 15000 - self.__time
            if self.__time <= 0:
                self.__counting_down = False
                self.__done_counting = True
                self.stop()
                self.__time = 0

        # Set messsage
        message = "%.3f s" % (self.__time/1000.0)

        # Change self.__time back (only applies to countdown timer)
        if self.__counting_down or self.__done_counting:
            self.__time = -1*(self.__time - 15000)
            self.__done_counting = False

        self.image = self.__font.render(message, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.top = self.__top
        self.rect.centerx = self.__centerx

class TextLabel(pygame.sprite.Sprite):
    '''This class inherits from the Sprite class and displays a message.'''

    def __init__(self, size, x_pos, y_pos, colour, screen):
        '''This method initializes the TextLabel class and sets the
        __size, __colour, and __message attributes It takes a size,
        x_pos, y_pos, colour, message and the screen as parameters..'''

        # Call the parent __init__() method
        pygame.sprite.Sprite.__init__(self)

        self.__screen = screen
        self.__size = size
        self.__centerx = x_pos
        self.__top = y_pos
        self.__colour = colour
        self.__message = ""
        self.__font = pygame.font.Font("Bungee-Regular.ttf", self.__size)

    def set_scramble(self, scramble):

        # Turns list into string
        str_scramble = " ".join(scramble)

        self.__message = str_scramble

    def set_text(self, text):
        self.__message = text

    def get_message(self):
        return self.__message

    def add_text(self, text):
        self.__message += "    " + text

    def show(self):
        self.__top = self.__screen.get_height()/2

    def hide(self):
        self.__top = -100

    def update(self):
        '''This method updates the message, renders the font and
        initializes the rect attributes for the TextLabel class.'''

        message = self.__message
        self.image = self.__font.render(message, 1, self.__colour)
        self.rect = self.image.get_rect()
        self.rect.top = self.__top
        self.rect.centerx = self.__centerx
