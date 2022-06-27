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
# https://www.pygame.org/docs/
# https://www.w3schools.com/python/

import os
import sys
import platform
import random
import time
import tkinter
from tkinter.colorchooser import askcolor
from tkinter import messagebox
import datetime
import pygame
from pygame.locals import Rect
# from screeninfo import get_monitors
# import inspect

from ToolTip import ToolTip
import inspect
import pprint

# Clear the terminal at program startup
os.system('cls||clear')
pp = pprint.PrettyPrinter(indent=4)

debugFile = "DougPyWorms.txt"
if os.path.exists(debugFile):
    os.remove(debugFile)


def line_info(message="nothing", show=False):
    f = inspect.currentframe()
    i = inspect.getframeinfo(f.f_back)
    tString = f"{os.path.basename(i.filename)}:{i.lineno}  called from {i.function}  {message}\n"
    file1 = open(debugFile, "a")
    file1.write(tString)
    file1.close()
    if show:
        print(tString)


if platform.system() == "Windows":
    os.environ["SDL_VIDEODRIVER"] = "windib"

# This positioning is for testing purposes on specific systems
if os.getenv("COMPUTERNAME") == 'DBKAYNOX-MOBL4':
    screenPosVertical = -600
    screenPosHorizontal = 250
elif platform.system() == "Linux":
    screenPosVertical = 0
    screenPosHorizontal = 250
elif platform.system() == "OS X":
    screenPosVertical = 0
    screenPosHorizontal = 0
else:
    line_info(' '.join(["Unknown platform:", platform.system()]))
    exit()

screen = 0
tkRoot = 0
pygame.init()
pygame.display.init()
# https://www.pygame.org/docs/ref/event.html
for event in pygame.event.get():
    if event.type == pygame.WINDOWRESIZED:
        line_info('resize event')


def about():
    messagebox.showinfo('About TkWorms',
                        os.linesep.join([' '.join(['Start directory: ',
                                                   os.getcwd()]),
                                         ' '.join(['Script name:',
                                                   os.path.basename(__file__)]),
                                         ' '.join(['Version:',
                                                   str(os.path.getmtime(__file__))]),
                                         ' '.join(['Geometry:',
                                                   tkRoot.geometry()]),
                                         ' '.join(['Screen size:',
                                                   str(tkRoot.winfo_screenwidth()),
                                                   'x',
                                                   str(tkRoot.winfo_screenheight())]),
                                         ' '.join(['Python version:',
                                                   platform.python_version()]),
                                         ' '.join(['Platform:',
                                                   platform.platform()])
                                         ]))


def setUp():
    # worms.guiDisable("tkinter.disabled")
    global screen
    global tkRoot
    line_info(' '.join(['Starting ', str(datetime.datetime.now())]), True)
    os.environ["SDL_VIDEO_WINDOW_POS"] = "%i, %i" % (
        screenPosHorizontal,
        screenPosVertical
    )
    pygame.init()
    screen = pygame.display.set_mode((worms.physicalScreenWidth, worms.physicalScreenHeight),
                                     pygame.RESIZABLE)

    pygame.event.pump()
    # monitorInfo = get_monitors()

    img = pygame.image.load(
        ''.join([os.path.dirname(__file__),
                 os.sep, "worm.png"])
    )
    pygame.display.set_icon(img)

    pygame.display.set_caption("Draw some worms", "Worms")
    screen.fill(worms.backgroundColor)
    pygame.display.flip()

    # Generate list of colors
    colorKeys = pygame.color.THECOLORS.keys()
    worms.colorList = list(colorKeys)


def quitProgram():
    pygame.display.quit
    pygame.quit()
    line_info(' '.join(['We are quitting ', str(datetime.datetime.now())]), True)
    sys.exit(0)


class worms:
    global screen
    global tkRoot
    tkRoot = tkinter.Tk()
    infoLabelVar = tkinter.StringVar()
    clearBeforeDrawCheckButtonVar = tkinter.BooleanVar()
    backgroundColorRandomCheckButtonVar = tkinter.BooleanVar()
    wrapCheckButtonVar = tkinter.BooleanVar()
    showTextCheckButtonVar = tkinter.BooleanVar()
    blockSizeVar = tkinter.IntVar()
    speedVar = tkinter.IntVar()
    colorPatternRadioVar = tkinter.IntVar()
    menuWidth = 250
    menuHeight = 550
    physicalScreenWidth = 417
    virtualScreenWidth = 0
    physicalScreenHeight = 253
    virtualScreenHeight = 0
    colorList = []
    rectangle_list = []
    player = []
    foregroundColor = 'orange'
    backgroundColor = "black"

    def main():
        global screenPosVertical
        global screenPosHorizontal
        global screen
        global tkRoot

        pygame.event.pump()
        # event = pygame.event.wait()
        # line_info(''.join(['vent: ', str(event)]))

        geometry = "".join(
            [
                str(worms.menuWidth),
                "x",
                str(worms.menuHeight),
                "+",
                str(screenPosHorizontal - worms.menuWidth - 10),
                "+",
                str(screenPosVertical),
            ]
        )

        tkRoot.geometry(geometry)
        tkRoot.resizable(height=False, width=False)
        tkRoot.title("Draw some worms")
        main_dialog = tkinter.Frame(tkRoot)
        main_dialog.pack(side=tkinter.TOP, fill=tkinter.X)
        line_info(''.join(["dirname:    ", os.path.dirname(__file__)]))
        image = tkinter.PhotoImage(
            file="".join([os.path.dirname(__file__), os.sep, "worm.png"])
        )
        tkRoot.iconphoto(True, image)
        setUp()
        # #######################################
        # line_info(str(infoLabel))
        # #######################################
        infoLabel = tkinter.Label(
            tkRoot,
            textvariable=worms.infoLabelVar,
            text="Clear",
            fg="green",
            bg="white",
            width=20)
        infoLabel.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        worms.infoLabelVar.set('Draw some worms')
        ToolTip(infoLabel, text="Display information about program")
        # #######################################
        line_info(str(worms.infoLabelVar.get()))
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
        ToolTip(clearScreenButton, text="Clear display")
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
        selectForegroundColorButton = tkinter.Button(
            tkRoot,
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
            tkRoot,
            bg="white",
            width=20,
            highlightbackground="black",
            highlightthickness=1,
            relief=tkinter.RAISED
        )
        checkButtonFrame.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        # #######################################
        clearBeforeDrawCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Clear before draw",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: line_info("Clear before draw"),
            variable=worms.clearBeforeDrawCheckButtonVar
        )
        clearBeforeDrawCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(clearBeforeDrawCheckButton, "Clear Before Draw")
        worms.clearBeforeDrawCheckButtonVar.set(True)
        # #######################################
        backgroundColorRandomCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Random background color",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: line_info("Random background color"),
            variable=worms.backgroundColorRandomCheckButtonVar
        )
        backgroundColorRandomCheckButton.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(backgroundColorRandomCheckButton, text="Random background color")
        worms.backgroundColorRandomCheckButtonVar.set(False)
        # #######################################
        wrapCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Wrap",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: line_info("Wrap (no walls)"),
            variable=worms.wrapCheckButtonVar
        )
        wrapCheckButton.pack(
            side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(wrapCheckButton, text="Wrap (no walls)")
        worms.wrapCheckButtonVar.set(False)
        # #######################################
        showTextCheckButton = tkinter.Checkbutton(
            checkButtonFrame,
            text="Show text",
            fg="blue",
            bg="white",
            onvalue=True,
            offvalue=False,
            command=lambda: line_info("Show text"),
            variable=worms.showTextCheckButtonVar
        )
        showTextCheckButton.pack(
            side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(showTextCheckButton, text="Show text")
        worms.showTextCheckButtonVar.set(True)
        # #######################################
        radioButtonFrame = tkinter.Frame(
            tkRoot,
            bg="white",
            width=20,
            highlightbackground="black",
            highlightthickness=1
        )
        radioButtonFrame.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        # #######################################
        colorPatternRadio0 = tkinter.Radiobutton(
            radioButtonFrame,
            fg="blue",
            bg="white",
            text="Never change color",
            value=0,
            command=lambda: line_info("Never change color"),
            variable=worms.colorPatternRadioVar
        )
        colorPatternRadio0.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(colorPatternRadio0, "Never change color.")
        # #######################################
        colorPatternRadio1 = tkinter.Radiobutton(
            radioButtonFrame,
            fg="blue",
            bg="white",
            text="Random color each run",
            value=1,
            command=lambda: line_info("Random color each run"),
            variable=worms.colorPatternRadioVar
        )
        colorPatternRadio1.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(colorPatternRadio1, "Random color each run.")
        # #######################################
        colorPatternRadio2 = tkinter.Radiobutton(
            radioButtonFrame,
            fg="blue",
            bg="white",
            text="Change color every step",
            value=2,
            command=lambda: line_info("Change color every step"),
            variable=worms.colorPatternRadioVar
        )
        colorPatternRadio2.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(colorPatternRadio2, "Change color every step.")
        # #######################################
        colorPatternRadio3 = tkinter.Radiobutton(
            radioButtonFrame,
            fg="blue",
            bg="white",
            text="Change color of collision point",
            value=3,
            command=lambda: line_info("Change color of collision point"),
            variable=worms.colorPatternRadioVar
        )
        colorPatternRadio3.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(colorPatternRadio3, "Change color of collision point.")
        # #######################################
        colorPatternRadio4 = tkinter.Radiobutton(
            radioButtonFrame,
            fg="blue",
            bg="white",
            text="Change foreground color after collision",
            value=4,
            command=lambda: line_info("Change foreground color after collision"),
            variable=worms.colorPatternRadioVar
        )
        colorPatternRadio4.pack(side=tkinter.TOP, anchor=tkinter.W)
        ToolTip(colorPatternRadio4, "Change foreground color after collision.")
        worms.colorPatternRadioVar.set(0)
        # #######################################
        speedSelect = tkinter.Scale(
            tkRoot,
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
        worms.speedVar.set(5)
        # #######################################
        blockSize = tkinter.Scale(
            tkRoot,
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
            tkRoot,
            text="Quit",
            fg="blue",
            bg="white",
            width=20,
            command=quitProgram
        )
        quitButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(quitButton, text="Quit the program")
        # #######################################
        aboutButton = tkinter.Button(
            tkRoot,
            text="About",
            fg="blue",
            bg="white",
            width=20,
            command=about
        )

        aboutButton.pack(side=tkinter.TOP, anchor=tkinter.W, fill=tkinter.X)
        ToolTip(aboutButton, text="About the program")

        # #######################################

        tkRoot.after(500, worms.clearDisplay)
        tkRoot.mainloop()

        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                quitProgram()
                """
                pygame.display.quit
                pygame.quit()
                line_info(' '.join(['We are quitting ', str(datetime.datetime.now())]), True)
                sys.exit(0)
                 """

    # #######################################
    def drawScreenText(infoString, virtualScreenWidth, virtualScreenHeight):
        directionFont = pygame.font.SysFont('Verdana', 20)
        infoFont = pygame.font.SysFont('Verdana', 20)

        fontColor = 'pink'
        northText = directionFont.render("North", True, fontColor)
        southText = directionFont.render("South", True, fontColor)
        eastText = directionFont.render("East", True, fontColor)
        westText = directionFont.render("West", True, fontColor)
        infoText = infoFont.render(infoString, True, fontColor)
        fgText = infoFont.render(worms.foregroundColor, True, fontColor)
        bgText = infoFont.render(worms.backgroundColor, True, fontColor)
        size = ' '.join([str(virtualScreenWidth), str(virtualScreenHeight)])
        sizeText = infoFont.render(size, True, fontColor)

        screen.blit(northText, (virtualScreenWidth / 2, 10))
        screen.blit(southText, (virtualScreenWidth / 2, virtualScreenHeight - 30))
        screen.blit(eastText, (virtualScreenWidth - 60, virtualScreenHeight / 2))
        screen.blit(westText, (10, virtualScreenHeight / 2))
        screen.blit(infoText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 10))
        screen.blit(bgText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 35))
        screen.blit(fgText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 60))
        screen.blit(sizeText, (virtualScreenWidth / 2 - 35, virtualScreenHeight / 2 - 85))
        pygame.display.flip

    # #######################################
    def drawWorms():  # noqa: C901
        # if a collision happens, return true
        line_info('---- Draw button was clicked ----', True)

        def didCollisionHappen():
            collide = worms.rectangle_list.count(str(worms.player))
            if collide != 0:
                return (True, 'collide')
            if worms.player.right > worms.virtualScreenWidth:
                if worms.wrapCheckButtonVar.get():
                    line_info('worms.player.right')
                    worms.player.right = worms.blockSizeVar.get()
                else:
                    return (True, 'east')
            if worms.player.left < 0:
                if worms.wrapCheckButtonVar.get():
                    line_info('worms.player.left')
                    worms.player.left = worms.virtualScreenWidth - worms.blockSizeVar.get()
                    return (False, 'west')
                else:
                    return (True, 'west')
            if worms.player.bottom > worms.virtualScreenHeight:
                if worms.wrapCheckButtonVar.get():
                    line_info('worms.player.bottom')
                    worms.player.bottom = worms.blockSizeVar.get()
                    return (False, 'south')
                else:
                    return (True, 'south')
            if worms.player.top < 0:
                if worms.wrapCheckButtonVar.get():
                    line_info('worms.player.top')
                    worms.player.top = worms.virtualScreenHeight - worms.blockSizeVar.get()
                else:
                    return (True, 'north')

            # If a collision did not occur continue
            worms.rectangle_list.append(str(worms.player))
            return (False, 'No collision')

        # ----------------------
        def calculateMove():
            # line_info(' '.join(['clock.tick: ', str(clock.tick(60))]))
            if direction == 'N' or direction == 'NE' or direction == 'NW':
                worms.player.bottom -= worms.blockSizeVar.get()  # Going up (North)
            if direction == 'S' or direction == 'SE' or direction == 'SW':
                worms.player.top += worms.blockSizeVar.get()  # Going down (South)
            if direction == 'E' or direction == 'NE' or direction == 'SE':
                worms.player.left += worms.blockSizeVar.get()  # Going right (East)
            if direction == 'W' or direction == 'NW' or direction == 'SW':
                worms.player.right -= worms.blockSizeVar.get()  # Going left (West)

        # ----------------------
        # Start drawWorms here

        worms.physicalScreenWidth, worms.physicalScreenHeight = screen.get_size()
        line_info(' '.join(['physical:', str(worms.physicalScreenWidth), str(worms.physicalScreenHeight)]))
        worms.virtualScreenWidth = int(worms.physicalScreenWidth / worms.blockSizeVar.get()) * worms.blockSizeVar.get()
        worms.virtualScreenHeight = int(worms.physicalScreenHeight / worms.blockSizeVar.get()) * worms.blockSizeVar.get()
        line_info(' '.join(['virtual:', str(worms.virtualScreenWidth), str(worms.virtualScreenHeight)]))

        worms.rectangle_list = []
        collided = False

        if worms.clearBeforeDrawCheckButtonVar.get():
            worms.clearDisplay()

        if worms.backgroundColorRandomCheckButtonVar.get():
            worms.randomBackgroundColor()

        if worms.colorPatternRadioVar.get() == 1:
            color = random.randrange(0, len(worms.colorList))
            worms.foregroundColor = worms.colorList[color]

        # Get the starting position and direction
        # Values need to be an even multiple on blockSize
        try:
            OFFSET = worms.blockSizeVar.get() * 2  # This is how far from the screen edges to allow
            xx = int(worms.virtualScreenWidth / worms.blockSizeVar.get()) * worms.blockSizeVar.get()
            horizontalPosition = random.randrange(OFFSET, xx - OFFSET, worms.blockSizeVar.get())
            yy = int(worms.virtualScreenHeight / worms.blockSizeVar.get()) * worms.blockSizeVar.get()
            verticalPosition = random.randrange(OFFSET, yy - OFFSET, worms.blockSizeVar.get())
        except Exception as e:
            line_info(' '.join([str(e), 'block size versus screen size.']))
            horizontalPosition = 10
            verticalPosition = 10

        # horizontalPosition = random.randrange(OFFSET, worms.virtualScreenWidth - OFFSET)
        # verticalPosition = random.randrange(OFFSET, worms.virtualScreenHeight - OFFSET)
        direction = random.choice(['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'])

        # Calculate where the player should go
        # (left, top), (width, height)
        # This is the first location
        worms.player = Rect((horizontalPosition, verticalPosition),
                            (worms.blockSizeVar.get(), worms.blockSizeVar.get()))
        pygame.draw.rect(screen, 'green', worms.player)
        pygame.display.flip()
        # this puts info into the status label
        infoString = ' '.join([str(horizontalPosition),
                               str(verticalPosition),
                               str(direction)])
        worms.infoLabelVar.set(' '.join([infoString,
                                         worms.foregroundColor,
                                         worms.backgroundColor]))
        tkRoot.update_idletasks()

        if worms.showTextCheckButtonVar.get():
            worms.drawScreenText(infoString,
                                 worms.virtualScreenWidth,
                                 worms.virtualScreenHeight)
        pygame.display.flip()

        # loop until collision
        maxCollisions = 100
        collisionCount = 0
        tmpList = []  # tmpList is used to verify that all possible directions have been tried
        while not collided:
            saveLeft = str(worms.player.left)
            saveTop = str(worms.player.top)
            calculateMove()
            (collided, message) = didCollisionHappen()
            if not collided:  # Continue on moving
                # 0 Never change color
                # 1 Random color each run
                # 2 Change color every step
                # 3 Change color every corner
                # 4 Change foreground color after collision
                color = 0
                colorListValue = 0
                if worms.colorPatternRadioVar.get() == 0:
                    color = worms.foregroundColor
                elif worms.colorPatternRadioVar.get() == 1:
                    color = worms.foregroundColor
                elif worms.colorPatternRadioVar.get() == 2:
                    colorListValue = random.randrange(0, len(worms.colorList))
                    color = worms.colorList[colorListValue]
                elif worms.colorPatternRadioVar.get() == 3:
                    color = worms.foregroundColor
                elif worms.colorPatternRadioVar.get() == 4:
                    color = worms.foregroundColor
                else:
                    line_info('?????')
                # line_info(' '.join([str(colorListValue), str(color), str(worms.colorPatternRadioVar.get())]))
                pygame.draw.rect(screen, color, worms.player)
                pygame.display.flip()
                collisionCount = 0
                time.sleep(worms.speedVar.get() / 500)
                tmpList = []
            else:  # A collision occurred
                worms.player = Rect((int(saveLeft), int(saveTop)),
                                    (worms.blockSizeVar.get(), worms.blockSizeVar.get()))
                if worms.colorPatternRadioVar.get() == 2:
                    pygame.draw.rect(screen, 'pink', worms.player)  # This is a collision point
                if worms.colorPatternRadioVar.get() == 3:
                    pygame.draw.rect(screen, 'white', worms.player)
                # Change color every corner if needed
                if worms.colorPatternRadioVar.get() == 4:
                    colorListValue = random.randrange(0, len(worms.colorList))
                    worms.foregroundColor = worms.colorList[colorListValue]
                pygame.display.flip()
                directionList = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
                if collisionCount < maxCollisions:
                    direction = random.choice(directionList)
                    tmpList.append(direction)
                else:
                    direction = directionList[5]
                    print()
                collided = False
                # line_info(' '.join(['length tmpList', str(len(tmpList))]))
                collisionCount += 1
                if collisionCount >= maxCollisions:
                    pygame.draw.rect(screen, 'yellow', worms.player)  # This is the very last collision point
                    pygame.display.flip()
                    line_info(' '.join(['Collisions:',
                                        str(maxCollisions),
                                        str(collisionCount),
                                        str(len(tmpList))]))
                    tmpList.sort()
                    for i in directionList:
                        if i not in tmpList:
                            line_info(' '.join(['Not in tmpList:',
                                                str(i)]))
                    break

    # #######################################
    def clearDisplay():
        screen.fill(worms.backgroundColor)
        pygame.display.flip()

    def selectForegroundColor():
        colors = askcolor(title="Foreground color chooser")
        if colors[0] is None:  # cancel was selected
            return
        worms.foregroundColor = colors[1]
        pygame.display.flip()

    def selectBackgroundColor():
        colors = askcolor(title="Background color chooser")
        if colors[0] is None:  # cancel was selected
            return
        worms.backgroundColor = colors[1]
        screen.fill(worms.backgroundColor)
        pygame.display.flip()

    def randomBackgroundColor():
        color = random.randrange(0, len(worms.colorList))
        worms.backgroundColor = worms.colorList[color]
        screen.fill(worms.backgroundColor)
        pygame.display.flip()


# This is where we loop until user wants to exit
if __name__ == "__main__":
    worms.main()
