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
run this code simply downloading the source, going to the kezmenu directory and type:

   python tests.py

If you have the library installed on your system you can run the example program fron the python interpreter.

   import kezmenu
   kezmenu.runTests() 

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
   >>> def waitForUserAction(msg='???'):
   ...     global click_count
   ...     click_count+=1
   ...     pygame.display.set_caption("Example %s - %s" % (click_count, msg))
   ...     while True:
   ...         for event in pygame.event.get():
   ...             if event.type==KEYDOWN:
   ...                 return

Ok, lets call it for the first time.

   >>> waitForUserAction("An empty, dark surface")

We only displayed on the screen a surface filled with a dark color.

The KezMenu
-----------

Now it's time to create our KezMenu instance.

   >>> from kezmenu import KezMenu
   >>> menu = KezMenu()

To draw out menu we create before a second dummy function for test needs.

   >>> def drawMenu():
   ...     surface.fill( (50,50,50,255) )
   ...     menu.draw(surface)
   ...	   blitSurface()
   ...     pygame.display.flip()

Even this is a valid way to create our menu, we only obtain an empty menu.

   >>> drawMenu()
   >>> waitForUserAction("You see no difference")

You see no changes from the example 1, isn't it?
If we create our menu in this way we need to fill runtime it with our options.
You can do this by modifying runtime the 'options' attribute.

We need to know what the menu action must execute, before defining the option.

   >>> option_selected = None
   >>> def option1():
   ...     global option_selected
   ...     option_selected = 1
   >>> menu.options = ( {'label': 'First option!', 'callable': option1}, )

As you can see the options member must be a tuple of dictionary.
Those dict must contains (at least) the 'label' and 'callable' parameter; other paramter can
be specified for advanced use (see EFFECTS.txt).

The 'label' is the string to be draw for the menu option, and the 'callable' is the function, object,
method, ... to be call on selection.

   >>> drawMenu()
   >>> waitForUserAction("Our first option!")

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
   ...            ["Again!", option3],
   ...            ["Lambda", lambda: optionX(71)],
   ...            ["Quit", sys.exit],
   ...        )

You can fast create menu entries giving a list of couples that are our 'label' and 'callable' attributes.
The __init__ method does the magic and save those values in the right way.

   >>> type(menu.options[0]) == dict
   True
   >>> menu.options[1]['callable']
   <function option2 at ...>
   >>> [x['label'] for x in menu.options]
   ['First option!', 'sEcond', 'Again!', 'Lambda', 'Quit']

And now we refresh our window.

   >>> drawMenu()
   >>> waitForUserAction("All our options")

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

   >>> menu.position
   (0, 0)
   >>> menu.position = (30,50)
   >>> menu.position
   (30, 50)
   >>> drawMenu()
   >>> waitForUserAction("Not soo near to border now...")

Now the menu is in a better position on the screen.

Lets go over and modify some font properties. First talk of the menu dimension.
Data about the menu dimension is always available using the width and height attributes.

   >>> menu.width
   126
   >>> menu.height
   115

Those values are related to the labels displayed in the menu voices and also influenced by the
font used (and it's dimension).

   >>> new_font = pygame.font.Font(None, 38)
   >>> menu.font = new_font
   >>> drawMenu()
   >>> waitForUserAction("Bigger font")

This bigger font has different size, so the whole menu size raise.

   >>> menu.width
   154
   >>> menu.height
   135


   >>> menu.color = (255,255,255,100)
   >>> menu.focus_color = (255,255,0)
   >>> drawMenu()
   >>> waitForUserAction("...and better colors")
   
As you can see we can easily manipulate the font color, and the font of the selected item.

Do something useful with our KezMenu
------------------------------------

You surely noted that our previous examples are right now static photo without any action possible.
To make some real examples with our menu we need to use the KezMEnu.update method, and pass it
the `pygame.Event`__ instances that Pygame capture.
The waitForUserAction dummy function is no more needed because a menu is commonly a way itself to
wait for user decision.

__ http://www.pygame.org/docs/ref/event.html

   >>> click_count+=1
   >>> pygame.display.set_caption("Example %s - %s" % (click_count, "Use the KezMenu freely"))
   >>> while True:
   ...     events = pygame.event.get()
   ...     menu.update(events)
   ...     drawMenu()
   ...     pygame.display.flip()
   ...     if option_selected:
   ...         break
   >>> option_selected is not None
   True

The option_selected variable now contains the return value of the callable, relative to the option choosen.

NB: if you select the 'Quit' option running this test you will get a fake test failure.
This isn't a KezMenu bug, but it's normal in Python tests: the sys.exit call raise a
SystemExit exception that in tests are handled in a different way.

Ok, the example is at the end!

You can find examples about menu effects in the EFFECTS.txt file!

   >>> pygame.quit()

Credits
=======

 * PyMike from the Pygame community for his original work.

TODO
====

 * Submenus?
 * More effects

Subversion and other
====================

The SVN repository is hosted at the `Keul's Python Libraries`__

__ https://sourceforge.net/projects/kpython-utils/

