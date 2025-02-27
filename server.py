#!/usr/bin/env python3

import argparse
import queue
import sys
import sounddevice as sd
from vosk import Model, KaldiRecognizer
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import json
import logging
import time 

app = Flask(__name__)
socketio = SocketIO(app)

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


q = queue.Queue()
transcription_text = ""  # Variable to hold the latest transcription
partial_text_cache = "" # Cache to avoid sending redundant partial updates


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def callback(indata, frames, time_val, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        logger.error(f"Audio stream status: {status}")  # Log audio stream errors
    q.put(bytes(indata))


@app.route('/')
def index():
    return render_template('index.html', transcription=transcription_text)


@socketio.on('connect')
def handle_connect():
    print('Client Connected (Minimal Server)')  # Server-side log on connect
    emit('server_event', {'data': 'Minimal Server Connected'}) # Send event back


def transcribe_microphone(samplerate, device, model_lang):
    global transcription_text, partial_text_cache # Use the global variable

    try:
        if samplerate is None:
            device_info = sd.query_devices(device, "input")
            samplerate = int(device_info["default_samplerate"])
            logger.info(f"Samplerate set to device default: {samplerate}") # Log samplerate

        if model_lang is None:
            # Hard coded the in_en_model for now. change it to using model_lang as parameter
            model = Model("in_en_model")
            logger.info("Using default English (US) model")
        else:
            model = Model("in_en_model")
            logger.info(f"Using language model: {model_lang}")


        with sd.RawInputStream(samplerate=samplerate, blocksize=8000, device=device,
                                dtype="int16", channels=1, callback=callback):

            rec = KaldiRecognizer(model, samplerate)
            logger.info("Speech recognition engine started") # Log recognizer start
            while True:
                data = q.get()
                if rec.AcceptWaveform(data):
                    result = rec.Result()
                    logger.debug(f"VOSK Result: {result}") # Debug log of full VOSK result
                    result_json = json.loads(result)
                    new_transcription = result_json.get('text', '')

                    if new_transcription: # Only update if transcription is not empty
                        transcription_text = new_transcription
                        socketio.emit('transcription_update', {'text': transcription_text}, namespace='')
                        logger.info(f"Full transcription: {transcription_text}") # Log full transcription
                        partial_text_cache = "" # Clear partial cache after full result

                else:
                    partial_result = rec.PartialResult()
                    partial_json = json.loads(partial_result)
                    partial_text = partial_json.get('partial', '')

                    if partial_text and partial_text != partial_text_cache: # Check for new partial text and avoid redundant updates
                        transcription_text = partial_text # Update global variable even for partial
                        socketio.emit('transcription_update', {'text': partial_text}, namespace='/test')
                        partial_text_cache = partial_text # Update partial cache
                        logger.debug(f"Partial transcription: {partial_text}") # Debug log partial transcription
                    elif not partial_text and partial_text_cache: # Clear website if partial becomes empty
                        transcription_text = ""
                        socketio.emit('transcription_update', {'text': ""}, namespace='/test') # Clear website
                        partial_text_cache = "" # Clear cache
                        logger.debug("Partial transcription cleared")


    except KeyboardInterrupt:
        logger.info("Transcription stopped by user (KeyboardInterrupt)") # Log user initiated stop
        print("\nDone") # Keep console print for user feedback
    except Exception as e:
        logger.error(f"Exception in transcribe_microphone: {type(e).__name__}: {str(e)}") # Log full exceptions
        print(f"Error: {type(e).__name__}: {str(e)}") # Print error to console as well


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Live microphone transcription to website",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        "-d", "--device", type=int_or_str,
        help="input device (numeric ID or substring)")
    parser.add_argument(
        "-r", "--samplerate", type=int, help="sampling rate")
    parser.add_argument(
        "-m", "--model", type=str, help="language model; e.g. en-us, fr, nl; default is en-us")
    parser.add_argument(
        '--host', type=str, default='0.0.0.0', help='Host for Flask app')  # Add host argument
    parser.add_argument(
        '--port', type=int, default=5000, help='Port for Flask app')  # Add port argument
    parser.add_argument(
        '--debug', action='store_true', help='Enable debug logging') # Enable debug mode

    args = parser.parse_args()

    if args.debug: # Enable debug logging if --debug flag is set
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")


    # Start transcription in a separate thread so Flask can run
    import threading
    threading.Thread(target=transcribe_microphone, args=(args.samplerate, args.device, args.model), daemon=True).start() # Daemon thread

    socketio.run(app, host=args.host, port=args.port, debug=False) # Debug for Flask set to False, use --debug flag for app logging