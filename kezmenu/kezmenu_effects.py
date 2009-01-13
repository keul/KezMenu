# -*- coding: utf-8 -*-

VALID_EFFECTS = ('enlarge-font-on-focus','raise-line-padding-on-focus')

class KezMenuEffectAble(object):
    """Base class used from KezMenu, to group all data and method needed for effects support"""
    
    def __init__(self):
        self._effects = {}

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
        for name,params in self._effects.items():
            self.__getattribute__('_effectupdate_%s' % name.replace("-","_"))(time_passed)

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
        kwargs['padding_pps'] = kwargs['padding']/kwargs['enlarge_time'] # pixel-per-second
        # Now, every menu voices need additional infos
        for o in self.options:
            o['padding_line']=0.
            o['padding_time_passed']=0.

    def _effectupdate_raise_line_padding_on_focus(self, time_passed):
        """Gradually enlarge the padding of the focused line.
        If the focus move from a voice to another, also reduce padding of all other not focused entries.
        """
        data = self._effects['raise-line-padding-on-focus']
        pps = data['padding_pps']
        i = 0
        for o in self.options:
            if i==self.option:
                # Raise me
                if o['padding_line']<data['padding']:
                    o['padding_line']+=pps*time_passed
                elif o['padding_line']>data['padding']:
                    o['padding_line'] = data['padding']
            elif o['padding_line']:
                if o['padding_line']>0:
                    o['padding_line']-=pps*time_passed
                elif o['padding_line']<0:
                    o['padding_line'] = 0
            i+=1

