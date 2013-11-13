steampunk_dlna
==============

A controller for my home DLNA network. With punchcards, lights and stuff.

The plan:
I want to control my music at home with a Steampunked DLNA controller. It will run on a Raspberry PI with Arduino.
Selection of music is done with punchcards. Display of current music is done using displays controlled by a motorshield with servos and
stepper motors.

punchcard creator
-----------------
Punchcards are SVG files created out of the data from the music. The cards contain an ID of the music to play. This will then be looked up. The creator creates the db and the svg files

Controller
----------
Input: Camera, music-db, Rotary encoder
Output: Audio, stepper and servos
