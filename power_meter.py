#!/usr/bin/python

# Header
# Imports
from __future__ import division
from sys import argv

# Constants
DEFAULT_SIZE = 10
FULL_SYMBOL  = '='
EMPTY_SYMBOL = ' '

if '__main__' == __name__:
    size = int(argv[1]) if len(argv) > 1 else DEFAULT_SIZE
    with open('/proc/acpi/battery/BAT0/state', 'r') as file:
        i = file.read() # Because it's made on-the-fly
        j = i[:-4].rindex(' ') + 1
        curvolt = int(i[j:-4])
    with open('voltages', 'r') as file:
        maxvolt = int(file.readline())
        if curvolt > maxvolt:
            maxvolt = curvolt
    if curvolt == maxvolt:
        with open('voltages', 'w') as file:
            file.write(str(curvolt))
    percent = int((curvolt/maxvolt)*size)
    f = FULL_SYMBOL  * percent
    e = EMPTY_SYMBOL * (size-percent)
    print "[%s%s]" % (f,e)
