import pygame
import time
from _thread import *

import multiplayer
import graphics


def fight(win, screen_size, path_images, my_poke, battle_id, trainer_id, opponent):
    
    server = multiplayer.multiplayer(battle_id, opponent) # handles all the connection, and either creates of connects to a server

    time.sleep(0.5)
    multiplayer.player_initiation_client(server, my_poke, trainer_id, screen_size)
    
    graphics.load(path_images)

    frame_nb = 0
    map = multiplayer.load_info(server)

    clock=pygame.time.Clock()

    while 1:

        graphics.draw(win, screen_size, map, trainer_id)
        if (frame_nb%4==0):
            map = multiplayer.load_info(server)
        
        
        clock.tick(30)
        frame_nb+=1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

    

