# Capstone - Quantum Cascade Laser Driver

## Installing MicroPython on STM32F4-Discovery

**Software needed on the host (Ubuntu)**

To compile Micro Python, the `arm-none-eabi` cross-compiler is needed. On newer Ubuntu versions this could be easily installed through apt:

    $ sudo apt-get install gcc-arm-none-eabi

Also you will need the [stlink](https://github.com/texane/stlink) utility from texane. For more details on how to install stlink, please consult texane’s [README](https://github.com/texane/stlink/blob/master/README).

To download the ELF firmware, you will also need the GDB for arm-none-eabi. In theory this could be done by the following apt statement:

    $ sudo apt-get install gdb-arm-none-eabi libnewlib-arm-none-eabi

But unfortunately if you have installed any other gdb already (which is likely), this command will fail due a conflicting manpage! Thus, the following work-around is needed:

    $ sudo apt-get install -d gdb-arm-none-eabi
    $ sudo dpkg -i --force-overwrite /var/cache/apt/archives/gdb-arm-none-eabi_VERSION_amd64.deb

Change VERSION to your `gdb-arm-none-eabi` version. 

### Building Micro Python for the Discovery

Clone the Micro Python git repository:

    $ git clone https://github.com/micropython/micropython.git

Now change into the micropython directory and build for the STM32F4-Discovery:

    $ cd micropython
    $ cd ports/stm32
    $ make BOARD=STM32F4DISC

This should create the firmware.elf in `stm32/build-STM32F4DISC`.

### Flash the Micro Python firmware to the Discovery

Connect the Discovery through USB (the one on with the Mini-B connector, don’t connect the USB-OTG), then start (in a separate terminal) the stlinkt utilit:

    $ st-util

The `st-util` now waits for a connection from GDB. This is done like so (assuming you are still in the `micropython/ports/stm32` directory):

    $ arm-none-eabi-gdb build-STM32F4DISC/firmware.elf

Within GDB connect to st-util by:

    target extended localhost:4242

And flash the firmware with:

    load

The multi-color COM-LED should blink while loading. After downloading finised, terminate GDB.

Now disconnect the USB Mini-B cable to power the board completely off.  Connect a USB-OTG on the opposite side, and reconnect the USB Mini-B cable for power. After a few seconds, the STM should be mounted as a storage device showing the files `boot.py` and `main.py`. It is also possible to open a Python shell on the serial device `/dev/ttyACM0` or `/dev/ttyACM1`:

    $ screen /dev/ttyACM1


## Creating development environment


#### Step 1: Install a [Miniconda](http://conda.pydata.org/miniconda.html) (or [Anaconda](https://www.continuum.io/downloads) environment)

-----------------------------------------------------------------

Any Linux, Mac OS X, or Windows computer should be suitable.

If you don't already have conda on your machine, you can get it from [Miniconda](http://conda.pydata.org/miniconda.html), by opening a terminal window and 

##### Download Miniconda

    # for linux
    $ wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh

    # for osx
    $ wget https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -O miniconda.sh

    # for windows
    # go to: https://conda.io/miniconda.html

##### Install Miniconda

    $ bash miniconda.sh
    # follow instructions

#### Step 2: Clone beyond-matplotlib-tutorial-sea-2018 git repo

    git clone https://github.com/andersy005/capstone.git

#### Step 3: Then `cd` to the capstone folder and create a separate Conda environment to work in for this tutorial

    cd capstone
    conda env update

This downloads all of the dependencies and then all you have to is:

    source activate capstone

(omitting "source" if you are on Windows).



