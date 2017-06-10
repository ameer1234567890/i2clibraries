from i2clibraries import i2c_adxl345
from time import *

adxl345 = i2c_adxl345.i2c_adxl345(0)

adxl345.setInterrupt(adxl345.FreeFall)

while True:
        # Determine if interrupt set
        [dataready, singletap, doubletap, activity, inactivity, freefall, watermark, overrun] = adxl345.getInterruptStatus()
        
        if freefall:
                print("AAAAAAAAAHHHHHHHHHHH!!!!!!!")
