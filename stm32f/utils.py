
import pyb


class PulseGenerator:
    def __init__(self,
                 channel=1,
                 pin_name='A0',
                 duty_cycle=0.5,
                 timer=None,
                 freq=500,
                 tim=2):
        """ Generate a pulse width modulated signal on given pin
                 
                 Keyword Arguments:
                     channel {int} -- PWM channel to use (default: {1})
                     pin_name {str} -- pin name to use (default: {'A0'})
                     duty_cycle {float} -- fraction of time the signal is on (default: {0.5})
                     timer {[pyb.Timer]} -- a timer object (default: {None})
                     freq {int} -- frequency for PWM (default: {500})
                     tim {int} -- timer to use (default: {2})
        """

        self.channel = channel
        self.pin = pyb.Pin(pin_name)
        self.duty_cycle = duty_cycle
        self.freq = freq
        self.tim = tim 

        if timer is None:
            self.timer = pyb.Timer(tim, freq=self.freq)

        elif type(timer) == pyb.Timer:
            self.timer = timer

    def set(self):

        """Set the pulse width for the PWM signal
        """

        self.pulse_width = int(self.timer.period() * self.duty_cycle)
        self.ch = self.timer.channel(self.channel, pyb.Timer.PWM, pin=self.pin)
        self.ch.pulse_width(self.pulse_width)
