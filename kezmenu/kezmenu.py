# -*- coding: utf-8 -*-

# KezMenu - By Luca Fabbri
# This code is released under GPL license
# ---------------------------------------------------------------
# This work is based on the original EzMeNu script, released from
# PyMike, from the Pygame community
# See http://www.pygame.org/project/855/
# ---------------------------------------------------------------

import pygame
import warnings

__author__ = "Keul - lucafbb AT gmail.com"
__version__ = "0.3.0"

__description__ = "A simple and basical Pygame library for fast develop of menu interfaces"

VALID_EFFECTS = ('enlarge-font-on-focus','raise-line-padding-on-focus')

class deprecated(object):
    """A decorator for deprecated functions"""
    
    def __init__(self, msg):
        self._msg = msg
        self._printed = False
    
    def __call__(self, func):
        """Log out the deprecation message, but only once"""
        if not self._printed:
            def wrapped_func(*args):
                warnings.warn(self._msg % func.__name__, DeprecationWarning, stacklevel=3)
                func(*args)
            self._printed = True
            return wrapped_func
        return func

class KezMenu(object):
    """A simple but complete class to handle menu using Pygame"""

    def __init__(self, *options):
        """Initialise the EzMenu! options should be a sequence of lists in the
        format of [option_name, option_function]"""

        self.options = [{'label': x[0], 'callable': x[1]} for x in options]
        self.x = 0
        self.y = 0
        self.option = 0
        self.width = 0
        self.height = 0
        self.color = (0, 0, 0, 0)
        self.focus_color = (255, 0, 0, 255)
        self.mouse_focus = False
        self._effects = {}
        # The 2 lines below seem stupid, but for effects I can need different font for every line.
        self._font = None
        self.font = pygame.font.Font(None, 32)
        self._fixSize()

    def enableEffect(self, name, **kwargs):
        """Enable an effect in the KezMEnu
        Raise a KeyError if the name of the effect is not know.
        Additional keyword argument will be passed to the propert effect's init method, and stored.
        @name: the name of the effect as string (must be one of the kezmenu.VALID_EFFECTS values)
        """
        if name not in VALID_EFFECTS:
            raise KeyError("KezMenu don't know an effect of type %s" % name)
        self._effects[name] = kwargs
        self.__getattribute__('_effectinit_%s' % name.replace("-","_"))(kwargs)

    def disableEffect(self, name):
        """Disable an effect"""
        try:
            del self._effects[name]
        except KeyError:
            pass

    def _updateEffects(self, time_passed):
        """Update method for the effects handle"""
        for name,params in self._effects.items:
            self.__getattribute__('_effectupdate_%s' % name.replace("-","_"))(time_passed)

    def _fixSize(self):
        """Fix the menu size. Commonly called when the font is changed"""
        self.height = 0
        for o in self.options:
            text = o['label']
            font = o['font']
            ren = font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            self.height+=font.get_height()

    def draw(self, surface):
        """Draw the menu to the surface."""
        offset = 0
        i = 0
        for o in self.options:
            font = o.get('font',self._font)
            if i==self.option and self.focus_color:
                clr = self.focus_color
            else:
                clr = self.color
            text = o['label']
            ren = font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            surface.blit(ren, (self.x, self.y + offset))
            offset+=font.get_height()
            i+=1

    def update(self, events, time_passed=None):
        """Update the menu and get input for the menu.
        @events: the pygame catched events
        @time_passed: optional parameter, only used for animations. The time passed (in seconds) from the last
                      update call (commonly went from pygame.Clock.tick method)
        """
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.options[self.option]['callable']()
            # Mouse controls
            elif e.type == pygame.MOUSEBUTTONDOWN:
                lb, cb, rb = pygame.mouse.get_pressed()
                if lb and self.mouse_focus:
                    self.options[self.option]['callable']()
        # Menu limits
        if self.option > len(self.options)-1:
            self.option = len(self.options)-1
        elif self.option < 0:
            self.option = 0
        # Check for mouse position
        self._checkMousePositionForFocus()
        if time_passed is not None:
            self._updateEffects(time_passed)

    def _checkMousePositionForFocus(self):
        """Check the mouse position to know if move focus on a option"""
        i = 0
        mouse_pos = pygame.mouse.get_pos()
        ml,mt = self.position
        for o in self.options:
            text = o['label']
            font = o['font']
            w,h = font.size(text)
            rect = pygame.Rect( (self.x+ml, self.y + mt + i*h), (w,h) )
            if rect.collidepoint(mouse_pos):
                self.option = i
                self.mouse_focus = True
                break           
            i+=1
        else:
            self.mouse_focus = False


    @deprecated(("The %s function is deprecated and will be removed in future versions. "
                 "Please use the position property instead to specify (x,y)"))
    def set_pos(self, x, y):
        """Set the topleft of the menu at x,y"""
        self.position = (x,y)

    def _setPosition(self, position):
        x,y = position
        self.x = x
        self.y = y
    position = property(lambda self: (self.x,self.y), _setPosition, doc="""The menu position inside the container""")

    @deprecated(("The %s function is deprecated and will be removed in future versions. "
                 "Please use the font property instead."))
    def set_font(self, font):
        """Set the font used for the menu."""
        self.font = font

    def _setFont(self, font):
        self._font = font
        for o in self.options:
            o['font'] = font
        self._fixSize()
    font = property(lambda self: self._font, _setFont, doc="""Font used by the menu""")

    @deprecated(("The %s function is deprecated and will be removed in future versions. "
                 "Please use the focus_color attribute directly instead."))
    def set_highlight_color(self, color):
        """Set the highlight color"""
        self.focus_color = color

    @deprecated(("The %s function is deprecated and will be removed in future versions. "
                 "Please use the color attribute directly instead."))
    def set_normal_color(self, color):
        """Set the normal color"""
        self.color = color

    def center_at(self, x, y):
        """Center the menu at x,y"""
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)


    # ******* Effects *******

    def _effectinit_enlarge_font_on_focus(self, **kwargs):
        """Init the effect that enlarge the focused menu entry.
        Keyword arguments can contain enlarge_time (seconds needed to raise the element size)
        and enlarge_factor (a value that repr the size multiplier to be reached).
        """
        if not kwargs.has_key('enlarge_time'):
            kwargs['enlarge_time'] = 2.
        if not kwargs.has_key('enlarge_factor'):
            kwargs['enlarge_factor'] = 2.
        kwargs['time_passed'] = 0

    def _effectupdate_enlarge_font_on_focus(self, time_passed):
        """Gradually enlarge the font size of the focused line"""
        raise NotImplementetError("Not yet available")


    def _effectinit_raise_line_padding_on_focus(self, **kwargs):
        """Init the effect that raise the empty space above and below the focused entry.
        Keyword arguments can contain enlarge_time (seconds needed to raise the element size)
        and padding (a value that repr the number of pixel to be added above and below the focused line).
        """        
        if not kwargs.has_key('enlarge_time'):
            kwargs['enlarge_time'] = 2.
        if not kwargs.has_key('padding'):
            kwargs['padding'] = 10
        # Now, every menu voices need additional infos
        for o in self.options:
            o['padding_line']=0
            o['padding_time_passed']=0

    def _effectupdate_raise_line_padding_on_focus(self, time_passed):
        """Gradually enlarge the padding of the focused line.
        If the focus move from a voice to another, also reduce padding of all other not focused entries.
        """
        data = self._effects['raise-line-padding-on-focus']
        pps = data['padding']/data['enlarge_time'] # pixel-per-second
        i = 0
        for o in self.options:
            if i==self.option:
                # Raise me
                if o['padding_line']<data['padding']:
                    pass
            elif o['padding_line']:
                # Reduce me
                pass
            i+=1


def runTests():
    import tests
