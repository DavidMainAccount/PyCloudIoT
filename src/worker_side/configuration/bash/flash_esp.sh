#!/bin/bash

function check_success  {
    if [ $? -eq 0 ]; then
        echo -e "\e[32mDONE: $1 \e[0m"
    else
        echo -e "\e[31m***ERROR: Couldnt $1 \e[0m"
        echo -e "\e[31mCheck flash_logs.txt for further information.\e[0m"
        exit
    fi
}

port=$1 #/dev/ttyUSB0
firmware_with_path=$2 #../firmware/esp32-20190401-v1.10-258-g83f3c29d3.bin

echo "**************"
echo "Chosen port: " $port
echo "Uploading firmware at: " $firmware_with_path
echo "**************"

#Install ESPTOOL
echo "=> Upgrading/installing esptool"
pip install --upgrade esptool &>flash_logs.txt
check_success "Install/upgrade esptool"

# Formatage de la carte connectée sur port
echo "=> Erasing flash from board"
esptool.py --chip esp32 -p $port erase_flash &>>flash_logs.txt
check_success "Erase flash"

#Install Mycropython ESP32
echo "=> Flashing new firmware"
esptool.py --chip esp32 -p $port write_flash -z 0x1000 $firmware_with_path &>>flash_logs.txt
check_success "Flash board"

#uploading the program
chmod +x upload.sh
./upload.sh
