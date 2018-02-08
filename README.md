# Capstone

Accessing the board

`$ picocom /dev/ttyACM1`


Turn Led on GPIO

```python
green_led = pyb.Pin('D12', pyb.Pin.OUT_PP)
green_led.value(1)
```

```python
dir(pyb.Pin.board)
dir(pyb.Pin.cpu) 
```