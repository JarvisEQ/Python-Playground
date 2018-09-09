import sys, os
import time, random
import wave, argparse, pygame
import numpy as np
from collections import deque
from matplotlib import pyplot as plt

#nasty global variable, plz ignore
gShowPlot = False

#the pentatonic minor scale
pmNotes = {'4C' : 262, 'Eb' : 311 , 'F' : 349 , 'G' : 391 , 'Bb' : 466}

#give a frequency, this function returns a note corresponding to that frequency
def generateNote(freq):
    nSamples = 44100
    sampleRate = 44100
    N = int(sampleRate/freq)
    
    #making the ring buffer
    buf = deque([random.random() - .05 for i in range(N)])

    #doing the things with the plot
    if gShowPlot:
    	axline, = plt.plot(buf)

    samples = np.array([0]*nSamples, 'float32')
    for i in range(nSamples):
    	samples[i] = buf[0]
    	avg = 0.996*0.5*(buf[0] + buf[1])
    	buf.append(avg)
    	buf.popleft()
    	if gShowPlot:
    		if i % 100 == 0:
    			axline.set_ydata(buf)
    			plt.draw()

    #convert sample t0 16-bit values
    samples = np.array(samples*32767, 'int16')
    return samples.tostring()

#this writes stuff to a WAVE file
def writeWAVE(fname, data):
	
	file = wave.open(fname, 'wb')

	#file params and setting them
	nChanels = 1
	sampleWidth = 2
	framesRate = 44100
	nFrames = 44100
	file.setparams((nChanels,sampleWidth,framesRate,nFrames,'NONE','noncompressed'))

	#setting the data and closing the file
	file.writeframes(data)
	file.close() 

#this plays music
class NotePlayer:

	#make me senpai
	def __init__(self):
		pygame.mixer.pre_init(44100, -16, 1, 2048)
		pygame.init()
		self.notes = {}

	#method to add a note
	def add(self, filename):
		self.notes[filename] = pygame.mixer.Sound(filename)

	#play a note
	def play(self, filename):
		try:
			self.notes[filename].play()
		except:
			print(filename + " not found")

	#this just plays whatever
	def playRandom(self):
		index = random.randint(0, len(self.notes)-1)
		note = list(self.notes.values())[index]
		note.play()

#my mane squeeze
def main():
	global gShowPlot

	#das parsering of the arguments
	#so argumental sometimes smh
	parser = argparse.ArgumentParser(description="Generating sounds with the Karplus String Algorithm")
	parser.add_argument('--display', action='store_true', required=False)
	parser.add_argument('--play', action='store_true', required=False)
	parser.add_argument('--piano', action='store_true', required=False)
	args = parser.parse_args()

	#show plot if flag was set
	if args.display:
		gShowPlot = True
		plt.ion()

	#create note player
	nPlayer = NotePlayer()

	for name, freq in list(pmNotes.items()):
		filename = name + ".wav"
		#if we need to make a file for the note
		if not os.path.exists(filename) or args.display:
			data = generateNote(freq)
			print("creating " + filename)
			writeWAVE(filename, data)
		#if we don't have to make a file
		else:
			print("Thing is already a thing, moving along")

		#adding the notes to the player
		nPlayer.add(name + ".wav")

		#playing if tag is set
		if args.display:
			nPlayer.play(name + ".wav")
			time.sleep(0.5)

	#playing random crap
	if args.play:
		while True:
			try:
				nPlayer.playRandom()
				#rest - 1 to 8 beats
				rest = np.random.choice([1,2,4,8], 1, p=[0.15, 0.7, 0.1, 0.05])
				time.sleep(0.25*rest[0])
			except KeyBoardInterrupt:
				exit()
				# interrupts are the best!

	#random piano
	if args.piano:
		while True:
			for event in pygame.event.get():
				if (event.type == pygame.KEYUP):
					print("YOU PRESSED A KEY REEEEEEEEE")
					nPlayer.playRandom()
					time.sleep(0.5)


if __name__ == '__main__':
	main()