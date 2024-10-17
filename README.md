# Sirenus

## Description
A soundboard where the sound is played on the server, rather than the client. Perfect for in the office or at home!

Currently heavily work in progress

## Features
- Audio played from a central server
- Hot-swappable sounds, no need to restart the app!

## Pre-requisites
- **Python**: Version 3.8 or later
- **Pip**
- **Flask**
- **Pygame**

Assuming you have Python and Pip installed already you can run this command to install the re-requisites:

```
pip3 install flask pygame
```

## Installation
Installing and running the app is easily done as follows:
```
git clone https://github.com/apesoda/sirenus 
cd sirenus/

python3 -m flask run --host='0.0.0.0'
```
Sounds are read from `static/sounds/`, so put any of your desired

## Acknowledgements
This project makes use of the following free (as in speech and beer) content:
- **Boing 2** by magnuswaker: https://freesound.org/s/540790/- License: Creative Commons 0
- **Github icon** by Lucide -- https://lucide.dev/icons/github -- License: ISC
