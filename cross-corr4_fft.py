#numpy version
import numpy as np
import serial, sys, time
import matplotlib.pyplot as plt

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
	  line2=line.strip().decode('utf-8')
	  data = [str(val) for val in line2.split(",")]
	#  print(line2)
	  if i<100 and len(data)==11 and data[1]!="" and data[2]!="":
	    d1=np.append(d1,np.float(data[1]))
	    d2=np.append(d2,np.float(data[2]))
	    i=i+1
	  else:
	    x=range(len(d1)) #plot array
	    plt.plot(x,d1)
	    plt.show()
	    plt.plot(x,d2)
	    plt.show()
	    c=1.0/(np.linalg.norm(d1)*np.linalg.norm(d2))   # added on 16.Sep.2021
	    corr=np.empty(0)   #make nd.array of length zero
	    corr=np.append(corr,np.dot(d1,d2)*c)  # the first element of corr, modified on 16.Sep.2021
	    for i in range(len(d1)):
	      d2=np.roll(d2,1)  # shift 1 to the left
	      corr=np.append(corr,np.dot(d1,d2)*c)   # cross correlation, modified on 16.Sep.2021
	    mx=np.amax(corr)
	    print("shift: max and indwx")
	    print(mx)
	    for i in range(len(corr)):
	      if corr[i]==mx:
	        ix=i
	        break
	    print(ix)
	    x=range(len(corr)) #plot array
	    plt.plot(x,corr)
	    plt.show()
	    
	    c=1.0/(np.linalg.norm(d1)*np.linalg.norm(d2)) 
	    f1=np.fft.fft(d1)
	    f2=np.conjugate(np.fft.fft(d2))
	    ff=f1*f2
	    corrf=np.real(np.fft.ifft(ff))*c
#find max
	    print("cross-correlation: max and indwx")
	    print(np.amax(corrf))
	    print(find_index(corrf))

	    x=range(len(corrf)) #plot array
	    plt.plot(x,corrf)
	    plt.show()

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
