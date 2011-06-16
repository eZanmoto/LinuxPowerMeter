#!/usr/bin/python

# Header

# License

# A command-line program for outputting the current battery state visually.
# Copyright (C) 2011  Seán Kelleher
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
from sys import argv

# Constants
DEFAULT_SIZE = 10
FULL_SYMBOL  = '='
EMPTY_SYMBOL = ' '
CONFIG_FILE  = 'voltages'

if '__main__' == __name__:
    size = int(argv[1]) if len(argv) > 1 else DEFAULT_SIZE
    with open(CONFIG_FILE, 'r') as file:
        batfile = file.readline().strip()
        maxvolt = int(file.readline().strip())
    with open(batfile, 'r') as file:
        i = file.read() # Because it's made on-the-fly
        # FIXME: Should be checking amps instead of volts
        j = i[:-4].rindex(' ') + 1
        curvolt = int(i[j:-4])
    if curvolt > maxvolt:
        maxvolt = curvolt
        with open(CONFIG_FILE, 'w') as file:
            file.write(str(curvolt))
    percent = int((curvolt/maxvolt)*size)
    f = FULL_SYMBOL  * percent
    e = EMPTY_SYMBOL * (size-percent)
    print "[%s%s]" % (f,e)
