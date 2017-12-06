import pygame
from pygame.locals import *
from .barrier import Barrier
from .ladder import Ladder
import yaml
import os


class Level(object):
    def __init__(self,levelfile, settings, screen):
        self.levelfile = levelfile
        self.settings = settings
        self.leveldict = yaml.safe_load(open(os.path.join(self.settings.leveldir,levelfile)))
        self.playerx = self.leveldict['player_pos']['x']
        self.playery = self.leveldict['player_pos']['y']
        if self.playerx == 'center':
            self.playerx = screen.get_width() / 2
        if self.playery == 'center':
            self.playery = screen.get_height() / 2
        self.background_mode = self.leveldict['background_mode']
        self.background = pygame.image.load(os.path.join(settings.bgdir,self.leveldict['background']))
        self.background = pygame.transform.smoothscale(self.background,(1920,834))
        self.width = self.leveldict['width']
        self.music = self.leveldict['music']
        assert self.background_mode in ['follow','tile','stretch']

    def get_barriers(self):
        for b in self.leveldict['barriers']:
            name = None
            if 'name' in b:
                name = b['name']
            yield Barrier(b['x'],b['y'],0,0, self.settings, name=name, image=b['image'])

    def get_ladders(self):
        for b in self.leveldict['ladders']:
            name = None
            if 'name' in b:
                name = b['name']
            yield Ladder(b['x'],b['y'], self.settings, name=name, image=b['image'])


    def save():
        #TODO - for editor
        pass