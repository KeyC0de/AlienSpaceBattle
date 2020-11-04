#! python
#coding=utf-8
#setup.py
import os
os.environ['TCL_LIBRARY'] = "C:/Program Files/Python36/tcl/tcl8.6"
os.environ['TK_LIBRARY'] = "C:/Program Files/Python36/tcl/tk8.6"
import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name = "python_invaders",
    version = "0.1",
    options={"build_exe": {"packages":["pygame"], 
                           "include_files":["images/2d-game-background-3.png","images/alien.bmp","images/alien_green.png", "images/alien_grey.png", "images/alien_nobg.tga", "images/alien_orange.png", "images/alien_purple.png", "images/destroyed_alien.png", "images/destroyed_green.png", "images/destroyed_ship.png", "images/missile.png", "images/missile_small.png", "images/raindrop.png", "images/ship.bmp", "images/ship_nobg.bmp", "images/ship_nobg.png", "images/space_background.jpg", "images/space_background.png", "images/star.png","sounds/bg_romariogrande__alien-dream.wav","sounds/fire_missile.ogg", "sounds/bg_romariogrande__alien-dream.ogg", "sounds/fire_missile.wav", "sounds/laser_bullet.wav", "sounds/laser_impact.ogg", "sounds/missile_hit.wav"]}},
    description = "Space Invaders in Python. Made with PyGame by Nikos Lazaridis",
    author = "Nikos J. Lazaridis",
    executables = executables
)


