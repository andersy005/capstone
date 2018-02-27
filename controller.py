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

POWER_MAX = 72.
POWER_MIN = 65.
LASER_VOLTAGE = 20.
LASER_CURRENT = 3.6


def sanitize_power_input(power):
    """[summary]
    
    Arguments:
        power {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    # check lower and upper bound for the power
    if (power >= POWER_MIN) and (power <= POWER_MAX):
        return float(power)

    else:
        print('Input out of range. Setting the power to allowed minimum value of {}'.format(POWER_MIN))
        return float(POWER_MIN)


power = sanitize_power_input(70)
print('Power = {} W'.format(power))


def create_dac(power, dac_pin):
    """[summary]
    
    Arguments:
        power {[type]} -- [description]
        dac_pin {[type]} -- [description]
    """

    current = power / LASER_VOLTAGE
    dac_value = int((current / LASER_CURRENT) * 4095)
    print(dac_pin)
    print(current, dac_value)
    dac = pyb.DAC(dac_pin, bits=12)
    dac.write(dac_value)


def set_laser_voltage(dac_pin):
    """[summary]
    
    Arguments:
        dac_pin {[type]} -- [description]
    """

    volt = LASER_VOLTAGE / 10.
    dac_value = int(volt / 3. * 4095)
    print(dac_pin)
    print(volt, dac_value)
    dac = pyb.DAC(dac_pin, bits=12)
    dac.write(dac_value)

dac_pin1 = init_pin('A5', mode=pyb.Pin.ANALOG)
dac_pin2 = init_pin('A4', mode=pyb.Pin.ANALOG)

create_dac(power, dac_pin1)
set_laser_voltage(dac_pin2)