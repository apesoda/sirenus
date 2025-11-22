# Sirenus

## Description
A soundboard where the sound is played on the server, rather than the client. Perfect for in the office or at home!

Currently heavily work-in-progress

## Features
- Audio played from a central server
- TTS to play custom sound-bites
- Search bar to quickly find the sound-bite you need
- Randomized sounds - just use a subdirectory
- Hot-swappable sounds, no need to restart the app!

## Requirements
- **Python**: Version 3.11 or later
- **Pip**
- **Flask**
- **Pygame-ce**
- **Mutagen**
- **pyttsx3**

Assuming you have Python and Pip installed already you can run this command to install the requirements:

```
pip3 install flask pygame-ce mutagen pyttsx3
```

## Installation
Installing and running the app is easily done as follows:
```
git clone https://github.com/apesoda/sirenus 
cd sirenus/

python3 app.py
```

### Linux installation notes
If you are on a Linux system and TTS output is not working out of the box you can try installing the packages below:
```
espeak-ng ffmpeg libespeak1
```

## Configuration
Sounds are read from `static/sounds/` by default, put all your favorite sounds in this directory to have them show up on the board!
The mixer assumes a sample rate of `44100 Hz`.

Basic customization is available by editing the [`sirenus.toml`](sirenus.toml) file

Sample:
```
[ui]
title = "Cool Tab Title"
heading = "The Best Soundboard"
desc = "Below you will find some beautiful sounds, have a click!"
```
See the [`defaults.toml`](helpers/defaults.toml) file to view  _all_ options.

## API
You can use requests to the API to trigger sounds/TTS as well! This way you can hook playing sounds into scripts/workflows.
```
curl -X POST http://sirenus.example.com/play -H "Content-Type: application/json" -d '{"sound_file":"sound.mp3"}'
```

## Contributing
See [`CONTRIBUTING.md`](CONTRIBUTING.md)

## Acknowledgements
This project makes use of the following free (as in speech and beer) content:
- **Boing 2** by magnuswaker: https://freesound.org/s/540790/ License: Creative Commons 0
- **Icons** by Lucide: https://lucide.dev/icons/github  License: ISC
- **Inter** by RSMS: https://github.com/rsms/inter.git License: OFL
