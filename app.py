from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import pygame
from mutagen.mp3 import MP3
from mutagen._util import MutagenError

app = Flask(__name__)

# Set default vars
defaults = {
    "TITLE": "Sirenus",
    "HEADING": "Sirenus Soundboard",
    "DESC": "Click one of the buttons below to play a sound!",
    "SOUND_DIR": 'static/sounds/',
    "SAMPLE_RATE": 44100,
}

# Load environment variables for custom config
load_dotenv(dotenv_path='sirenus.cfg')

title = os.getenv('TITLE', defaults['TITLE'])
heading = os.getenv('HEADING', defaults['HEADING'])
desc = os.getenv('DESC', defaults['DESC'])
sound_dir = os.getenv('SOUND_DIR', defaults['SOUND_DIR'])
sample_rate = int(os.getenv('SAMPLE_RATE', defaults['SAMPLE_RATE']))

# Initialize pygame for sound playback
pygame.mixer.pre_init(sample_rate)
pygame.mixer.init()

# Function to validate if a sound is truly an mp3 and not just a file with the extension
def is_mp3(file_path: str) -> bool:
    try:
        mp3_file: Union[MP3, None] = MP3(file_path)
        return True
    except MutagenError:
        return False

# Look in 'sound_dir' for valid mp3's put them in an array and populate the
# 'index.html' template with the valid sounds as buttons.
@app.route('/')
def index():
    valid_files = [file for file in os.listdir(sound_dir) if is_mp3(os.path.join(sound_dir, file))]
    valid_files.sort()
    return render_template('index.html', sounds=valid_files, title=title, heading=heading, desc=desc)

# Request handling; check if requested file exists and is valid, load and play
# Return error if request file is not found in the requested location
@app.route('/play', methods=['POST'])
def play_sound():
    sound_file: Union[str, None] = request.json.get('sound_file')
    sound_path = os.path.join(sound_dir, sound_file)

    if sound_file and os.path.exists(sound_path) and is_mp3(sound_path):
        # Load and play the sound
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        return jsonify({'status': 'playing', 'file': sound_file})
    return jsonify({'status': 'error', 'message': 'File not found'}), 404

# Kill sound if player is busy
@app.route('/stop', methods=['POST'])
def stop_sound():
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
        return jsonify({'status': 'stopped'})
    return jsonify({'status': 'error', 'message': 'No sound is playing'}), 400

if __name__ == '__main__':
    app.run(debug=True)
