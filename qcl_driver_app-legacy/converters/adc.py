import pyb 

# Create an analog object from a pin
pin = pyb.Pin('C1')
adc = pyb.ADC(pin)

# Read an analog value 
val = adc.read()