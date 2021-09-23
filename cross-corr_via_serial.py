#numpy version
import numpy as np
import serial, sys, time
#import matplotlib.pyplot as plt

def find_index(c):  # find index of maximum value
  mc=np.amax(c)
  for i in range(len(c)):
    if c[i]==mc:
      im=i
      break
  return im

ser=serial.Serial(sys.argv[1], sys.argv[2])  #open serial port
print("connected to: " + ser.portstr)
time.sleep(2)
i=0
d1=np.empty(0)
d2=np.empty(0)
f = open(sys.argv[3], "w")   # open file
while True:
  try:
	  line = ser.readline()
	  line2=line.strip().decode('utf-8',errors='replace')
	  data = [str(val) for val in line2.split(",")]
#	  print(line2)
	  if i<100 and len(data)==11: # and len(d1)<100 and len(d2)<100:
#	    if isinstance(data[1], float) and isinstance(data[2], float):
	    d1=np.append(d1,np.float(data[1]))
	    d2=np.append(d2,np.float(data[2]))
	    i=i+1
	  else:
	    if len(d1)!=0:
	      c=1.0/(np.linalg.norm(d1)*np.linalg.norm(d2)) 
	      print(len(d1))
	      f1=np.fft.fft(d1)
	      f2=np.conjugate(np.fft.fft(d2))
	      ff=f1*f2
	      corrf=np.real(np.fft.ifft(ff))*c
#find max
	      print("cross-correlation: max and index")
	      print(np.amax(corrf))
	      print(find_index(corrf))

	    d1=np.empty(0)
	    d2=np.empty(0)
	    corr=np.empty(0)
	    i=0
  except KeyboardInterrupt:
    print ('exiting')
    ser.cloase()
    f.close()
    exit()
    break
