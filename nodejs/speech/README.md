## Speech sample

This folder contains Node.js code that records WAV file from the microphone,
sends it to [Google Cloud
Speech-To-Text](https://cloud.google.com/speech-to-text/) API for recognition,
then send the resulting text to [Google Cloud
Text-To-Speech](https://cloud.google.com/text-to-speech/) API for converting
back to WAV file, and plays the resulting file (basically, repeating what you
said, but using a Google Cloud Text-To-Speech voice).

To use this sample, you'll need to have the following:
- Raspberry Pi with a microphone and speaker. Actually, there is nothing
  specific to Raspberry Pi here, the code should work on any Linux with ALSA.
- Google Cloud API JSON key that has access to Speech service. Point environment
  variable `GOOGLE_APPLICATION_CREDENTIALS` to the key file.

Before running the code, make sure to install all the dependencies by running
```js
npm install
```

Enjoy!
