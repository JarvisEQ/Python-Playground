import math
import turtle
import sys, random, argparse
import numpy as np
import random
from PIL import Image
from datetime import datetime
from fractions import gcd


def drawCricle(x, y, r):
    turtle.up()
    turtle.setpos(x+r, y)
    turtle.down()

    for i in range(0, 365, 5):
        a = math.radians(i)
        turtle.setpos(x + r*math.cos(a), y + r*math.sin(a))

#this class is one spiro
class Spiro:
    def __init__(self, xc, yc, col, R, r, l):
        self.t = turtle.Turtle()
        self.t.shape("turtle")
        self.step = 5
        self.drawingComplete = False
        self.setparams(xc, yc, col, R, r, l)
        self.restart()
        
        #sets parameters, amazing I know
    def setparams(self, xc, yc, col, R, r, l):
        self.xc = xc
        self.yc = yc
        self.R = int(R)
        self.r = int(r)
        self.l = l
        self.col = col
        gcdval = gcd(self.r, self.R)
        self.nRot = self.r//gcdval
        self.k = r/float(R)
        self.t.color(*col)
        self.a = 0
        
        #starts the sprio up again
    def restart(self):
        self.drawingComplete = False
        self.t.showturtle()
        self.t.up()
        R, k ,l = self.R, self.k, self.l
        a = 0.0
        x = R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        self.t.down()
        
        #making the thing a thing
    def draw(self):
        R, k, l = self.R, self.k, self.l
        for i in range(0, 360*self.nRot + 1, self.step):
            a = math.radians(i)
            x = R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
            y = R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
            self.t.setpos(self.xc + x, self.yc + y)
        #Imma just hide this thing 
        self.t.hideturtle
    
    #update the drawing by one step
    def update(self):
        if self.drawingComplete:
            return
        self.a += self.step
        R ,k ,l = self.R, self.k, self.l
        a = math.radians(self.a)
        x = R*((1-k)*math.cos(a) + 1*k*math.cos((1-k)*a/k))
        y = R*((1-k)*math.sin(a) - 1*k*math.sin((1-k)*a/k))
        self.t.setpos(self.xc + x, self.yc + y)
        if self.a > 360*self.nRot:
            self.drawingComplete = True
            self.t.hideturtle()

    def clear(self):
        self.t.clear

#this class creates a abunch of spiros
class SpiroAnimator:
    #the magical constructor
    def __init__(self, N):
        #timer is set in milisecounds
        self.deltaT = 10
        self.width = turtle.window_width()
        self.height = turtle.window_height()
        self.spiros = []
        for i in range(N):
            rparams = self.genRandomParams()
            spiro = Spiro(*rparams)
            self.spiros.append(spiro)
        turtle.ontimer(self.update, self.deltaT)
        
    #makes random parameters for the spiros
    def genRandomParams(self):
        width, height = self.width, self.height
        R = random.randint(50, min(width, height)//2)
        r = random.randint(10, 9*R//10)
        l = random.uniform(0.1, 0.9)
        xc = random.randint(-width//2, width//2)
        yc = random.randint(-height//2, height//2)
        col = (random.random(), random.random(), random.random())
        return(xc, yc, col, R, r, l)
    
    #clears the spiros and makes new ones
    def restart(self):
        for spiro in self.spiros:
            spiro.clear()
            rparams = self.genRandomParams()
            spiro.setparams(*rparams)
            spiro.restart()
            
    def update(self):
        nComplete = 0
        for spiro in self.spiros:
            spiro.update()
            if spiro.drawingComplete:
                nComplete += 1
        if nComplete == len(self.spiros):
            self.restart()
        turtle.ontimer(self.update, self.deltaT)
        
    def toggleTurtles(self):
        for spiro in self.spiros:
            if spiro.t.isvisible():
                spiro.t.hideturtle()
            else:
                spiro.t.showturtle()
                
                
#saves the spiro as a png image file
def saveDrawing():
    turtle.hideturtle()
    datestr = (datetime.now()).strftime("%d%b%Y-%H%M%S")
    filename = "spiro" + datestr
    print("saving drawing as %s.eps/png" %filename)
    canvas = turtle.getcanvas()
    canvas.postscript(file = filename + ".eps")
    img = Image.open(filename + ".eps")
    img.save(filename + ".png", "png")
    turtle.showturtle()
        
def main():
    print("yuup yuup, making dem spirographs")
    
    descStr = "This program makes Spirographs using turtle. When given no arguments, this program will make 4 random Spirographs"
    
    
    #paser to take in command line argumnets
    parser = argparse.ArgumentParser(description = descStr)
    parser.add_argument('--sparams', nargs=3, dest ='sparams', required=False, 
                        help = "The three arguments in sparams: R, r, l")
    args = parser.parse_args()
    
    #setting up thy turtle
    turtle.setup(width=.8, height=.8)
    turtle.shape('turtle')
    turtle.title("Magical Spirographs!")
    turtle.onkey(saveDrawing, "s")
    turtle.listen()
    turtle.hideturtle()
    
    #this is where the magic happens
    #check if given command line arguments and makes one according to those args
    #if not, 4 random ones will be generated
    if args.sparams:
        params = [float(x) for x in args.sparams]
        #default colour is black, because I want to paint it black
        col = (0.0,0.0,0.0)
        spiro = Spiro(0,0,col,*params)
        spiro.draw()
    else:
        spiroAnim = SpiroAnimator(4)
        turtle.onkey(spiroAnim.toggleTurtles, "t")
        turtle.onkey(spiroAnim.restart, "space")
    
    turtle.mainloop()
    
    
#need to do this, i guess
main()        
