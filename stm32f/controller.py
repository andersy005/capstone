import pyb

##########################################################################
#                       Pulse Width Modulation                           #
#                                                                        #
##########################################################################
class PulseGenerator:
    def __init__(self, channel=1, pin_name='A0', duty_cycle=0.5, timer=None,
                 prescaler=40000, period=500, tim=2, freq=1000):
        self.channel = channel
        self.pin = pyb.Pin(pin_name)
        self.duty_cycle = duty_cycle

        if timer is None:
            #self.timer = pyb.Timer(tim, prescaler=prescaler, period=period)
	    self.timer = pyb.Timer(tim, freq=freq)

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



def is_safe(qcl_current, measured_current, tolerance=0.1):
    if measured_current >= qcl_current-tolerance and measured_current <= qcl_current+tolerance:
        return True

    else:
        return False 

