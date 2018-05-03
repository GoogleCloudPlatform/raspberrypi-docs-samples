// Copyright 2018 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

/** @fileoverview This script can be run on Raspberry Pi (as well as on any
 * other Linux system with ALSA sound). It will do the following:
 * - record audio of length `recordLength` ms and save it into `input.wav`,
 * - send this file to Google Cloud Speech-To-Text API for recognition,
 * - send the resulting text to Google Cloud Text-To-Speech API to convert it
 *   back into speech, saving the result to `output.wav`,
 * - play the resulting file.
 *
 * Right now it uses simple wrappers `record.sh` and `play.sh` that wrap
 * `arecord` and `aplay`, but can be changed to use ALSA directly (e.g. using
 * the `alsa` NPM module).
 *
 * To make the script work, you need to point environment variable
 * GOOGLE_APPLICATION_CREDENTIALS to the JSON service account key for the Google
 * Cloud Speech service.
 */

const textToSpeech = require('@google-cloud/text-to-speech');
const speech = require('@google-cloud/speech');
const fs = require('fs');
const util = require('util');
const writeFile = util.promisify(fs.writeFile);
const readFile = util.promisify(fs.readFile);
const {spawn} = require('child_process');

const recordLength = 5000;

/** Wait for a key pressed on the keyboard.
 */
async function keypress() {
  process.stdin.setRawMode(true);
  return new Promise(resolve =>
    process.stdin.once('data', () => {
      process.stdin.setRawMode(false);
      resolve();
    })
  );
}

/** Record sound for `delay` ms and save it into `filename`.
 * @param {string} filename Filename (WAV) to save the sound into.
 * @param {Number} delay Delay, in milliseconds.
 * @returns {Promise} Resolves when done.
 */
async function recordSound(filename, delay) {
  return new Promise(resolve => {
    const process = spawn('./record.sh', [filename]);
    process.on('close', resolve);
    setTimeout(() => {
      process.kill('SIGTERM');
    }, delay);
  });
}

/** Plays sound from the given file.
 * @param {string} filename Filename (WAV) to play the sound from.
 * @returns {Promise} Resolves when done.
 */
async function playSound(filename) {
  return new Promise(resolve => {
    const process = spawn('./play.sh', [filename]);
    process.on('close', resolve);
  });
}

/** Converts text into speech.
 * @param {string} text A text to say.
 * @param {outputFile} text Filename (WAV) to save the result.
 */
async function runTextToSpeech(text, outputFile) {
  const client = new textToSpeech.TextToSpeechClient();

  const request = {
    input: {text: text},
    voice: {languageCode: 'en-US', ssmlGender: 'FEMALE'},
    audioConfig: {audioEncoding: 'LINEAR16'},
  };

  let response = await client.synthesizeSpeech(request);
  await writeFile(outputFile, response[0].audioContent, 'binary');
}

/** Converts speech to text.
 * @param {inputFile} Filename of a WAV file to recognize.
 * @returns {string} Recognized text.
 */
async function runSpeechToText(inputFile) {
  const client = new speech.SpeechClient();

  const encoding = 'LINEAR16';
  const languageCode = 'en-US';
  const config = {
    encoding: encoding,
    languageCode: languageCode,
  };

  let buffer = await readFile(inputFile);

  const audio = {
    content: buffer.toString('base64'),
  };
  const request = {
    config: config,
    audio: audio,
  };

  let data = await client.recognize(request);
  let response = data[0];
  let transcription = response.results
    .map(result => result.alternatives[0].transcript)
    .join('\n');
  return transcription;
}

/** Main function.
 */
async function main() {
  let inputFile = 'input.wav';
  let outputFile = 'output.wav';
  for (;;) {
    console.log('Say something');
    await recordSound(inputFile, recordLength);
    let transcription = await runSpeechToText(inputFile);
    console.log('I heard:', transcription);
    await runTextToSpeech(transcription, outputFile);
    await playSound(outputFile);
    console.log('Press any key to continue...');
    await keypress();
  }
}

main().catch(err => {
  console.log('ERROR:', err);
});
