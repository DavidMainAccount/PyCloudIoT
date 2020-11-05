#!/bin/bash

#Install ESPTOOL
pip install --upgrade esptool
echo -ne 'Installing : ######                     (33%)\r'

# Formatage de la carte connectée sur ttyUSB0
esptool.py --chip esp32 -p /dev/ttyUSB0 erase_flash
echo -ne 'Installing : ##############             (66%)\r'

#Install Mycropython ESP32
esptool.py --chip esp32 -p /dev/ttyUSB0 write_flash -z 0x1000 ../firmware/esp32-20190401-v1.10-258-g83f3c29d3.bin
echo -ne 'Installing : ####################   (100%)\r'
echo -ne '\n'

#uploading the program
chmod +x upload.sh
./upload.sh
