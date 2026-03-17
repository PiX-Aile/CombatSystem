import pygame
import os 
import random

screen_size = (1250*0.85,680*0.9) # will be changed after 1062, 612
#screen_size = (1250*0.8,680*0.8)
win = pygame.display.set_mode(screen_size) # sets up the display
pygame.display.set_caption("Game")
pygame.init()
pygame.font.init()

path_images=os.path.join(os.getcwd(),"Images")


class Pokemon():
    def __init__(self, name):
        self.name = name
        self.atks = []


import time
import random

my_poke = [Pokemon("B"), Pokemon("A"), Pokemon("A")]
my_poke = [Pokemon("A"), Pokemon("B"), Pokemon("A")]
my_poke[0].atks = ["dash_Sword", "dash_SFire", "dash_Sword"]
my_poke[1].atks = ["Elec_Spell", "Plasma_Spell", "Fire_Spell"]
my_poke[2].atks = ["Elec_Spell", "Plasma_Spell", "Fire_Spell"]

opponent = Pokemon("Samourai")
opponent.atks = ["Psy"]

#trainer_id = random.choice(["AK", "N"])
trainer_id = "AK" # 'AK' or 'N'

battle_id = "1"

import main
main.fight(win, screen_size, path_images, my_poke, battle_id, trainer_id, opponent)

