## Vision sample

This folder contains Python code that takes a picture from the attached
Raspberry Pi camera and sends it to [Google Cloud
Vision](https://cloud.google.com/vision/) API for annotation.
The result is printed on the LCD screen connected to your Raspberry Pi.

To use this sample, you'll need to have the following:
- Raspberry Pi with a
  [RaspiCam](https://www.raspberrypi.org/products/camera-module-v2/)-compatible
  camera.
- [PiFace](http://www.piface.org.uk/products/piface_control_and_display/)-compatible
  LCD screen.
- Google Cloud API JSON key that has access to Vision service. Point environment
  variable `GOOGLE_APPLICATION_CREDENTIALS` to the key file.

You need to install Python modules `picamera` and `pifacecad` to make the sample
work, but it's easy to change it to take a picture from some other source, and
report a result in some other way without writing to an LCD screen, if you don't
have one.

Enjoy!
