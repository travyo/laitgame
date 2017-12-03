import pygame
from pygame.locals import *

class InputHandler(object):
    def __init__(self, settings,screen,flags):
        self.screen = screen
        self.settings = settings
        self.flags = flags
        if pygame.joystick.get_count():
            self.joystick = pygame.joystick.Joystick(0)
            self.joystick.init()

    def __reset_flags(self):
        self.keymap = {
        "up": [K_UP, K_w],
        "down": [K_DOWN, K_s],
        "left": [K_LEFT,K_a],
        "right": [K_RIGHT,K_d],
        "a": [K_1],
        "b": [K_2],
        "x": [K_3],
        "y": [K_4],
        "start": [K_RETURN, K_SPACE],
        "select": [K_ESCAPE]
        }
        self.joybtnmap = {
        0: "a",
        1: "b",
        2: "x",
        3: "y",
        6: "select",
        7: "start"
        }
        #4 and 5 are the shoulder buttons on a gamepad
        self.joyaxismap = {
        "lr":[0,3],
        "ud":[1,4]
        }
        self.quit = False

        for button in self.keymap:
            setattr(self, button, False)

    def get_events(self, scalefunc, menu=None):
        self.__reset_flags()
        for event in pygame.event.get():
            #TODO flag buttons on joystick events
            answer = ''
            if event.type == QUIT:
                self.quit = True
            elif event.type == KEYDOWN:
                for button in self.keymap:
                    if event.key in self.keymap[button]:
                        setattr(self, button, True)
            elif event.type == VIDEORESIZE:
                self.screen = pygame.display.set_mode(event.size,self.flags)
                self.settings.settingsdict['Resolution']['w'] = self.screen.get_width()
                self.settings.settingsdict['Resolution']['h'] = self.screen.get_height()
                self.settings.save_settings()
                scalefunc()
                pygame.display.flip()
            elif event.type == pygame.JOYBUTTONDOWN:
                if event.button in self.joybtnmap:
                    button = self.joybtnmap[event.button]
                    self.settings.logger.debug('Joy button %s pressed translating to %s' % (event.button, button))
                    setattr(self, button, True)
                else:
                    self.settings.logger.debug('Unknown joy button %s pressed' % event.button)
                    print (event.button)
            elif event.type == pygame.JOYBUTTONUP:
                if event.button in self.joybtnmap:
                    button = self.joybtnmap[event.button]
                    self.settings.logger.debug('Joy button %s pressed translating to %s' % (event.button, button))
                    setattr(self, button, False)
                else:
                    self.settings.logger.debug('Unknown joy button %s pressed' % event.button)
                    print (event.button)
            elif event.type == pygame.JOYAXISMOTION:
                #Our simple control scheme treats all axes and hats as equal
                for i in range(self.joystick.get_numaxes()):
                    axis = self.joystick.get_axis(i)
                    if axis != 0:
                        axisdir = None
                        for direction in self.joyaxismap:
                            if i in self.joyaxismap[direction]:
                                axisdir = direction
                                break
                        if axisdir and axisdir == 'lr':
                            if axis <0:
                                self.left = True
                            elif axis > 0:
                                self.right = True
                        elif axisdir == 'ud':
                            if axis <0:
                                self.up = True
                            elif axis > 0:
                                self.down = True
            elif event.type == pygame.JOYHATMOTION:
                lr,ud = event.value
                if lr == -1:
                    self.left = True
                elif lr == 1:
                    self.right = True
                if ud == 1:
                    self.up = True
                elif ud == -1:
                    self.down = True



            if menu:
                menu.react(event)
