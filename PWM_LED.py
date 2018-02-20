# main.py -- put your code here!
import pyb 

# Initialize pins
# on the STM32F4DISC the main LEDS are connected to pins
# PD12-PD15 having channesl 1-4 of timer 4 as the alternate
# function #2
led1 = pyb.Pin('D12')
led2 = pyb.Pin('D13')
led3 = pyb.Pin('D14')
led4 = pyb.Pin('D15')
led1.on()
led2.on()
led3.on()
led4.on()

# create an analog object from a pin
pin = pyb.Pin('C1')
adc = pyb.ADC(pin)

# Create and initialize timer object at timer 4
# Set up the timer so that it starts counting
# We will configure it to count upwards with a period
# of 500 and the prescaler set to 40000	
timer = pyb.Timer(4, prescaler=40000, period=500)

	  
# We will now configure the timer to generate 80% impulses
# on LED1 connected to D12 (i.e active 4/5 of the period and 
# inactive for the next 1/5). This is done by configuring 
# the channel 1 in the PWM mode with a compare value of 
# 400 (out of period 500)
ch1 = timer.channel(1, pyb.Timer.PWM, pin=led1, pulse_width=400)

while True:

	val = int(adc.read())
    print(val)

    # we can easily configure the timer to generate pulse signal on
	# another channel. The period will have to be the same, however
	# the compare value (pulse_width) can be different. 
	# In this case we will configure the timer to generate 20% impulses
	# on LED2 (i.e active 1/5 of the period and inactive for the next 4/5)
	# This is done by configuring the channel 2 in the PWM mode with a compare 
	# value of 100 (out of period 500)
	ch2 = timer.channel(2, pyb.Timer.PWM, pin=led2, pulse_width=val)