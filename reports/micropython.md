# What is MicroPython?

MicroPython is a tiny open source Python programming language interpreter that runs on small embedded development boards.  With MicroPython you can write clean and simple Python code to control hardware instead of having to use complex low-level languages like C or C++. 

# Why MicroPython?

The simplicity of the Python programming language makes MicroPython an excellent choice for beginners who are new to programming and hardware.  However MicroPython is also quite full-featured and supports most of Python's syntax. 

Beyond its ease of use MicroPython has some unique features that set it apart from other embedded systems:

- **Interactive REPL, or read-evaluate-print loop.**  This allows you to connect to a board and have it execute code without any need for compiling or uploading--perfect for quickly learning and experimenting with hardware!
- **Extensive software library.**  Like the normal Python programming langauge MicroPython is 'batteries included' and has libraries built in to support many tasks.  For example parsing JSON data from a web service, searching text with a regular expression, or even doing network socket programming is easy with built-in libraries for MicroPython.
- **Extensibility.**  For advanced users MicroPython is extensible with low-level C/C++ functions so you can mix expressive high-level MicroPython code with faster low-level code when you need it.

# What Can MicroPython do?

Almost anything you can imagine! MicroPython can control hardware and connected devices.  You can control GPIO pins to blink lights, read switches, and more.  You can drive PWM outputs for servos, LEDs, etc. or read analog sensors with an analog to digital converter.  Talking to I2C or SPI devices is easy too,and you'll even find network & WiFi support. 

# What Can't MicroPython do?

One thing to realize is that MicroPython code isn't as fast and might use a little more memory compared to other low-level C/C++-based code.  Usually this doesn't matter since the speed and memory differences are small and don't impact most normal uses.

However the code which has tight timing or performance requirements might not work in MicroPython.  However there are ways to mix both MicroPython and low-level C/C++ code so you can have the best of both worlds--your main logic in clean and easy to understand MicroPython code, and performance critical parts written in faster low-level code.


# References

- MicroPython homepage (http://micropython.org/)
- MicroPython Documentation (http://docs.micropython.org/en/latest/pyboard/)