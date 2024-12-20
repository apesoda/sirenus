# Sirenus

## Description
A soundboard where the sound is played on the server, rather than the client. Perfect for in the office or at home!

Currently heavily work-in-progress

## Features
- Audio played from a central server
- Hot-swappable sounds, no need to restart the app!

## Requirements
- **Python**: Version 3.8 or later
- **Pip**
- **Flask**
- **Pygame**
- **Mutagen**

Assuming you have Python and Pip installed already you can run this command to install the requirements:

```
pip3 install flask pygame mutagen
```

## Installation
Installing and running the app is easily done as follows:
```
git clone https://github.com/apesoda/sirenus 
cd sirenus/

python3 -m flask run --host='0.0.0.0'
```
Sounds are read from `static/sounds/`, put all your favorite sounds in this directory to have them show up on the board!

## Terminal
Since the sounds are played using POST requests you can also play them from the terminal
```
curl -X POST http://host:5000/play -H "Content-Type: application/json" -d '{"sound_file":"sound.mp3"}'
```

## Acknowledgements
This project makes use of the following free (as in speech and beer) content:
- **Boing 2** by magnuswaker: https://freesound.org/s/540790/ License: Creative Commons 0
- **Github icon** by Lucide: https://lucide.dev/icons/github  License: ISC
- **Inter** by RSMS: https://github.com/rsms/inter.git License: OFL
