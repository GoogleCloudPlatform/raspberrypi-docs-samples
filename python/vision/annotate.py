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
Takes an image from the RaspiCam attached to your Raspberry Pi, sends it to
Google Cloud Vision API for annotation and displays the result on the LCD
display attached to your Raspberry Pi.

Required hardware:
- Raspberry Pi
- RaspiCam https://www.raspberrypi.org/products/camera-module-v2/
- LCD screen http://www.piface.org.uk/products/piface_control_and_display/

The script requires a service account key for the Google Cloud Vision API
to be downloaded in JSON format and put in `keyfile.json` near the script.
"""

import io
import os
import picamera
import pifacecad
import time
import sys

from google.cloud import vision
from google.cloud.vision import types

# Configuration
basedir = os.path.dirname(os.path.abspath(__file__))
apikey = os.path.join(basedir, "keyfile.json")
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = apikey
lcd_lines = 2
pin_count = 5
file_dir = os.path.join(basedir, "snap")
display = False

# End of configuration


class Annotator:
    def __init__(self):
        self.client = vision.ImageAnnotatorClient()
        self.cad = pifacecad.PiFaceCAD()
        self.listener = pifacecad.SwitchEventListener(chip=self.cad)
        self.camera = picamera.PiCamera()

    def start(self):
        self.is_prompt = True
        for i in range(pin_count):
            self.listener.register(i, pifacecad.IODIR_FALLING_EDGE,
                                   lambda event: self.pin_event_handler(event))
        self.listener.activate()
        self.reset_screen()

    def stop(self):
        self.listener.deactivate()

    def get_picture_from_camera(self, filename):
        self.camera.capture(filename)

    def pin_event_handler(self, event):
        if self.is_prompt:
            self.annotate_picture()
            self.is_prompt = False
        else:
            self.reset_screen()
            self.is_prompt = True

    def annotate_picture(self):
        if display:
            os.system("killall display > /dev/null 2>&1")

        self.cad.lcd.clear()
        self.cad.lcd.backlight_on()
        self.cad.lcd.write('Snap!')

        try:
            os.stat(file_dir)
        except:
            os.mkdir(file_dir)

        filename = os.path.join(file_dir, str(time.time()) + ".jpg")
        self.get_picture_from_camera(filename)

        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()
        self.cad.lcd.write('Wait...')

        with io.open(filename, "rb") as image_file:
            content = image_file.read()
        image = types.Image(content=content)
        response = self.client.label_detection(image=image)
        labels = response.label_annotations

        self.cad.lcd.clear()
        self.cad.lcd.backlight_on()
        lineno = 0
        for label in labels:
            if lineno >= lcd_lines:
                break
            self.cad.lcd.set_cursor(0, lineno)
            self.cad.lcd.write(label.description)
            lineno += 1

        if display:
            os.system("display -resize 1024x768 \"%s\" > /dev/null 2>&1 &" %
                      (filename))

    def reset_screen(self):
        self.cad.lcd.clear()
        self.cad.lcd.backlight_off()
        self.cad.lcd.write('Press any button')
        self.cad.lcd.set_cursor(0, 1)
        self.cad.lcd.write('to take a photo')


def main():
    annotator = Annotator()
    annotator.start()
    input("Press Pi button to take a picture, or Enter to stop. ")
    annotator.stop()


main()
