import pyb

##########################################################################
#                       Pulse Width Modulation                           #
#                                                                        #
##########################################################################
class PulseGenerator:
    def __init__(self, channel=1, pin_name='A0', duty_cycle=0.5, timer=None,
                 prescaler=40000, period=500, tim=2):
        self.channel = channel
        self.pin = pyb.Pin(pin_name)
        self.duty_cycle = duty_cycle

        if timer is None:
            self.timer = pyb.Timer(tim, prescaler=prescaler, period=period)

        elif type(timer) == pyb.Timer:
            self.timer = timer 
        

    def set(self):
        self.pulse_width = int(self.timer.period() * self.duty_cycle)
        self.ch = self.timer.channel(self.channel, pyb.Timer.PWM, pin=self.pin)
        self.ch.pulse_width(self.pulse_width)

def shutdown():
    pass 


def feedback_loop(qcl_current, shunt_resistor=0.05, gain=10, vref=3.):
    vf = qcl_current * shunt_resistor
    adc_value = vf/vref * 4095
    measured_current = adc_value/2047 * qcl_current

    if not is_safe(qcl_current=qcl_current, measured_current=measured_current):
        shutdown()



def is_safe(qcl_current=qcl_current, measured_current=measured_current, tolerance=0.1):
    if measured_current >= qcl_current-tolerance and measured_current <= qcl_current+tolerance:
        return True

    else:
        return False 








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