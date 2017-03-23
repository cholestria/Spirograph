import sys, random, argparse
import numpy as np
import math
import turtle
import random
from PIL import Image
from datetime import datetime
from fractions import gcd


class Spiro:
    #constructor
    def __init__(self, xc, yc, col, R, r, l):

        #create the turtle object
        self.t = turtle.Turtle()
        #set the cursor shape
        self.t.shape('turtle')
        #set the step in degrees
        self.step = 5
        #set the drawing complete flag
        self.drawingComplete = False

        #set the parameters
        self.setparams(xc, yc, col, R, r, l)

        #initialize the drawing
        self.restart()

    def setparams(self, xc, yc, col, R, r, l):

        #the spirograph parameters
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col

        #reduce r/R to it's smallest form
        gcdVal = gcd(self.r, self.R)
        self.nRot = self.r//gcdVal

        #get the ratio of radii
        self.k = r/float(R)

        #set the color
        self.t.color(*col)

        #set the current angle
        self.a = 0

    def restart(self):
        #raise pen
        self.t.up()

        #set the flag
        self.drawingComplete = False

        #show the turtle
        self.t.showturtle()

        # go to the first point
        R, k, l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()

    def draw(self):
        #draw the points
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)

        #when drawing is done, hide the cursor
        self.t.hideturtle()

    def update(self):
        #skip the rest of the steps if done
        if self.drawingComplete:
            return
        #increment the angle
        self.a += self.step
        #draw a step
        R, k, l = self.R, self.k, self.l
        #set the angle
        a = math.radians(self.a)
        x = self.R*((1-k)*math.cos(a) + l*k*math.cos((1-k)*a/k))
        y = self.R*((1-k)*math.sin(a) - l*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        #if drawing is complete, set the flag
        if self.a >= 360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

    def clear(self):
        self.t.clear()


class SpiroAnimator():
    def __init__(self, N):
        #set timer in milliseconds
        self.deltaT = 10
        #get window dimensions
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        #create the spiro object
        self.spiros = []
        for i in range(N):
            #generate random parameters
            rparams = self.genRandomParams()
            #set the spiro parameters
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        #call timer
        turtle.ontimer(self.update, self.deltaT)

    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(),
               random.random(),
               random.random())
        return (xc, yc, col, R, r, l)

    def restart(self):
        for spiro in self.spiros:
            #clear
            spiro.clear()
            #generate random parameters
            rparams = self.genRandomParams()
            #set the spiro parameters
            spiro.setparams(*rparams)
            #restart drawing
            spiro.restart()

    def update(self):
        #update all spiros
        nComplete = 0
        for spiro in self.spiros:
            #update
            spiro.update()
            #count completed spiros
            if spiro.drawingComplete:
                nComplete += 1
        #restart is all spiros are complete
        if nComplete == len(self.spiros):
            self.restart()
        #call the timer
        turtle.ontimer(self.update, self.deltaT)

    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()


def saveDrawing():
    #hide the turtle cursor
    turtle.hideturtle()
    #generate unique filenames
    dateStr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    fileName = 'spiro-' + dateStr
    print('Saving drawing to %s.eps/png' % fileName)

    #get the tkinter canvas
    canvas = turtle.getcanvas()

    #save the drawing as a postscript image
    canvas.postscript(file = fileName + '.eps')

    #use the Pillow module to convert the postscript image file to PNG
    img = Image.open(fileName + '.eps')
    img.save(fileName + '.png', 'png')

    #show the cursor
    turtle.showturtle()


def main():
    print('generating spirograph...')
    #create parser
    descStr = """This program draws Spirographs using the Turtle module. When
    run with no aruments, this prgram draws random Spirographs.

    Terminology:
    R: radius of the outer circle
    r: raidus of the inner circle
    l: ratio of hole distance to r
    """

    parser = argparse.ArgumentParser(description=descStr)

    #add expected arguments
    parser.add_argument('--sparams', nargs=3, dest='sparams', required=False,
                        help='The three arguments in sparams: R, r, l.')

    #parse args
    args = parser.parse_args()

    #set the width of the drawing window to 80% of the screen width
    turtle.setup(width=0.8)

    #set the cursor shape to turtle
    turtle.shape('turtle')

    #set the title to Spirographs
    turtle.title("Spirographs!")

    #add the key handler for save drawings
    turtle.onkey(saveDrawing, "s")

    #start listening
    turtle.listen()

    #hide the main turtle cursor
    turtle.hideturtle()

    #check for arguments send to --sparams and draw the Spirograph
    if args.sparams:
        params = [float(x) for x in args.sparams]
        #draw the spirograph with the given parameters
        col = (0.0, 0.0, 0.0)
        spiro = Spiro(0, 0, col, *params)
        spiro.draw()
    else:
        #create the animator object
        spiroAnim = SpiroAnimator(4)
        #add a key handler to toggle the cursor
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        #add a key handler to restart
        turtle.onkey(spiroAnim.restart, "space")

    #start the turtle main loop
    turtle.mainloop()

if __name__ == "__main__":
    main()
