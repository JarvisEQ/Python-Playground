import numpy as np
import wave
import math as maths

#simpele project that outputs a wave file that plays a sinwave
#this is the prelude to Guitar.py

sRate = 44100
nSamples = sRate * 5
x = np.arange(nSamples)/float(sRate)
vals = np.sin(2.0*maths.pi*220.0*x)
data = np.array(vals*32767, 'int16').tostring()
file = wave.open('sine220.wav' , 'wb')
file.setparams((1,2,sRate,nSamples,'NONE','uncompressed'))
file.writeframes(data)
file.close()

