from flask import Flask, render_template, request, jsonify
import os
import pygame
from mutagen.mp3 import MP3
from mutagen._util import MutagenError

app = Flask(__name__)

# Initialize pygame for sound playback
pygame.mixer.init()

# Define where in the current working directory the sound folder is
SOUND_FOLDER = os.path.join(os.getcwd(), 'static/sounds')

# Function to validate if a sound is truly an mp3 and not just a file with the extension
def is_mp3(file_path: str) -> bool:
    try:
        mp3_file: Union[MP3, None] = MP3(file_path)
        return True
    except MutagenError:
        return False

# Look in 'SOUND_FOLDER' for valid mp3's put them in an array and populate the
# 'index.html' template with the valid sounds as buttons.
@app.route('/')
def index():
    valid_files = [file for file in os.listdir(SOUND_FOLDER) if is_mp3(os.path.join(SOUND_FOLDER, file))]
    valid_files.sort()
    return render_template('index.html', sounds=valid_files)

# Request handling; check if requested file exists and is valid, load and play
# Return error if request file is not found in the requested location
@app.route('/play', methods=['POST'])
def play_sound():
    sound_file: Union[str, None] = request.json.get('sound_file')
    sound_path = os.path.join(SOUND_FOLDER, sound_file)

    if sound_file and os.path.exists(sound_path) and is_mp3(sound_path):
        # Load and play the sound
        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.play()
        return jsonify({'status': 'playing', 'file': sound_file})
    return jsonify({'status': 'error', 'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
