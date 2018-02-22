import pyb
TIM = 2
PRESCALER = 40000
PERIOD = 500

##########################################################################
#                       Pulse Width Modulation                           #
#                                                                        #
##########################################################################


# Initialize pins
def init_pin(pin_name='A0', mode=pyb.Pin.OUT_PP):
    """[summary]

    Keyword Arguments:
        mode {[type]} -- [description] (default: {pyb})

    Returns:
        [type] -- [description]
    """

    pin = pyb.Pin(pin_name, mode)
    return pin


# Create and initialize timer object
timer = pyb.Timer(TIM, prescaler=PRESCALER, period=PERIOD)


# We will now configure the timer to generate 80% impulses
def pulse_generator(timer, channel=1, pin=None, duty_cycle=1.0):

    pulse_width = int(timer.period() * duty_cycle)
    ch = timer.channel(channel, pyb.Timer.PWM, pin=pin,
                       pulse_width=pulse_width)
    return ch


pin = init_pin()
ch = pulse_generator(timer, pin=pin, duty_cycle=0.5)


##########################################################################
#                       Digital to Analog Converter (DAC)                #
#                                                                        #
##########################################################################
