import pygame
import os 
import random

screen_size = (1250*0.85,680*0.9) # will be changed after
#screen_size = (1250*0.8,680*0.8)
win = pygame.display.set_mode(screen_size) # sets up the display
pygame.display.set_caption("Game")
pygame.init()
pygame.font.init()

path_images=os.path.join(os.getcwd(),"Images")


class Pokemon():
    def __init__(self, name):
        self.name = name
        self.atks = ["SAlec", "SElec", "SFire"]


import time
import random

my_poke = [Pokemon("Pumpking"), Pokemon("Pumpking"), Pokemon("Pumpking")]

opponent = Pokemon("Samourai")

#trainer_id = random.choice(["AK", "N"])
trainer_id = "N" # 'AK' or 'N'

battle_id = "1"

import main
main.fight(win, screen_size, path_images, my_poke, battle_id, trainer_id, opponent)

