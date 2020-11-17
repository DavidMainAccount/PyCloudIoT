On a separate repository: https://github.com/DavidMainAccount/PyCloudIoT-generate-firmware

As we are aiming to make some complex calculus with micropython using an specific external library (ulab) that you can find at: https://github.com/v923z/micropython-ulab , we are obliged to make our own version of micropython firmware per kind of node. In this first version, we will focus on the esp32 boards. 

# Create ESP32 custom firmware
To begin, create a folder called Micropython inside this folder. Inside /Micropython we will create a specific folder per kind of board. Then a subfolder called esp32.

Inside esp32, clone the micropython official repository: https://github.com/micropython/micropython/. Go to the /micropython/ports/esp32 folder and execute **make**. This will give us an output like:

```
Use make V=1 or set BUILD_VERBOSE in your environment to increase build verbosity.
The ESPIDF variable has not been set, please set it to the root of the esp-idf repository.
See README.md for installation instructions.
Supported git hash: 3ede9f011b50999b0560683f9419538c066dd09e
Makefile:34: *** ESPIDF not set.  Stop.
```

We will then retain the supported git hash for the following installs. Go back to Micropython/esp32 and clone the official esp-idf repository: git clone https://github.com/espressif/esp-idf.git then get inside the folder.

Checkout (git checkout ...) to the git hash returned before. And run **git submodule update --init** to install the dependencies.

After that, we need to download a cross-compiler. Install the cross compiler dependencies: **sudo apt-get install git wget make libncurses-dev flex bison gperf python python-serial** and download the cross compiler **wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz**. Then extract his files at a new folder at: Micropython/esp32/esp/. To extract the files go to the folder and run **tar -zxvf ../xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz**.
Finally export the cross compiler path: 
**export PATH=/home/username/Micropython/esp32/esp/xtensa-esp32-elf/bin:$PATH** .

Go back now to the folder Micropython/esp32/micropython/ports/esp32. Here inside, we need to create a makefile to overwrite some important values from the already pressent makefile

``` /Micropython/esp32/micropython/ports/esp32/makefile

ESPIDF = /home/username/Micropython/esp32/esp-idf
#PORT = /dev/ttyUSB0
#FLASH_MODE = qio
#FLASH_SIZE = 4MB
#CROSS_COMPILE = xtensa-esp32-elf-
 
include Makefile

```

Go back to the micropython folder then execute:

**git submodule update --init**

Next we need to do the cross-compiler build. To do so, we will execute: 

```
make -C mpy-cross
git submodule init lib/berkeley-db-1.xx
git submodule update
```

Then, we will download the external ulab library. And put it at: /Micropython/esp32/ulab. 

Finally go back to Micropython/esp32/micropython/ports/esp32 and comment one lane on the original Makefile (because of ulab compatibilities): 

```
$(OBJ_MP): CFLAGS += -Wdouble-promotion -Wfloat-conversion
```

Finally, we run **make USER_C_MODULES=../../../ulab** to build the new firmware. This will build your firmware at build-GENERIC/firmware.bin. Then you can use put it on the /configuration/firmware folder and run use it to flash your boards (already done with the scripts using esptool).

# credits:
https://www.microdev.it/wp/en/2018/08/08/esp32-micropython-compiling-for-esp32/
https://github.com/micropython/micropython/tree/master/ports/esp32
https://github.com/micropython/micropython/tree/master/ports/esp32


# Firmawre without esp-32
You can also use a firmware that does not have ulab. In this case, simply chose the esp-32... firmware on the upload script.