# -*- coding: utf-8 -*-

# KezMenu - By Luca Fabbri
# This code is released under GPL license
# ---------------------------------------------------------------
# This work is based on the original EzMeNu script, released from
# PyMike, from the Pygame community
# See http://www.pygame.org/project/855/
# ---------------------------------------------------------------

import pygame

__author__ = "Keul - lucafbb AT gmail.com"
__version__ = "0.2.1"

__description__ = "A simple and basical PyGame based module for a fast development of menu interfaces"

class KezMenu(object):
    """A simple but complete class to handle menu using pygame"""

    def __init__(self, *options):
        """Initialise the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = options
        self.x = 0
        self.y = 0
        self.option = 0
        self.width = 1
        self.color = (0, 0, 0, 0)
        self.hcolor = (255, 0, 0, 0)
        self.mouse_focus = False
        try:
            self.font = pygame.font.Font(None, 32)
            self.height = len(self.options)*self.font.get_height()
            self._fixWidth()
        except:
            pass

    def _fixWidth(self):
        for o in self.options:
            text = o[0]
            ren = self.font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()

    def draw(self, surface):
        """Draw the menu to the surface."""
        i=0
        for o in self.options:
            if i==self.option:
                clr = self.hcolor
            else:
                clr = self.color
            text = o[0]
            ren = self.font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + i*self.font.get_height()))
            i+=1
            
    def update(self, events):
        """Update the menu and get input for the menu."""
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.options[self.option][1]()
            # Mouse controls
            elif e.type == pygame.MOUSEBUTTONDOWN:
                lb, cb, rb = pygame.mouse.get_pressed()
                if lb and self.mouse_focus:
                    self.options[self.option][1]()
                
        if self.option > len(self.options)-1:
            self.option = len(self.options)-1
        elif self.option < 0:
            self.option = 0
        # Check for mouse position
        self._checkMousePositionForFocus()

    def _checkMousePositionForFocus(self):
        """Check the mouse position to know if move focus on a option"""
        i = 0
        for o in self.options:
            text = o[0]
            w,h = self.font.size(text)
            rect = pygame.Rect( (self.x, self.y + i*h), (w,h) )
            if rect.collidepoint(pygame.mouse.get_pos()):
                self.option = i
                self.mouse_focus = True
                break           
            i+=1
        else:
            self.mouse_focus = False

    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.x = x
        self.y = y
        
    def set_font(self, font):
        """Set the font used for the menu."""
        self.font = font
        self.height = len(self.options)*self.font.get_height()
        self._fixWidth()
        
    def set_highlight_color(self, color):
        """Set the highlight color"""
        self.hcolor = color
        
    def set_normal_color(self, color):
        """Set the normal color"""
        self.color = color
        
    def center_at(self, x, y):
        """Center the center of the menu at x,y"""
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)
