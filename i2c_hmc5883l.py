import math
import smbus
from time import *
from math import *

class MagnetometerAxes:
	
	def __init__(self, hmc5883l, x, y, z):
		self.raw_x = x
		self.raw_y = y 
		self.raw_z = z
		
		self.scaled_x = 0
		self.scaled_y = 0
		self.scaled_z = 0

		self.scale = hmc5883l.scale
		self.calculateScaled()
		
		self.declination = 0

	# Used primarily for debugging
	def printAxes(self):
		print "Raw X: "+str(int(self.raw_x))
		print "Raw Y: "+str(int(self.raw_y))
		print "Raw Z: "+str(int(self.raw_z))
		
		print "Twos Complement X:"+str(self.twosToInt(self.raw_x, 16))
		print "Twos Complement Y:"+str(self.twosToInt(self.raw_y, 16))
		print "Twos Complement Z:"+str(self.twosToInt(self.raw_z, 16))
		
		print "Scale X: "+str(self.scaled_x)
		print "Scale Y: "+str(self.scaled_y)
		print "Scale Z: "+str(self.scaled_z)
		
	def calculateScaled(self):
		# Insure first 4 bits 0, 12 bit two's complement, range
		int_x = self.twosToInt(self.raw_x, 16)
		int_y = self.twosToInt(self.raw_y, 16)
		int_z = self.twosToInt(self.raw_z, 16)
		
		if (int_x == -4096):
			self.scaled_x = None
		else:
			self.scaled_x = int_x * self.scale
			
		if (int_y == -4096):
			self.scaled_y = None
		else:
			self.scaled_y = int_y * self.scale
			
		if (int_z == -4096):
			self.scaled_z = None
		else:
			self.scaled_z = int_z * self.scale
			
	def setDeclination(self, degree, min = 0):
		self.declination = (degree+min/60) * (math.pi/180)
		
	# Returns heading in degrees and fraction of a minute
	def getHeading(self):
		headingRad = math.atan2(self.scaled_y, self.scaled_x)
		headingRad += self.declination
		
		# Correct for reversed heading
		if(headingRad < 0):
			headingRad += 2*math.pi
			
		# Check for wrap and compensate
		if(headingRad > 2*math.pi):
			headingRad -= 2*math.pi
			
		# Convert to degrees from radians
		headingDeg = headingRad * 180/math.pi
		
		return headingDeg
	
	def printHeading(self):
		heading = self.getHeading()
		headingDeg = int(math.floor(heading))
		headingMin = int(math.floor((heading - headingDeg) * 60))
		print str(headingDeg)+u"\u00b0 "+str(headingMin)+"'"
		
		
	def twosToInt(self, val, len):
		# Convert twos compliment to integer
		if(val & (1 << len - 1)):
			val = val - (1<<len)
		return val

class i2c_hmc5883l:
	
	ConfigurationRegisterA = 0x00
	ConfigurationRegisterB = 0x01
	ModeRegister = 0x02
	AxisXDataRegisterMSB = 0x03
	AxisXDataRegisterLSB = 0x04
	AxisZDataRegisterMSB = 0x05
	AxisZDataRegisterLSB = 0x06
	AxisYDataRegisterMSB = 0x07
	AxisYDataRegisterLSB = 0x08
	StatusRegister = 0x09
	IdentificationRegisterA = 0x10
	IdentificationRegisterB = 0x11
	IdentificationRegisterC = 0x12
	

	MeasurementContinuous = 0x00
	MeasurementSingleShot = 0x01
	MeasurementIdle = 0x03
	
	def __init__(self, port, addr=0x1e, gauss=1.3):
		self.addr = addr
		self.bus = smbus.SMBus(port)
		
		self.scale = 0
		self.setScale(gauss)
		
	def readAxes(self):
		
		# X Axis
		msb = self.bus.read_byte_data(self.addr, self.AxisXDataRegisterMSB)
		x_raw = (msb << 8) | self.bus.read_byte_data(self.addr, self.AxisXDataRegisterLSB)
		
		# Z Axis
		msb = self.bus.read_byte_data(self.addr, self.AxisZDataRegisterMSB)
		z_raw = (msb << 8) | self.bus.read_byte_data(self.addr, self.AxisZDataRegisterLSB)
		
		# Y Axis
		msb = self.bus.read_byte_data(self.addr, self.AxisYDataRegisterMSB)
		y_raw = (msb << 8) | self.bus.read_byte_data(self.addr, self.AxisYDataRegisterLSB)
	
		return MagnetometerAxes(self, x_raw, y_raw, z_raw)
	
	def setContinuousMode(self):
		self.bus.write_byte_data(self.addr, self.ModeRegister, self.MeasurementContinuous)
		
	def setScale(self, gauss):
		if gauss == 0.88:
			self.scale_reg = 0x00
			self.scale = 0.73
		elif gauss == 1.3:
			self.scale_reg = 0x01
			self.scale = 0.92
			print self.scale
		elif gauss == 1.9:
			self.scale_reg = 0x02
			self.scale = 1.22
		elif gauss == 2.5:
			self.scale_reg = 0x03
			self.scale = 1.52
		elif gauss == 4.0:
			self.scale_reg = 0x04
			self.scale = 2.27
		elif gauss == 4.7:
			self.scale_reg = 0x05
			self.scale = 2.56
		elif gauss == 5.6:
			self.scale_reg = 0x06
			self.scale = 3.03
		elif gauss == 8.1:
			self.scale_reg = 0x07
			self.scale = 4.35
		
		self.scale_reg = self.scale_reg << 5
		self.bus.write_byte_data(self.addr, self.ConfigurationRegisterB, self.scale_reg)
		
	