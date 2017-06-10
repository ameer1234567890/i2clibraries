from i2clibraries import i2c_hmc5883l

hmc5883l = i2c_hmc5883l.i2c_hmc5883l(0)

hmc5883l.setContinuousMode()
hmc5883l.setDeclination(9,54)

# To get string of degrees and minutes
heading = hmc5883l.getHeadingString()
