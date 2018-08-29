#programmed by Liam Jarvis
#
#Base on the project in the book Python Playground

import sys, argparse
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#good ol constants
ON = 255
OFF = 0
vals = [ON, OFF]

#adds a glider to the grid at the point given
def addGlider(i, j, grid):
    gilder = np.array([[0,0,255],[255,0,255],[0,255,255]])
    grid[i:i+3, j:j+3] = gilder

#generates a random grid
def randomGrid(N):
    return np.random.choice(vals, N*N, p=[.2,.8]).reshape(N,N)

#updates the grid according to the rules we've set
def update(frameNum, img, grid, N):
    #need to use a new grid else it could mess things up
    newGrid = grid.copy()
    
    #double loop to look at all of the sqaures on the grid
    for i in range(N):
        for j  in range(N):
            
            #first find all of the ON sqaures around the point i and j
            total = int((grid[i, (j-1)%N] + grid[i, (j+1)%N] + grid[(i-1)%N, j] + grid[(i+1)%N, j] + grid[(i-1)%N, (j-1)%N] + grid[(i-1)%N, (j+1)%N] + grid[(i+1)%N, (j-1)%N] + grid[(i+1)%N, (j+1)%N])/255)
            
            #applying rules
            if grid[i,j] == ON:
                if(total < 2) or (total > 3):
                    newGrid[i,j] = OFF
            else:
                if total == 3:
                    newGrid[i,j] = ON
    
    #once out of the loop, update the grid with the new grid
    img.set_data(newGrid)
    grid[:] = newGrid[:]
    return img

#my main squeeze
def main():
    parser = argparse.ArgumentParser(description="Run Conway's Game of Life1")
    
    #add all dem arguments
    parser.add_argument('--grid-size', dest='N', required=False)
    parser.add_argument('--mov-file', dest='movfile', required=False)
    parser.add_argument('--interval', dest='interval', required= False)
    parser.add_argument('--glider', action='store_true', required=False)
    parser.add_argument('--gosper', action='store_true', required=False)
    args = parser.parse_args()
    
    #setting grid size
    N = 100
    if args.N and int(args.N) > 8:
        N = int(args.N)
    
    #setting update interval
    updateInterval = 50
    if args.interval:
        updateInterval = args.interval
    
    #declaring grid
    grid = np.array([])
    #add glider to the thing
    if args.glider:
        grid = np.zeros(N*N).reshape(N, N)
        addGlider(1,1,grid)
    #make a random grid
    else:
        grid = randomGrid(N)
        
    #setting up the animation
    fig, ax = plt.subplots()
    img = ax.imshow(grid, interpolation='nearest')
    ani = animation.FuncAnimation(fig, update, fargs=(img,grid,N,), frames =10, interval=updateInterval,save_count = 50)
    
    #saving to mov file if args were provided
    if args.movfile:
        ani.save(args.moviefile, fps=30, extra_args=['-vcodec','libx254'])
        
    plt.show()
    
main()
