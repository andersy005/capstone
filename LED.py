import pyb 
green_led = pyb.Pin('D12', pyb.Pin.OUT_PP)
green_led.value(1)
green_led.value(0)