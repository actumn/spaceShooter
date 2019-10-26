from os import path

import pygame

from spaceshooter import sound_folder

shooting_sound = pygame.mixer.Sound(path.join(sound_folder, 'pew.wav'))
missile_sound = pygame.mixer.Sound(path.join(sound_folder, 'rocket.ogg'))
expl_sounds = [
    pygame.mixer.Sound(path.join(sound_folder, sound)) for sound in ['expl3.wav', 'expl6.wav']
]
pygame.mixer.music.set_volume(0.2)

player_die_sound = pygame.mixer.Sound(path.join(sound_folder, 'rumble1.ogg'))
