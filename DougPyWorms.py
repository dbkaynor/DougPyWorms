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
import time
import tkinter
# from tkinter import messagebox
# Surface.get_at((x, y))[:3]
from tkinter.colorchooser import askcolor
import pygame
from pygame.locals import Rect
from screeninfo import get_monitors
import inspect

from ToolTip import ToolTip
import pprint

# Clear the terminal at progarm startup
os.system('cls||clear')

pp = pprint.PrettyPrinter(indent=4)

if platform.system() == "Windows":
    os.environ["SDL_VIDEODRIVER"] = "windib"

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

pygame.init()
pygame.display.init()
for event in pygame.event.get():
    if event.type == pygame.WINDOWRESIZED:
        print('resize')

debugMode = True
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


# https://www.pygame.org/docs/ref/event.html
for event in pygame.event.get():
    if event.type == pygame.WINDOWRESIZED:
        print('resize')


class worms:
    tkRoot = tkinter.Tk()
    infoLabelVar = tkinter.StringVar()
    clearBeforeDrawCheckButtonVar = tkinter.BooleanVar()
    foregroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    backgroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    blockSizeVar = tkinter.IntVar()
    speedVar = tkinter.IntVar()
    menuWidth = 220
    menuHeight = 500
    screenWidth = 800
    screenHeight = 500
    colorList = []
    foregroundColor = 'white'
    backgroundColor = "black"
    rectangle_list = []
    playerNew = []
    playerOld = []

    def main():
        global screenPosVertical
        global screenPosHorizontal
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
                str(screenPosVertical - 50),
            ]
        )

        worms.tkRoot.geometry(geometry)
        worms.tkRoot.resizable(height=False, width=False)
        worms.tkRoot.title("Draw some worms")
        main_dialog = tkinter.Frame(worms.tkRoot)
        main_dialog.pack(side=tkinter.TOP, fill=tkinter.X)
        print("dirname:    ", os.path.dirname(__file__))
        photo = tkinter.PhotoImage(
            file="".join([os.path.dirname(__file__), os.sep, "worm2.png"])
        )
        worms.tkRoot.iconphoto(True, photo)
        # worms.clearDisplay()
        worms.setUp()
        # #######################################
        infoLabel = tkinter.Label(
            worms.tkRoot,
            textvariable=worms.infoLabelVar,
            text="Clear",
            fg="blue",
            bg="white",
            width=20)
        infoLabel.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        worms.infoLabelVar.set('Draw some worms')
        # #######################################
        drawWormsButton = tkinter.Button(
            worms.tkRoot,
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
            worms.tkRoot,
            text="Clear",
            fg="blue",
            bg="white",
            width=20,
            command=worms.clearDisplay
        )
        clearScreenButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(clearScreenButton, text="Clear display")
        # #######################################
        selectScreenFillButton = tkinter.Button(
            worms.tkRoot,
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
            worms.tkRoot,
            text="Random background color",
            fg="blue",
            bg="white",
            width=20,
            command=worms.randomBackgroundColor
        )
        randomScreenFillButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(randomScreenFillButton, text="Random background color")
        # #######################################
        selectForegroundColorButton = tkinter.Button(
            worms.tkRoot,
            text="Select foreground color",
            fg="blue",
            bg="white",
            width=20,
            command=worms.selectForegroundColor
        )
        selectForegroundColorButton.pack(
            side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X
        )
        ToolTip(selectForegroundColorButton, text="Select foreground color")
        # #######################################
        checkButtonFrame = tkinter.Frame(
            worms.tkRoot,
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
        ToolTip(clearBeforeDrawCheckButton, "Clear Before Draw")
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
            worms.tkRoot,
            fg="blue",
            bg="white",
            label="Speed",
            length=150,
            from_=1,
            to=40,
            variable=worms.speedVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED
        )
        speedSelect.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(speedSelect, "Select speed.")
        worms.speedVar.set(10)
        # #######################################
        blockSize = tkinter.Scale(
            worms.tkRoot,
            fg="blue",
            bg="white",
            label="Block size",
            length=150,
            from_=1,
            to=40,
            variable=worms.blockSizeVar,
            orient=tkinter.HORIZONTAL,
            relief=tkinter.RAISED
        )
        blockSize.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(blockSize, "Block size.")
        worms.blockSizeVar.set(10)
        # #######################################
        quitButton = tkinter.Button(
            worms.tkRoot,
            text="Quit",
            fg="blue",
            bg="white",
            width=20,
            command=worms.quitProgram
        )
        quitButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(quitButton, text="Quit the program")
        # #######################################
        worms.tkRoot.mainloop()

    def quitProgram():
        if debugMode:
            print("Quit using window X")
        pygame.display.quit
        pygame.quit()
        sys.exit(0)

    # #######################################
    def setUp():
        global debugMode
        global screen
        global tkRoot

        debugFile = "DougPyWorms.txt"
        if os.path.exists(debugFile):
            os.remove(debugFile)

        os.environ["SDL_VIDEO_WINDOW_POS"] = "%i, %i" % (
            screenPosHorizontal,
            screenPosVertical
        )

        screen = pygame.display.set_mode((worms.screenWidth, worms.screenHeight),
                                         pygame.RESIZABLE)

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
            "".join([os.path.dirname(__file__),
                     os.sep, "worm1.png"])
        )
        pygame.display.set_icon(img)
        pygame.display.set_caption("Draw some worms", "worms")

        # tkinter.update()
        screen.fill(worms.backgroundColor)
        pygame.display.flip()

        # Generate list of colors
        colorKeys = pygame.color.THECOLORS.keys()
        worms.colorList = list(colorKeys)
        if debugMode:
            print("Number of colors: ", len(worms.colorList))

    # #######################################
    def drawScreenText(infoString, screenWidth, screenHeight):
        directionFont = pygame.font.SysFont('Verdana', 20)
        infoFont = pygame.font.SysFont('Verdana', 20)

        fontColor = 'pink'
        northText = directionFont.render("North", True, fontColor)
        southText = directionFont.render("South", True, fontColor)
        eastText = directionFont.render("east", True, fontColor)
        westText = directionFont.render("west", True, fontColor)
        infoText = infoFont.render(infoString, True, fontColor)

        screen.blit(northText, (screenWidth / 2, 10))
        screen.blit(southText, (screenWidth / 2, screenHeight - 30))
        screen.blit(eastText, (screenWidth - 60,screenHeight / 2))
        screen.blit(westText, (10, screenHeight / 2))
        screen.blit(infoText, (screenWidth / 2, screenHeight / 2))
        pygame.display.flip()

    # #######################################
    def drawWorms():  # noqa: C901
        worms.screenWidth, worms.screenHeight = screen.get_size()
        if debugMode:
            print(worms.screenWidth, worms.screenHeight, '*' * 30)
        worms.rectangle_list = []

        # if a collision happens return true
        def testForCollision():
            collide = worms.rectangle_list.count(str(worms.playerNew))
            # collide = pygame.Rect.collidelist(worms.playerNew, worms.rectangle_list)
            if collide != 0:
                print('collide: ', collide)
                print(worms.playerNew, worms.rectangle_list)
                return (True, 'collide')
            if worms.playerNew.right >= worms.screenWidth:
                print('worms.playerNew.right <= worms.screenWidth', worms.playerNew.right, worms.screenWidth)
                return (True, 'east')
            if worms.playerNew.left <= 0:
                print('worms.playerNew.left <= 0', worms.playerNew.left, 0)
                return (True, 'west')
            if worms.playerNew.bottom >= worms.screenHeight:
                print('worms.playerNew.bottom >= worms.screenHeight', worms.playerNew.bottom, worms.screenHeight)
                return (True, 'south')
            if worms.playerNew.top <= 0:
                print('worms.playerNew.top <= 0', worms.playerNew.top, 0)
                return (True, 'north')

            # If a collision did not occur continue
            worms.rectangle_list.append(str(worms.playerNew))
            # if debugMode:
            # print('389', worms.rectangle_list, worms.playerNew)
            return (False, 'No collision')

        # ----------------------
        def calculateMove():
            # print('clock.tick: ', str(clock.tick(60)))
            if direction == 'N' or direction == 'NE' or direction == 'NW':
                worms.playerNew.top -= worms.blockSizeVar.get()  # Going up (North)
            if direction == 'S' or direction == 'SE' or direction == 'SW':
                worms.playerNew.bottom += worms.blockSizeVar.get()  # Going down (South)

            if direction == 'E' or direction == 'NE' or direction == 'SE':
                worms.playerNew.right += worms.blockSizeVar.get()  # Going right (East)
            if direction == 'W' or direction == 'NW' or direction == 'SW':
                worms.playerNew.left -= worms.blockSizeVar.get()  # Going left (West)

        # ----------------------
        # Get the starting position and direction
        horizontalPosition = random.randrange(10, worms.screenWidth - 10)
        verticalPosition = random.randrange(10, worms.screenHeight - 10)

        direction = random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

        # the following are for debugging
        # Also worms.playerOld is tweaked for debugging

        # horizontalPosition = 10
        # verticalPosition = 50
        # direction = 'W'

        # this puts info into the status label
        infoString = ' '.join([str(horizontalPosition),
                               str(verticalPosition),
                               str(direction)])
        worms.infoLabelVar.set(infoString)
        if debugMode:
            print('info: ', infoString)

        collided = False

        # (left, top), (width, height)
        worms.playerNew = Rect((horizontalPosition, verticalPosition),
                               (worms.blockSizeVar.get(), worms.blockSizeVar.get()))
        worms.playerOld = Rect((horizontalPosition, verticalPosition + 200),
                               (worms.blockSizeVar.get(), worms.blockSizeVar.get()))

        if worms.clearBeforeDrawCheckButtonVar.get():
            worms.clearDisplay()

        if worms.backgroundColorRandomCheckButtonVar.get():
            worms.randomBackgroundColor()

        if worms.foregroundColorRandomCheckButtonVar.get():
            color = random.randrange(0, len(worms.colorList))
            worms.foregroundColor = worms.colorList[color]

        # screen.fill(worms.backgroundColor)
        worms.drawScreenText(infoString, worms.screenWidth, worms.screenHeight)
        pygame.draw.rect(screen, worms.foregroundColor, worms.playerNew)
        pygame.draw.rect(screen, 'green', worms.playerOld)
        worms.rectangle_list.append(str(worms.playerOld))
        pygame.display.flip()

        # loop until collision
        while not collided:
            calculateMove()
            # print('clock.tick: ', str(clock.tick(60)))
            pygame.draw.rect(screen, worms.foregroundColor, worms.playerNew)
            pygame.display.flip()

            time.sleep(worms.speedVar.get() / 500)

            # returns true if we collided
            (collided, message) = testForCollision()

            if collided:
                if debugMode:
                    print('  '.join(['line: ', str(inspect.getframeinfo(inspect.currentframe()).lineno),
                                     'collided:', str(collided),
                                     'message:', message,
                                     'screenWidth:', str(worms.screenWidth),
                                     'screenHeight:', str(worms.screenHeight),
                                     'direction:', direction,
                                     'blockSize:', str(worms.blockSizeVar.get()),
                                     'speed:', str(worms.speedVar.get()),
                                     os.linesep,
                                     'worms.playerNew.bottom:', str(worms.playerNew.bottom),
                                     'worms.playerNew.top:', str(worms.playerNew.top),
                                     'worms.playerNew.left:', str(worms.playerNew.left),
                                     'worms.playerNew.right:', str(worms.playerNew.right),
                                     os.linesep,
                                     'rectangle count: ', str(len(worms.rectangle_list)),
                                     'sizeof.rectangle_list: ', str(sys.getsizeof(worms.rectangle_list))]))
            # pygame.draw.rect(screen, worms.foregroundColor, worms.playerNew)
            # pygame.display.flip()

    def clearDisplay():
        global debugMode
        screen.fill(worms.backgroundColor)
        pygame.display.flip()
        if debugMode:
            print("clearDisplay: ", worms.backgroundColor)

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

    def selectForegroundColor():
        global debugMode
        colors = askcolor(title="Foreground color chooser")
        if debugMode:
            print("selectForegroundColor: ", colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        worms.foregroundColor = colors[1]
        pygame.display.flip()
        if debugMode:
            print("selectForegroundColor: ", worms.foregroundColor)

    def selectBackgroundColor():
        global debugMode
        colors = askcolor(title="Background color chooser")
        if debugMode:
            print(colors[0], colors[1])
        if colors[0] is None:  # cancel was selected
            return
        worms.backgroundColor = colors[1]
        screen.fill(worms.backgroundColor)
        pygame.display.flip()
        if debugMode:
            print("selectBackgroundColor")

    def randomBackgroundColor():
        global debugMode
        color = random.randrange(0, len(worms.colorList))
        worms.backgroundColor = worms.colorList[color]
        screen.fill(worms.backgroundColor)
        pygame.display.flip()
        if debugMode:
            print("randomBackgroundColor: ", color, worms.backgroundColor)


# This is where we loop until user wants to exit
if __name__ == "__main__":
    worms.main()
