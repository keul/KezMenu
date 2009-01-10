=======
KezMEnu
=======

A simple and basical Pygame based module for a fast development of menu interfaces.

Introduction
============

This module is based on the original work of PyMike, from the PyGame community
(see the `EzMeNu project`__ for more info). As I found some issues using the Mike's version library,
I release this one that fix some issue.

__ http://www.pygame.org/project/855/

Examples and usage
==================

Here a fully example of use of this library. Even if I use the Python doctest format, this isn't a
politically correct test because I wait for user input and no real tests are done on the results.

Maybe someday I'll fix this!

However the code in this page is a working example. If you know nothing about doctests, only know that you can
run this code simple accessing at the egg source and type:

   python tests.py

Init all the Pygame stuff
-------------------------

First of all we need to enable the Pygame environment

   >>> import pygame
   >>> from pygame.locals import *
   >>> import pygame.font
   >>> pygame.font.init()
   >>> screen = pygame.display.set_mode((640,480), 0, 32)

KezMEnu works drawing the menu onto a `pygame.Surface`__ instance, so we will not draw the menu directly
on the 'screen' instance (but we could!).
So we create this surface first.

__ http://www.pygame.org/docs/ref/surface.html

   >>> surface = pygame.Surface( (400,400), flags=SRCALPHA, depth=32 )
   >>> surface.fill( (50,50,50,255) )
   <rect(0, 0, 400, 400)>

Now we can blit the surface on the screen. We will repeat this procedure several times so it's better create out first
dummy function (those functions aren't really useful outside this test environment):

   >>> def blitSurface():
   ...     screen.blit(surface, (50,50) )
   ...     pygame.display.update()

So we can call it for the first time.

   >>> blitSurface()

This is a graphical test, so we need to delay the automatic actions and make possible that the user can look at results
and then go over. We wait for user input before going on.

To do this we create a second silly function that we'll call often later.

   >>> click_count = 0
   >>> def waitForUserAction():
   ...     global click_count
   ...     click_count+=1
   ...     pygame.display.set_caption("Example %s" % click_count)
   ...     while True:
   ...         for event in pygame.event.get():
   ...             if event.type == QUIT:
   ...                 import sys
   ...                 sys.exit(0)
   ...             if event.type==KEYDOWN:
   ...                 return

Ok, lets call it for the first time.

   >>> waitForUserAction()

We only displayed on the screen a surface filled with a dark color.

The KezMenu
-----------

Now it's time to create our KezMenu instance.

   >>> from kezmenu import KezMenu
   >>> menu = KezMenu()

To draw out menu we create before a second dummy function for test needs.

   >>> def drawMenu():
   ...     menu.draw(surface)
   ...	   blitSurface()
   ...     pygame.display.flip()

Even this is a valid way to create our menu, we only obtain an empty menu.

   >>> drawMenu()
   >>> waitForUserAction()

You see no changes from the example 1, isn't it?
If we create our menu in this way we need to fill runtime it with our options.
You can do this by modifying runtime the 'options' attribute.

We need to know what the menu action must execute, before defining the option.

   >>> option_selected = None
   >>> def option1():
   ...     global option_selected
   ...     option_selected = 1
   >>> menu.options = ( ["First option!", option1], )

As you can see the options attribute must be a tuple of couples. Those couples will be composed
by the label to use and a callable object to be executed when the menu item is selected.

   >>> drawMenu()
   >>> waitForUserAction()

Ways to link action to menu selection
-------------------------------------

The other (most common) way is to create the options directly on menu creation.
To do make the test more complete, we need to add some other callable!

   >>> def option2():
   ...     global option_selected
   ...     option_selected = 1
   >>> def option3():
   ...     global option_selected
   ...     option_selected = 1

   >>> import sys
   >>> def optionX(p):
   ...     global option_selected
   ...     option_selected = p

Now create a new menu instance.

   >>> menu = KezMenu(
   ...            ["First option!", option1],
   ...            ["sEcond", option2],
   ...            ["Again!", option2],
   ...            ["Lambda", lambda: optionX(71)],
   ...            ["Quit", sys.exit],
   ...        )

And now we refresh our window.

   >>> drawMenu()
   >>> waitForUserAction()

Its very important to see how the actions are linked to the menu items. We must create couples of labels and
callable objects without calling it! Like abowe you must pass to the MezMenu a function, you must not call the function
itself.

You can also use as callable argument a method of an object, a Python standard callable (like the `sys.exit`__ above)

What if you wanna also need to pass parameter(s) to the callable? The use of the `lambda function`__ above will show you how
to do this!

__ http://docs.python.org/library/sys.html#sys.exit
__ http://docs.python.org/reference/expressions.html#id17

Customize the menu GUI: colors, font, ...
-----------------------------------------

The menu showed in the last example is a little ugly. Too near the the surface border
and color used for non selected elements are ugly.
You can modify those properties also for an already created menu.

   >>> menu.set_position(30,50)
   >>> drawMenu()
   >>> waitForUserAction()







Credits
=======

 * PyMike from the Pygame community for his original work.

TODO
====

 * Submenus?

Subversion and other
====================

The SVN repository is hosted at the `Keul's Python Libraries`__

__ https://sourceforge.net/projects/kpython-utils/

