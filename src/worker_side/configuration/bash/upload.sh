#!/bin/bash

function check_success  {
    if [ $? -eq 0 ]; then
        echo -e "\e[32mDONE: $1 \e[0m"
    else
        echo -e "\e[31m***ERROR: Couldnt $1 \e[0m"
        echo -e "\e[31mCheck upload_logs.txt for further information.\e[0m"
        exit
    fi
}

port=$1 #/dev/ttyUSB0

#Upload files
echo -ne 'Puting Files : #                                       (0%)\r'
ampy --port $port put ../../src/Libraries &>upload_logs.txt
check_success "Put /Libraries"
echo -ne 'Puting Files : ##################                     (50%)\r'
ampy --port $port put ../../src/main.py &>>upload_logs.txt
check_success "Put /main.py"
echo -ne 'Puting Files : ##############################         (80%)\r'
ampy --port $port put ../../src/Results &>>upload_logs.txt
check_success "Put /Results"
echo -ne 'Puting Files : ##################################     (90%)\r'
ampy --port $port put ../../src/Scripts &>>upload_logs.txt
check_success "Put /Scripts"
echo -ne 'Puting Files : ######################################(100%)\r'
echo -ne '\n'

ampy --port $port reset
