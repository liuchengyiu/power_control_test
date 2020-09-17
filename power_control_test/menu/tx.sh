#!/bin/bash
com0="/dev/ttyACM0"
com1="/dev/ttyACM1"
com2="/dev/ttyACM2"
com3="/dev/ttyACM3"
while :
do
    echo -e -n "\x11\x22\x33\x44\x55\x66" > $com0
    echo -e -n "\x11\x22\x33\x44\x55\x66" > $com1
    echo -e -n "\x11\x22\x33\x44\x55\x66" > $com2
    echo -e -n "\x11\x22\x33\x44\x55\x66" > $com3
    sleep 1s
done