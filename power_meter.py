#!/usr/bin/python

# Header

# License

# A command-line program for outputting the current battery state visually.
# Copyright (C) 2011  Sean Kelleher
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Imports
from __future__ import division
import getopt
import sys

# Constants
DEFAULT_SIZE = 10
FULL_SYMBOL  = '='
EMPTY_SYMBOL = ' '
CONFIG_FILE  = 'voltages'

GETOPT_ERROR_CODE = 0

def get_max_power(cfile=CONFIG_FILE):
    """Gets the maximum recorded power of the battery."""
    with open(cfile, 'r') as file:
        maxpower = int(file.readline().strip())
        return maxpower

def get_cur_power():
    """Gets the current power of the battery."""
    with open('/proc/acpi/battery/BAT0/state', 'r') as file:
        cont = file.read() # Because it's made on-the-fly
        for line in cont.split('\n'):
            if line.startswith('remaining capacity:'):
                curcur  = extract_magnitude(line, 4)
            if line.startswith('present voltage:'):
                curvolt = extract_magnitude(line, 3)
    return curcur * curvolt

def extract_magnitude(line, unitlen):
    """Extracts the magnitude of a rating from a line in a linux battery file.

    Keyword arguments:
    'line'    -- the line to extract the magnitude from
    'unitlen' -- how much of the end of the line the units take up
    """
    i   = line[:-unitlen].rindex(' ') + 1
    mag = int(line[i:-unitlen])
    return mag

def set_max_power(maxpower, cfile=CONFIG_FILE):
    """Sets the highest recoded power value."""
    with open(cfile, 'w') as file:
        file.write(str(maxpower))

def usage():
    print """Linux Power Meter command-line utility

    -h, --help      Print this
    -s, --size=     Specify the character size of the graph
    """
    sys.exit()

if '__main__' == __name__:
    numeric = False
    size = DEFAULT_SIZE

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hns:',
                                   ["help", "numeric", "size="])
    except getopt.GetoptError:
        sys.stderr.write("Error parsing command options")
        sys.exit(getoptErrorCode)

    for opt, value in opts:
        if opt in ("-h", "--help"): usage()
        elif opt in ("-n", "--numeric"): numeric = True
        elif opt in ("-s", "--size"): size = int(value)
        else: usage()

    maxpow = get_max_power()
    curpow = get_cur_power()
    if curpow > maxpow:
        maxpow = curpow
        set_max_power(maxpow)
    percent = curpow / maxpow
    if numeric:
        print "\t%.2f %%" % (percent * 100)
    else:
        percent = int(percent * size)
        f = FULL_SYMBOL  * percent
        e = EMPTY_SYMBOL * (size - percent)
        print "[%s%s]" % (f,e)
