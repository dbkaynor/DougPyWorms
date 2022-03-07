# import math
import os
import platform
# import random
import sys
# import tkinter
# from tkinter import messagebox
# from tkinter.colorchooser import askcolor

import pygame
from screeninfo import get_monitors

# from ToolTip import ToolTip

if platform.system() == "Windows":
    os.environ["SDL_VIDEODRIVER"] = "windib"
import pprint

debugMode = True
pp = pprint.PrettyPrinter(indent=4)
colorList = []
currentBackgroundColor = "black"
monitorWidth = 0
monitorHeight = 0

if platform.system() == "Windows":
    screenPosVertical = -900
    screenPosHorizontal = 250
elif platform.system() == "Linux":
    screenPosVertical = 0
    screenPosHorizontal = 250
else:
    print("Unknown platform " + platform.system())
    exit()

monitorInfo = get_monitors()
if debugMode:
    print("setUp")
    for monitorInfo in get_monitors():
        print(str(monitorInfo))



foregroundColor = "white"
root = 0

pygame.init()
pygame.display.init()
# https://www.pygame.org/docs/ref/event.html
for event in pygame.event.get():
    if event.type == pygame.WINDOWRESIZED:
        print('resize')

gettrace = getattr(sys, "gettrace", None)
print(gettrace)
if gettrace is None:
    print("No sys.gettrace")
    debugMode = True
elif gettrace:
    print("Hmm, Big Debugger is watching me")
    debugMode = True
else:
    print("No debugger detected")
    debugMode = False
    if debugMode:
        print(" __name__", __name__)


class worms:

    def main():

        directions = {
            'n': '',
            'ne': '',
            'e': '',
            'se': ''
        }

        global monitorWidth
        global monitorHeight
        global root
        global screenPosVertical
        global screenPosHorizontal
        global foregroundColor
        global debugMode

        debugFile = "DougPyWorms.txt"
        if os.path.exists(debugFile):
            os.remove(debugFile)

        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i, %i" % (
            screenPosHorizontal,
            screenPosVertical
        )

        infoObject = pygame.display.Info()
        pygame.display.set_mode((infoObject.current_w, infoObject.current_h))

        #  screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Show some worms", "WORMS")
        pygame.event.pump()
        # event = pygame.event.wait()
        # print('event: ', str(event))

        clock = pygame.time.Clock()

        # Creating a new rect for first object
        player_rect = pygame.Rect(200, 500, 50, 10)
        # Creating a new rect for second object
        player_rect2 = pygame.Rect(200, 0, 10, 10)

        # Creating variable for gravity
        gravity = 4

        # Creating a boolean variable that
        # we will use to run the while loop
        run = True

        # Creating an infinite loop
        # to run our game
        while run:

            # Setting the framerate to 60fps
            clock.tick(60)

            # Adding gravity in player_rect2
            player_rect2.bottom += gravity

            # Checking if player is colliding
            # with platform or not using the
            # colliderect() method.
            # It will return a boolean value
            collide = pygame.Rect.colliderect(player_rect, player_rect2)

            # If the objects are colliding
            # then changing the y coordinate
            if collide:
                player_rect2.bottom = player_rect.top

            # Drawing player rect
            pygame.draw.rect(root, (0, 255, 0),
                             player_rect)
            # Drawing player rect2
            pygame.draw.rect(root, (0, 0, 255),
                             player_rect2)

            # Updating the display surface
            pygame.display.update()


if __name__ == "__main__":
    worms.main()
