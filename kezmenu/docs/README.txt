=======
KezMenu
=======

A simple and basical Pygame based module for a fast development of menu interfaces.

Introduction
============

This module is based on the original work of *PyMike*, from the Pygame community
(see the `EzMeNu project`__ for more info). As I found some issues using the Mike's version library,
I release this one that fix some of theme, and also add features.

__ http://www.pygame.org/project/855/

`What you can do with this?`
	You can easilly draw a menu interface, and selecting an option using the mouse of arrow keys.

Examples and usage
==================

Here a fully example of use of this library. Even if we use the Python doctest format, this isn't a
politically correct automated test because we'll wait for user input and no real tests are done onto results
(no... this is not true, but none of the major feature are really tested here).

Maybe someday I'll complete this with better python tests!

However...
The code in this page is a working example. If you know nothing about doctests, only know that you can
run this code simply downloading the source, going to the kezmenu directory and type:

   python tests.py

If you have the library installed on your system you can run the example program from the python interpreter:

   import kezmenu

   kezmenu.runTests() 

Init all the Pygame stuff
-------------------------

First of all we need to enable the Pygame environment:

   >>> import pygame
   >>> from pygame.locals import *
   >>> import pygame.font
   >>> pygame.font.init()
   >>> screen = pygame.display.set_mode((640,480), 0, 32)

KezMenu works drawing the menu onto a `pygame.Surface`__ instance; the better (simpler) choice is always draw the menu
onto the screen (another Surface instance obtained using methods of the `pygame.display`__ Pygame's module, like
`pygame.display.set_mode`__),
because is not possible in Pygame to know the offset of a blitten surface from the screen topleft corner.

__ http://www.pygame.org/docs/ref/surface.html
__ http://www.pygame.org/docs/ref/display.html
__ http://www.pygame.org/docs/ref/display.html#pygame.display.set_mode

This is not important if you are not planning to use the mouse on the menu and rely only up and down keys.
To disable the mouse, just put to False the *mouse_enabled* attribute of a KezMEnu instance.

In the first example below we will use a surface inside the screen for drawing the menu.
So we create this surface first:

   >>> surface = pygame.Surface( (400,400), flags=SRCALPHA, depth=32 )
   >>> surface.fill( (150,150,150,255) )
   <rect(0, 0, 400, 400)>

Now we can blit the surface on the screen. We will repeat this procedure some times so it's better create out first
dummy function (those functions aren't really useful outside this test environment):

   >>> def blitSurface():
   ...     screen.blit(surface, (50,50) )
   ...     pygame.display.update()

So we can call it for the first time:

   >>> blitSurface()

This is a graphical test, so we need to delay the automatic actions and make possible that the user can look at results
and then go over. We wait for user input before going over.

To do this we create a second silly function that we'll call often later:

   >>> click_count = 0
   >>> def waitForUserAction(msg='???'):
   ...     global click_count
   ...     click_count+=1
   ...     pygame.display.set_caption("Example %s - %s" % (click_count, msg))
   ...     while True:
   ...         for event in pygame.event.get():
   ...             if event.type==KEYDOWN:
   ...                 return

Ok, lets call it for the first time:

   >>> waitForUserAction("An empty, dark surface")

We only displayed on the screen a surface filled with a dark color.

The KezMenu
-----------

Now it's time to create our KezMenu instance:

   >>> from kezmenu import KezMenu
   >>> menu = KezMenu()

To draw out menu we create before another second dummy function for test needs:

   >>> def drawMenu():
   ...     surface.fill( (150,150,150,255) )
   ...     menu.draw(surface)
   ...	   blitSurface()
   ...     pygame.display.flip()

This is a valid way to create our menu, but we only obtain an empty menu (so invisible to user).

   >>> drawMenu()
   >>> waitForUserAction("You see no difference")

You see no changes from the example 1, isn't it?
If we create our menu in this way we need to fill it runtime with our options.
You can do this by modifying runtime the *options* attribute.

We need to know what the menu action must execute, before defining the option:

   >>> option_selected = None
   >>> def option1():
   ...     global option_selected
   ...     option_selected = 1
   >>> menu.options = ( {'label': 'First option!', 'callable': option1}, )

As you can see the options member must be a tuple of dictionary.
Those dict must contains (at least) the *label* and *callable* parameters; other paramter can
be specified for advanced use (see *EFFECTS.txt*).

The *label* is the string to be draw for the menu option, and the *callable* is the function, object,
method, ... to be called on selection.

As far as we blitted the menu inside a surface that isn't in the (0,0) screen position, we need (if we wanna use also mouse
control later) to specify the *screen_topleft_offset* attribute:

   >>> menu.screen_topleft_offset = (50,50)
   >>> drawMenu()
   >>> waitForUserAction("Our first option!")

In this way we say to the menu that all coordinates must keep count of an offset from the topleft corner of the screen.

Pass a screen object directly to the *menu.draw* method is more common, so in all other examples we will drop the use
of the surface object.

   >>> surface = None

Ways to link action to menu selection
-------------------------------------

Manually change the *options* attribute is simple (and can be useful) but the most common way is to create the options
directly on menu creation.
To do make tests more complete, we need to add some other callable!

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

Now create a new menu instance:

   >>> menu = KezMenu(
   ...            ["First option!", option1],
   ...            ["sEcond", option2],
   ...            ["Again!", option3],
   ...            ["Lambda", lambda: optionX(71)],
   ...            ["Quit", sys.exit],
   ...        )

You can fast create menu entries giving a list of couples that are our *label* and *callable* attributes.
The *__init__* method does the magic and save those values in the right way.

   >>> type(menu.options[0]) == dict
   True
   >>> menu.options[1]['callable']
   <function option2 at ...>
   >>> [x['label'] for x in menu.options]
   ['First option!', 'sEcond', 'Again!', 'Lambda', 'Quit']

Like said above we will not use anymore the surface object, so we can simplify a little our dummy function:

   >>> def drawMenu():
   ...     screen.fill( (150,150,150,255) )
   ...     menu.draw(screen)
   ...     pygame.display.flip()

And now we refresh our window:

   >>> drawMenu()
   >>> waitForUserAction("All our options")

It's very important to see how the actions are linked to the menu items. We must create couples of labels and
*callable objects* without calling them! Like above you must pass the callable to the KezMenu a function,
you must not call the callable yourself.

We can also use as callable argument a method of an object, a Python standard callable (like the `sys.exit`__ above)

What if you wanna also need to pass parameter(s) to the callable? The use of the `lambda function`__ above will show you how
to do this!

__ http://docs.python.org/library/sys.html#sys.exit
__ http://docs.python.org/reference/expressions.html#id17

Customize the menu GUI: colors, font, ...
-----------------------------------------

The menu showed in the last example is a little ugly. Too near the the screen border and color used for non selected
elements are ugly.
You can modify those properties also for an already created menu:

   >>> menu.position
   (0, 0)
   >>> menu.position = (30,50)
   >>> menu.position
   (30, 50)
   >>> drawMenu()
   >>> waitForUserAction("Not soo near to border now...")

Now the menu is in a better position on the screen.

Lets go over and modify some font properties, but first let me talk about the menu dimension.
Data about the menu dimension is always available using the *width* and *height* attributes:

   >>> menu.width
   126
   >>> menu.height
   115

Those values are related to the labels displayed in the menu voices and also influenced by the
font used (and it's dimension):

   >>> new_font = pygame.font.Font(None, 38)
   >>> menu.font = new_font
   >>> drawMenu()
   >>> waitForUserAction("Bigger font")

This bigger font has different size, so the whole menu size raise:

   >>> menu.width
   154
   >>> menu.height
   135

Now colors:

   >>> menu.color = (255,255,255,100)
   >>> menu.focus_color = (255,255,0)
   >>> drawMenu()
   >>> waitForUserAction("...and better colors")
   
As you can see we can easily manipulate the font color, and the font of the selected item.

Do something useful with our KezMenu
------------------------------------

You noticed that our previous examples are rightnow static screenshots without any possible interaction.

To make some real examples with our menu we need to use the *KezMEnu.update* method, and pass it
the `pygame.Event`__ instances that Pygame had captured.
The *waitForUserAction* dummy function is no more needed because a menu is commonly a way to wait for user
decision itself.

__ http://www.pygame.org/docs/ref/event.html

   >>> click_count+=1
   >>> pygame.display.set_caption("Example %s - %s" % (click_count, "Use the KezMenu freely"))
   >>> while True:
   ...     events = pygame.event.get()
   ...     menu.update(events)
   ...     drawMenu()
   ...     if option_selected:
   ...         break
   >>> option_selected is not None
   True

The *option_selected* variable now contains the return value of the callable, relative to the option choosen.

NB: if you select the *Quit* option running this test you will get a fake test failure.
This isn't a KezMenu bug, but it's normal in Python tests: the *sys.exit* call raise a
*SystemExit* exception that in tests are handled in a different way.

Ok, the example is at the end!

But KezMenu has also some effects!
You can find examples about menu effects in the *EFFECTS.txt* file!

Goodbye!

   >>> pygame.quit()



