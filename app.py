from flask import Flask, render_template, request, jsonify
import os
import pygame

app = Flask(__name__)

# Initialize pygame for sound playback
pygame.mixer.init()

# Define where in the current working directory the sound folder is
SOUND_FOLDER = os.path.join(os.getcwd(), 'static/sounds')

# Look in 'SOUND_FOLDER' for mp3's put them in an array and populate the
# 'index.html' template with the sounds as buttons.
@app.route('/')
def index():
    sound_files = [f for f in os.listdir(SOUND_FOLDER) if f.endswith('.mp3')]
    return render_template('index.html', sounds=sound_files)

# Request handling; check if requested file exists, load and play
# Return error if request file is not found in the requested location
@app.route('/play', methods=['POST'])
def play_sound():
    sound_file = request.json.get('sound_file')
    if sound_file and os.path.exists(os.path.join(SOUND_FOLDER, sound_file)):
        # Load and play the sound
        pygame.mixer.music.load(os.path.join(SOUND_FOLDER, sound_file))
        pygame.mixer.music.play()
        return jsonify({'status': 'playing', 'file': sound_file})
    return jsonify({'status': 'error', 'message': 'File not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
