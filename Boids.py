#boids boids boids
#boids everywhere
#flapping dem wings, without purpose
#but they are just a simulation
#and I am not
#or possibly I am
#but who the fuck really cares
#Suno Luno

import sys, argparse
import math as maths
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.spatial.distance import squareform, pdist, cdist
from numpy.linalg import norm

width, height = 640, 480

class Boids:

    def __init__(self, N):
        #setting up dem BOIDS
        self.pos = [width/2, height/2] + 10*np.random.rand(2*N).reshape(N, 2)
        angles = 2*maths.pi*np.random.rand(N)
        self.vel = np.array(list(zip(np.sin(angles), np.cos(angles))))
        self.N = N
        self.minDist = 25.0
        self.maxRuleVel = 0.03
        self.maxVal = 2.0

    def tick(self, frameNum, pts, beak):
        #this does one tick of the simulation
        #IE, change everything by just a little
        self.distMatrix = squareform(pdist(self.pos))

        #apply rulez to the boids
        self.vel += self.applyRules()
        self.limit(self.vel, self.maxVal)
        self.pos += self.vel
        self.applyBC()

        #updating stuff
        pts.set_data(self.pos.reshape(2*self.N)[::2], self.pos.reshape(2*self.N)[1::2])
        vec = self.pos + 10*self.vel/self.maxVal
        beak.set_data(vec.reshape(2*self.N)[::2], vec.reshape(2*self.N)[1::2])

    def limitVec(self, vec, maxVal):
    	#keep the magnitude of the thing within limits
        mag = norm(vec)
        if mag > maxVal:
        	vec[0], vec[1] = vec[0]*maxVal/mag , vec[1]*maxVal/mag


    def limit(self, X, maxVal):
        for vec in X:
        	self.limitVec(vec, maxVal)

    def applyBC(self):
        #apply boundary conditions
        deltaR = 2.0

        for coord in self.pos:
        	if coord[0] > width + deltaR:
        		coord[0] = -deltaR
        	if coord[0] < -deltaR:
        		coord[0] = width - deltaR
        	if coord[1] > height + deltaR:
        		coord[1] = -deltaR
        	if coord[1] < -deltaR:
        		coord[1] = height + deltaR

    def applyRules(self):
        #rule 1, seperation
        D = self.distMatrix < .25
        vel = self.pos*D.sum(axis=1).reshape(self.N, 1) - D.dot(self.pos)
        self.limit(vel, self.maxRuleVel)

        #rule 2, alignment
        vel2 = D.dot(self.vel)
        self.limit(vel2, self.maxRuleVel)
        vel += vel2

        #rule 3, cohesion
        vel3 = D.dot(self.pos) - self.pos
        self.limit(vel3, self.maxRuleVel)
        vel += vel3

        return vel

    def buttonPress(self, event):
        # leftclick to add boids
        if event.button is 1:
            self.pos = np.concatenate((self.pos, np.array([[event.xdata, event.ydata]],)), axis = 0)

            #gives it a random velocity
            angles = 2*maths.pi*np.random.rand(1)
            v = np.array(list(zip(np.sin(angles), np.cos(angles))))
            self.vel =  np.concatenate((self.vel, v), axis = 0)
            self.N += 1
        #right click to scatter the BOIDS
        elif event.button is 3:
            self.vel += 0.1*(self.pos - np.array([[event.xdata, event.ydata]]))

def tick(frameNum, pts, beak, boids):
        boids.tick(frameNum, pts, beak)
        return pts, beak

def main():

    #FIRING MY PARSERS BOOOOOOM
    parser = argparse.ArgumentParser(description = "Implementing BOIDS")
    parser.add_argument('--num-boids', dest='N', required=False)
    args = parser.parse_args()

    #settinng number of BOIDS
    N = 100
    if args.N:
        N = int(args.N)

    #making BOIDS
    boids = Boids(N)

    #set up das plot
    fig = plt.figure()
    ax = plt.axes(xlim=(0, width), ylim=(0, height))

    pts, = ax.plot([],[], markersize=10, c='k', marker='o', ls='None')
    beak, = ax.plot([],[], markersize=4, c='r', marker='o', ls='None')
    anim = animation.FuncAnimation(fig, tick, fargs=(pts, beak, boids), interval=50)

    #event handler for button
    cid = fig.canvas.mpl_connect('button_press_event', boids.buttonPress)

    plt.show()

main()
