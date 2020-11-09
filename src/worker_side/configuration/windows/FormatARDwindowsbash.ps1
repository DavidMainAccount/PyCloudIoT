#!/bin/bash

python get-pip-windows.py

#Install ESPTOOL
pip install --upgrade esptool
Write-Host 'Installing : ######                     (33%)\r'

# Formatage de la carte connectée sur COM4
esptool --chip esp32 -p COM4 erase_flash
Write-Host 'Installing : ##############             (66%)\r'

#Install Mycropython ESP32
esptool --after hard_reset --chip esp32 -p COM4 write_flash -z 0x1000 ../firmware/esp32-20190401-v1.10-258-g83f3c29d3.bin
Write-Host 'Installing : ####################   (100%)\r'
Write-Host '\n'