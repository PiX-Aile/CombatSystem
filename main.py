import pygame
import time
from _thread import *

import multiplayer
import graphics




def fight(win, screen_size, path_images, my_poke, battle_id, trainer_id, opponent):

    has_already_attacked = [] # for animations, just after choosing attack, pokemon is still in turn order, but it has to dezoom to show attack
    # is equal to yes at first to that at the very beginning it zoomes right

    def load_map(server, data_to_send, map, has_already_attacked):
        
        loaded = multiplayer.load_info(server, data_to_send)
        
        if loaded != map:

            #did the first in torn_order change ?
            if (len(map)>0 and len(map[0].get("data"))>0 and map[0].get("data")[0] != loaded[0].get("data")[0]):
                while has_already_attacked:
                    del has_already_attacked[0]
                print("new turn order !!", loaded[0]["data"][0])

            for i in range(len(map)):
                map.pop(0)
            map.extend(loaded)
        
        
    
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
        graphics.visual_animations(keys, screen_size, win, map, trainer_id, server, clock, has_already_attacked)
        graphics.draw(win, screen_size, map, trainer_id)

    


        if (not data_to_send)  :
            selected_move =  keys[pygame.K_1]*( keys[pygame.K_2]==0)*( keys[pygame.K_3]==0) +2*  keys[pygame.K_2]*( keys[pygame.K_1]==0)*( keys[pygame.K_3]==0) +3* keys[pygame.K_3]*( keys[pygame.K_2]==0)*( keys[pygame.K_1]==0)
            #selected_creature = 0
            if selected_move:
                has_already_attacked.append("yess")
                data_to_send.append({'selected_move':selected_move})

        if (frame_nb%10==0):
            current_time = time.time()
            start_new_thread(load_map, (server,data_to_send, map, has_already_attacked))
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

    

