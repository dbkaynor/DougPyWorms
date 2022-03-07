# DougPyWorms.py
#
# Produces interesting patterns
#
# This  program  is free software: you can redistribute it and/or  modify it
# under the terms of the GNU General Public License as published by the Free
# Software  Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This  program  is  distributed  in the hope that it will  be  useful,  but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or  FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public  License
# for more details.
#
# You  should  have received a copy of the GNU General Public License  along
# with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# import math
import os
import platform
import random
import sys
import tkinter
# from tkinter import messagebox
# Surface.get_at((x, y))[:3]
from tkinter.colorchooser import askcolor

import pygame
from pygame.locals import Rect
from screeninfo import get_monitors

from ToolTip import ToolTip

if platform.system() == "Windows":
    os.environ["SDL_VIDEODRIVER"] = "windib"
import pprint

debugMode = True
pp = pprint.PrettyPrinter(indent=4)
colorList = []
currentBackgroundColor = "black"

# This positioning is for testing purposes
if platform.system() == "Windows":
    screenPosVertical = -900
    screenPosHorizontal = 250
elif platform.system() == "Linux":
    screenPosVertical = 0
    screenPosHorizontal = 250
elif platform.system() == "OS X":
    screenPosVertical = 0
    screenPosHorizontal = 0
else:
    print("Unknown platform: " + platform.system())
    exit()

foregroundColor = "white"
currentForegroundColor = foregroundColor
tkRoot = 0

pygame.init()
pygame.display.init()
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

clock = pygame.time.Clock()


class worms:
    tkRoot = tkinter.Tk()
    clearBeforeDrawCheckButtonVar = tkinter.BooleanVar()
    foregroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    backgroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    blockSizeVar = tkinter.IntVar()
    speedVar = tkinter.IntVar()
    menuWidth = 220
    menuHeight = 600

    def main():
        global tkRoot
        global screenPosVertical
        global screenPosHorizontal
        global foregroundColor
        global debugMode

        pygame.event.pump()
        # event = pygame.event.wait()
        # print('event: ', str(event))

        geometry = "".join(
            [
                str(worms.menuWidth),
                "x",
                str(worms.menuHeight),
                "+",
                str(screenPosHorizontal - worms.menuWidth - 10),
                "+",
                str(screenPosVertical - 80),
            ]
        )

        worms.tkRoot.geometry(geometry)
        worms.tkRoot.resizable(height=False, width=False)
        worms.tkRoot.title("Draw some worms")
        main_dialog = tkinter.Frame(tkRoot)
        main_dialog.pack(side=tkinter.TOP, fill=tkinter.X)
        print("dirname:    ", os.path.dirname(__file__))
        photo = tkinter.PhotoImage(
            file="".join([os.path.dirname(__file__), os.sep, "KickUnderBus.png"])
        )
        worms.tkRoot.iconphoto(True, photo)

        worms.setUp()
        # #######################################
        drawWormsButton = tkinter.Button(
            tkRoot,
            text="Draw",
            fg="blue",
            bg="white",
            width=20,
            command=worms.drawWorms
        )
        drawWormsButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(drawWormsButton, text="Draw worms")
        # #######################################
        clearScreenButton = tkinter.Button(
            tkRoot,
            text="Clear",
            fg="blue",
            bg="white",
            width=20,
            command=worms.clearDisplay
        )
        clearScreenButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(drawWormsButton, text="Clear display")
        # #######################################
        selectScreenFillButton = tkinter.Button(
            tkRoot,
            text="Select background color",
            fg="blue",
            bg="white",
            width=20,
            command=worms.selectBackgroundColor
        )
        selectScreenFillButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(selectScreenFillButton, text="Select background color")
        # #######################################
        randomScreenFillButton = tkinter.Button(
            tkRoot,
            text="Random background color",
            fg="blue",
            bg="white",
            width=20,
            command=worms.randomBackgroundColor
        )
        randomScreenFillButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(randomScreenFillButton, text="Random background color")
        # #######################################
        selectforegroundColorButton = tkinter.Button(
            tkRoot,
            text="Select foreground color",
            fg="blue",
            bg="white",
            width=20,
            command=worms.selectforegroundColor
        )
        selectforegroundColorButton.pack(
            side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X
        )
        ToolTip(selectforegroundColorButton, text="Select foreground color")
        # #######################################
        checkButtonFrame = tkinter.Frame(
            tkRoot,
            bg="white",
            width=20,
            highlightbackground="black",
            relief=tkinter.RAISED
        )
        checkButtonFrame.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        clearBeforeDrawCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Clear before draw",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Clear before draw"),
            variable=worms.clearBeforeDrawCheckButtonVar
        )
        clearBeforeDrawCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)
        worms.clearBeforeDrawCheckButtonVar.set(True)
        # #######################################
        foregroundColorRandomCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Random foreground color",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Random foreground color"),
            variable=worms.foregroundColorRandomCheckButtonVar
        )
        foregroundColorRandomCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(foregroundColorRandomCheckButton, text="Random foreground color")
        worms.foregroundColorRandomCheckButtonVar.set(True)
        # #######################################
        backgroundColorRandomCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Random background color",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: print("Random background color"),
            variable=worms.backgroundColorRandomCheckButtonVar
        )
        backgroundColorRandomCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)

        ToolTip(backgroundColorRandomCheckButton, text="Random background color")
        worms.backgroundColorRandomCheckButtonVar.set(False)
        # #######################################
        speedSelect = tkinter.Scale(
            tkRoot,
            fg="blue",
            bg="white",
            label="Speed",
            length=150,
            from_=1,
            to=20,
            variable=worms.speedVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED
        )
        speedSelect.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(speedSelect, "Select speed.")
        worms.speedVar.set(5)
        # #######################################
        blockSize = tkinter.Scale(
            tkRoot,
            fg="blue",
            bg="white",
            label="Block size",
            length=150,
            from_=1,
            to=20,
            variable=worms.blockSizeVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED
        )
        blockSize.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)

        ToolTip(blockSize, "Block size.")
        worms.blockSizeVar.set(10)
        # #######################################
        quitButton = tkinter.Button(
            tkRoot,
            text="Quit",
            fg="blue",
            bg="white",
            width=20,
            command=worms.quitProgram
        )
        quitButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(quitButton, text="Quit the program")
        # #######################################

        tkinter.mainloop()

    def quitProgram():
        if debugMode:
            print("Quit using window X")
        pygame.display.quit
        pygame.quit()
        sys.exit(0)

    # #######################################

    def setUp():
        global debugMode
        global colorList
        global screen

        global menuHeight
        global tkRoot

        debugFile = "DougPyWorms.txt"
        if os.path.exists(debugFile):
            os.remove(debugFile)

        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i, %i" % (
            screenPosHorizontal,
            screenPosVertical
        )
        screenWidth = 800
        screenHeight = worms.menuHeight  # 550

        screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
        pygame.display.set_caption("Draw some worms", "worms")
        pygame.event.pump()

        monitorInfo = get_monitors()
        if debugMode:
            print("setUp")
            for monitorInfo in get_monitors():
                print(str(monitorInfo))

        pp.pprint(screen.get_size())
        pp.pprint(pygame.display.Info())
        pp.pprint(str(event))

        img = pygame.image.load(
            "".join([os.path.dirname(__file__), os.sep, "KickUnderBus.png"])
        )

        pygame.display.set_icon(img)

        # Generate list of colors
        colorKeys = pygame.color.THECOLORS.keys()
        colorList = list(colorKeys)
        if debugMode:
            print("Number of colors: ", len(colorList))

    # #######################################
    def drawWorms():
        run = True
        # (left, top), (width, height)
        player_rect1 = Rect((150, 20), (worms.blockSizeVar.get(), worms.blockSizeVar.get()))
        player_rect2 = Rect((150, 350), (worms.blockSizeVar.get(), worms.blockSizeVar.get()))

        # pygame.display.update()
        pygame.display.flip()

        if worms.clearBeforeDrawCheckButtonVar.get():
            worms.clearDisplay()

        if worms.backgroundColorRandomCheckButtonVar.get():
            worms.randomBackgroundColor()

        if worms.foregroundColorRandomCheckButtonVar.get():
            color = random.randrange(0, len(colorList))
            worms.currentForegroundColor = colorList[color]
            if debugMode:
                print('randomForegroundColor: ', color, worms.currentForegroundColor)

        screenWidth, screenHeight = screen.get_size()
        print('*' * 30)
        print('nn', screenWidth, screenHeight)
        print('oo', player_rect1.bottom, player_rect1.top, player_rect1.left, player_rect1.right)
        print('pp', player_rect2.bottom, player_rect2.top, player_rect2.left, player_rect2.right)

        print(screenHeight, player_rect1.bottom)
        print('01', player_rect1.top)
        print(screenWidth, player_rect1.left)
        print('02', player_rect1.right)

        # loop until collision
        while run:
            print('clock.tick: ', str(clock.tick(60)))
            player_rect1.bottom += worms.speedVar.get()

            collide = pygame.Rect.colliderect(player_rect1, player_rect2)
            # if screenWidth
            # if screenHeight
            print('>>', player_rect2.bottom, player_rect1.top)
            if collide:
                run = False

            pygame.draw.rect(screen, worms.currentForegroundColor,
                             player_rect1)
            pygame.draw.rect(screen, 'green',
                             player_rect2)
            pygame.display.update()

    def clearDisplay():
        global debugMode
        global colorList
        global currentBackgroundColor
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print("clearDisplay: ", currentBackgroundColor)

    def writeDebugFile(pointsList):
        global debugMode
        if debugMode:
            print("writeDebugFile")
            fileDebug = open("DougPyWorms.txt", "a")
            for a in pointsList:
                my = " ".join([str(a[0]), "\t", str(a[1])])
                fileDebug.write(my + "\n")
            fileDebug.write("=" * 50 + "\n")
            fileDebug.close()

    def selectforegroundColor():
        global debugMode
        global foregroundColor
        global currentForegroundColor
        colors = askcolor(title="Foreground color chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        currentForegroundColor = colors[1]
        pygame.display.flip()
        if debugMode:
            print("selectforegroundColor")

    def randomForegroundColor():
        global debugMode
        global colorList
        global currentForegroundColor
        color = random.randrange(0, len(colorList))
        currentForegroundColor = colorList[color]
        if debugMode:
            print("randomForegroundColor: ", color, currentForegroundColor)

    def selectBackgroundColor():
        global debugMode
        global currentBackgroundColor
        colors = askcolor(title="Background color chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        currentBackgroundColor = colors[1]
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print("selectBackgroundColor")

    def randomBackgroundColor():
        global debugMode
        global colorList
        global currentBackgroundColor
        color = random.randrange(0, len(colorList))
        currentBackgroundColor = colorList[color]
        screen.fill(currentBackgroundColor)
        pygame.display.flip()
        if debugMode:
            print("randomBackgroundColor: ", color, currentBackgroundColor)


# This is where we loop until user wants to exit
if __name__ == "__main__":
    worms.main()
