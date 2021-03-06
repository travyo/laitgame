import pygame
from pygame.locals import *
from . import static
import time, os
import importlib.util
import sys

PLAYSOUND="PLAYSOUND"
PLAYMUSIC="PLAYMUSIC"
LOADLEVEL="LOADLEVEL"
ADDSPELL="ADDSPELL"


def importer(path, settings):
    p = os.path.join(settings.actionsdir, path)
    if sys.version_info[1] >= 5:
        spec = importlib.util.spec_from_file_location(os.path.basename(p),p)
        actionlib = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(actionlib)
        return actionlib
    else:
        #NOTE: I have not tested this
        from importlib.machinery import SourceFileLoader
        actionlib = SourceFileLoader(os.path.basename(p), p).load_module()
        return actionlib

def has_function(actionlib, functioname):
    return functioname in list(actionlib.__dict__.keys())

def get_function(actionlib, functioname):
    return getattr(actionlib, functioname)


class Trigger(static.Static):
    def __init__(self,x,y,w,h, settings, actions, name, image=None, rows=None, cols=None, row=0, fpf=5, game=None):
        static.Static.__init__(self, x, y, w, h, settings, name, image, rows, cols, row, fpf, game)
        self.game = game
        self.actions = actions
        self.firstCollision = True
        self.do_actions('onload')


    def loadlevel(self, loadlevel):
        now = time.time()
        #Nonblocking wait ten seconds
        while time.time() - now < 10:
            #Need to test this - not sure it's ideal
            #But we need time for the other actions on the next level trigger to happen
            pass
        self.game.nextlevel = loadlevel

    def do_actions(self, event, *params):
        for action in self.actions:
            if not 'event' in action:
                print ('Missing EVENT for ',action)
        for action in [i for i in self.actions if i['event'] == event]:
            self.settings.debug('Action: %s' % action)
            actionlib = importer(action['script'], self.settings)
            get_function(actionlib, action['method'])(self, *params, **action['params']) 


    def update(self):
        self.do_actions('update')         

    def on_collide(self,sprite):
        if sprite.name == 'Player' and self.firstCollision:
            self.firstCollision = False
            self.do_actions('collision',sprite)

            
