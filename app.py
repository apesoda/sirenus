#!/usr/bin/env python3
import os
import pygame
import pyttsx3
import random
import tomllib
from flask import Flask, render_template, request, jsonify
from pygame import mixer, base
from mutagen.mp3 import MP3
from mutagen._util import MutagenError
from typing import Union
from helpers.svg import svg
from helpers.config import set_config 

app = Flask(__name__)

with app.app_context():
    config = set_config()

# Load svgs
app.jinja_env.globals["svg"] = svg

# Set
sound_dir = config['app']['sound_dir']
sample_rate = config['app']['sample_rate']

# Initialize pygame for sound playback
pygame.mixer.pre_init(sample_rate)
pygame.mixer.init()

# Initialize TTS engine
engine = pyttsx3.init()

# Function to validate if a sound is truly an mp3 and not just a file with the extension
def is_mp3(file_path: str) -> bool:
    try:
        mp3_file: Union[MP3, None] = MP3(file_path)
        return True
    except MutagenError:
        return False

# Helper to get valid mp3s in a directory
def get_mp3s_in_dir(directory: str):
    try:
        return [f for f in os.listdir(directory) if is_mp3(os.path.join(directory, f))]
    except FileNotFoundError:
        return []

# Look in 'sound_dir' for valid mp3's and folders containing mp3's, put them in an array and populate the
# 'index.html' template with the valid sounds as buttons. Only send the name (not type) to the frontend.
@app.route('/')
def index():
    items = []
    for entry in os.listdir(sound_dir):
        path = os.path.join(sound_dir, entry)
        if os.path.isfile(path) and is_mp3(path):
            items.append(entry)
        elif os.path.isdir(path):
            mp3s = get_mp3s_in_dir(path)
            if mp3s:
                items.append(entry)
    items.sort()
    return render_template('index.html', sounds=items, config=config)

# Request handling; check if requested file exists and is valid, load and play
# Return error if request file is not found in the requested location
@app.route('/play', methods=['POST'])
def play_sound():
    sound_file = request.json.get('sound_file')
    if not sound_file:
        return jsonify({'status': 'error', 'message': 'No file or folder specified'}), 400

    # Simple path injection check
    if '..' in sound_file or sound_file.startswith('/') or '\\' in sound_file:
        return jsonify({'status': 'error', 'message': 'Invalid file or folder name'}), 400

    path = os.path.join(sound_dir, sound_file)
    if os.path.isfile(path) and is_mp3(path):
        # It's a valid mp3 file
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        return jsonify({'status': 'playing', 'file': sound_file})
    elif os.path.isdir(path):
        # It's a folder, pick a random mp3 inside
        mp3s = get_mp3s_in_dir(path)
        if mp3s:
            chosen_mp3 = random.choice(mp3s)
            sound_path = os.path.join(path, chosen_mp3)
            pygame.mixer.music.load(sound_path)
            pygame.mixer.music.play()
            return jsonify({'status': 'playing', 'file': chosen_mp3, 'folder': sound_file})
        else:
            return jsonify({'status': 'error', 'message': 'No mp3s in folder'}), 404
    else:
        return jsonify({'status': 'error', 'message': 'File or folder not found'}), 404

# Kill sound if player is busy
@app.route('/stop', methods=['POST'])
def stop_sound():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        return jsonify({'status': 'stopped sound'})
    return jsonify({'status': 'error', 'message': 'No sound is playing'}), 400

@app.route('/speak', methods=['POST'])
def speak_text():
    # Kill any soundbites that may be playing
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    text = request.json.get('text', '')
    if engine._inLoop:
        engine.endLoop()
    if text:
        engine.say(text)
        engine.runAndWait()
        return jsonify({'status': 'speaking', 'text': text})
    return jsonify({'status': 'error', 'message': 'No text provided'}), 400

if __name__ == '__main__':
    app.run(port=config['app']['port'], host=config['app']['host'])
