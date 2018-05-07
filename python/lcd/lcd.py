#!/usr/bin/python3

# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Diplay a two line message on Raspberry Pi LCD display using PiFaceCAD.
Useful for printing some debugging messages if your Pi is not connected
to the monitor.
Usage: python lcd.py line1 line2
"""

import pifacecad
import sys

cad = pifacecad.PiFaceCAD()
if len(sys.argv) == 1:
    cad.lcd.clear()
    exit(0)

if len(sys.argv) > 1:
    cad.lcd.set_cursor(0, 0)
    cad.lcd.write(sys.argv[1])

if len(sys.argv) > 2:
    cad.lcd.set_cursor(0, 1)
    cad.lcd.write(sys.argv[2])
