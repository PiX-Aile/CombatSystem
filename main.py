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
    map = multiplayer.load_info(server, [])

    clock=pygame.time.Clock()

    old_time = time.time()
    selected_creature = 0 # no selected
    data_to_send = []
    while 1:

        keys = pygame.key.get_pressed()

        output = graphics.visual_animations(keys, screen_size, win, map, trainer_id, server, clock)
        graphics.draw(win, screen_size, map, trainer_id)

        
        if output!=-1:
            selected_creature = output


        if (not data_to_send) and keys[pygame.K_LSHIFT] and selected_creature:
            selected_move =  keys[pygame.K_1]*( keys[pygame.K_2]==0)*( keys[pygame.K_3]==0) +2*  keys[pygame.K_2]*( keys[pygame.K_1]==0)*( keys[pygame.K_3]==0) +3* keys[pygame.K_3]*( keys[pygame.K_2]==0)*( keys[pygame.K_1]==0)
            if selected_move:
                move_name = my_poke[selected_creature-1].atks[selected_move-1]
                data_to_send.append({'move_name':move_name, 'creature_index': selected_creature})

        if (frame_nb%4==0):
            
            map = multiplayer.load_info(server, data_to_send)
            data_to_send = []
        
        a = time.time()
        #print(1/(a-old_time)) # displayes fps
        old_time = a
        
        clock.tick(30)
        frame_nb+=1
        
        for event in pygame.event.get():
            if event.type == pygame.quit:
                pygame.quit()
            if event.type == pygame.QUIT:
                pygame.quit()

    

