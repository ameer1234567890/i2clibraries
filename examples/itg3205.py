from i2clibraries import i2c_itg3205
from time import *

itg3205 = i2c_itg3205.i2c_itg3205(0)

while True:
   (itgready, dataready) = itg3205.getInterruptStatus()   
   if dataready:
      temp = itg3205.getDieTemperature()
      (x, y, z) = itg3205.getDegPerSecAxes() 
      print("Temp: "+str(temp))
      print("X:    "+str(x))
      print("Y:    "+str(y))
      print("Z:    "+str(z))
      print("")
   
   sleep(1)
