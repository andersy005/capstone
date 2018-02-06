# DAC: Digital Analog Converter

- The STM32F407 has a 12-bit digital-analog-converter (DAC) module with **two** independent output channels:
  - DAC1(pin PA4)
  - DAC2(pin PA5)

- The channels can be configured in 8-bit mode or 12-bit mode.
- The conversions can be done independently or simultaneously.
- Simultaneous mode can be used where two independent but synchronized signals must be generated. for e.g.the left and right channels of stereo audio.
- It is often important that the analog output is updated at precise instants, sometimes controlled by external hardware-thus the conversion process can be triggered by timers or external signals.
- A common use for DAC hardware is to **generate a time varying signal**. 
- Where the sample rate is high, it is impractical to control the conversion process entirely through **application software** or even **interrupt handlers**.
- Each DAC channel has **DMA**(Direct Memory Access) capability which can be controlled by the trigger signal.


**A simplified block diagram of one DAC channel**
![](https://i.imgur.com/evgewmD.png)

- Each channel has separate control logic which is configured through a single control register (CR).
- Data to be converted by channel x are written to data holding register (DHRx)
- In response to a trigger event, DHRx is transferred to the data output register (DORx) and after a settling time, the corresponding analog value appears at the output.
- The DAC output voltage is linear between $0$ and $V_{REF+}$ ($3.3$ V on the discovery board) and is defined by the following equation:

$$DACoutput = V_{REF+} \times \frac{DOR}{4095}$$