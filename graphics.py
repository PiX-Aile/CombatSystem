import pygame
import time
import random
import multiplayer
import os

from game_logics import all_coordinates


_global_zoom = 1 # set at the beginning of loop
_global_zoom_point = None
trainer_position = None

font_atk = pygame.font.Font('./Fonts/a.ttf', 15)

images_list = {}

def load(path_images):
    global images_list
    images_list = {}



    for name in os.listdir(os.path.join(path_images, "Fighting")):
        if ".png" in name :
            image = pygame.image.load(os.path.join(path_images, "Fighting", name)) # loads the image  

            if name == "background.png": 
                image=pygame.transform.rotozoom(image, 0, 0.8)

            elif name == "player_turn.png": 
                image=pygame.transform.rotozoom(image, 0, 1.4)
            elif name == "oponent_turn.png": 
                image = pygame.transform.rotozoom(image, 0, 1.4)
            elif name == "ally_turn.png": 
                image = pygame.transform.rotozoom(image, 0, 1.4)



            elif "trainer_" in name : # if trainer
                image=pygame.transform.rotozoom(image, 0, 3.5)

            elif name == "hp-full.png" or name=="hp-empty.png": 
                 image=pygame.transform.rotozoom(image, 0, 1.7)
                 image.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)
            elif name == "ennemy-hp-full.png" or name=="ennemy-hp-empty.png": 
                 image=pygame.transform.rotozoom(image, 0, 2)
            
                

            #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
            images_list[name.split(".")[0]] = image

    for name in os.listdir(os.path.join(path_images, "Creatures")):
        if ".png" in name :
            image = pygame.image.load(os.path.join(path_images, "Creatures", name)) # loads the image  

            image = pygame.transform.rotozoom(image, 0, 128/image.get_size()[0])

            if "-b" in name:
                    image = pygame.transform.rotozoom(image, 0, 2.4/1.3*0.8)
            if "-f" in name:
                image = pygame.transform.rotozoom(image, 0, 1.8/1.3*0.8)
                images_list[name.split(".")[0]+"_icon"] = pygame.transform.rotozoom(image, 0, 0.35)
                

            #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
            images_list[name.split(".")[0]] = image

    for name in os.listdir(os.path.join(path_images, "Animations")):
        counter = 0
        if ".png" in name :
            _a,y_,x_,_b = name.split("-")
            y_ = int(y_)
            x_ = int(x_)
            image = pygame.image.load(os.path.join(path_images, "Animations", name)) # loads the image  
    
            image = pygame.transform.rotozoom(image, 0, 1.5*800/image.get_size()[0])
            if "banner" in name:
                image = pygame.transform.rotozoom(image, 0, 0.7)
            if "Piplup" in name or "tkt" in name:
                image = pygame.transform.rotozoom(image, 0, 0.15)
            image_size = image.get_size()
            for y in range(y_):
                for x in range(x_): 
                    
                    #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
                    
                    coordinates = [int(image_size[0]/x_*x),int(image_size[1]/y_*y),int(image_size[0]/x_),int(image_size[1]/y_)-20]
                    if coordinates[1]>0:
                        coordinates[1]-=20
                    images_list[name.split("-")[0]+"_"+str(counter)] = image.subsurface(coordinates)
                    counter +=1 
        elif not ("." in name):
            counter = 0
            for file in os.listdir(os.path.join(path_images, "Animations", name)):
                image = pygame.image.load(os.path.join(path_images, "Animations", name, file)) # loads the image  
                image = pygame.transform.rotozoom(image, 0, 2)
                images_list[file.replace("-", "_").split(".")[0]] = image
                counter+=1



banner_counter = 0
def draw(win, screen_size, map, my_trainer_id):
    global banner_counter

    win.fill((0,0,0))
    if _global_zoom!=1: image=pygame.transform.rotozoom(images_list["background"], 0,_global_zoom) 
    else: image=images_list["background"]
    win.blit(image, (_global_zoom_point[0]+(_global_zoom_point[0]-screen_size[0]/2)*(_global_zoom-1), _global_zoom_point[1]+(_global_zoom_point[1]-screen_size[1]/2)*(_global_zoom-1)))

    
    for element in map:
        if element['name'].startswith("_"):
            if element['name'] == "_turn_order":
                count = 0
            
                for index in element['data']:
                    
                    if (count>3):
                        continue
                        

                    try:

                        icon_image = images_list[map[index]['name'].replace('-b', '-f')+"_icon"]   
                    except KeyError:
                        print("key error in graphics")
                        continue
                    creature_icon_margin = (60,35-icon_image.get_size()[1]/2)

                    if "-b" in map[index]['name']:
                        if (map[index]['player']==my_trainer_id):
                            background_image = images_list["player_turn"].copy()
                        else:
                            background_image = images_list["ally_turn"].copy()
                        
                    else:
                        background_image = images_list["oponent_turn"].copy()
                        #background_image = images_list["oponent_turn"].copy()
                        
                    win.blit(background_image, (-30 if count>0 else 0,(count)*70))
                    win.blit(icon_image, (creature_icon_margin[0]+(-50 if count>0 else -20), (count)*70+creature_icon_margin[1]))                        

                    count += 1


                #if map[element['data'][0]]['player']==my_trainer_id :
                #    text_co = (background_image.get_size()[0]*3/4+20, background_image.get_size()[1]*2/3)
                #    win.blit(font_atk.render(f'{0}', True, (255,255,255)), text_co)


            continue
    
        
        if not element.get('position'): # pour couvrir certains bugs au début pendant que le serveur init tout
            continue
        

        if element.get('destination'):
            
            current_time = (time.time()-element['starting_time'])/(element['arrival_time'])
            current_frame = 0

            if current_time>1:
                if element.get('explosion_time'):
                    current_frame = int(9*(time.time()-element['arrival_time']-element['starting_time'])/(element['explosion_time']))
                    

                current_time = 1
            
            

            if images_list.get(element['name']):
                image = images_list[element['name']]  
            else: # si on a dépassé la frame max
                  minus_index = 0
                  # erreur sur cette ligne -> fichier d'attaque n'existe pas ou pas le bon nom
                  while not images_list.get(element['name']+"_"+str(current_frame-minus_index)):
                      minus_index+=1
                  image = images_list[element['name']+"_"+str(current_frame-minus_index)]  

            x_position = element['position']['x']+ (element['destination']['x']-element['position']['x'])*current_time
            y_position = element['position']['y']+ (element['destination']['y']-element['position']['y'])*current_time

        else:
            image = images_list[element['name']]    
            x_position = element['position']['x']
            y_position = element['position']['y']

        if _global_zoom !=1:
            image=pygame.transform.rotozoom(image, 0,_global_zoom)
            
            
            
            # old code to reduce opacity of not selected
            if ((element.get('player')!=my_trainer_id) or element!=map[map[0]["data"][0]]) :
                if _global_zoom>=1: # to ignore animation of start
                    image.fill((255, 255, 255, 100 + 150 *(most_zoomed-_global_zoom) ), None, pygame.BLEND_RGBA_MULT)
            


        offset = element['position'].get('y-offset')
        if offset:
            element['position']['y-offset']+=random.randint(-2,2)/10
        else:
            offset = 0

        if element.get("zoom") :# zoom pendant le dash
            image=pygame.transform.rotozoom(image, 0, element.get("zoom"))
        

        base_coordinates = [x_position-image.get_size()[0] + _global_zoom_point[0]+(_global_zoom_point[0]+x_position-screen_size[0]/2)*(_global_zoom-1),y_position-image.get_size()[1]+ _global_zoom_point[1]+(_global_zoom_point[1]+y_position-screen_size[1]/2)*(_global_zoom-1)]
        coordinates = base_coordinates[:];coordinates[1]+=offset
        win.blit(image, coordinates)

        # ui of hps :
        if element.get("hp") and  _global_zoom ==1 :
            

            if element["player"] == 'opponent':
                base_coordinates = (280,-230)
                empty_image = images_list["ennemy-hp-empty"]
                full_image = images_list["ennemy-hp-full"]

            else:
                base_coordinates[0]+=30
                base_coordinates[1]+=30
                empty_image = images_list["hp-empty"]
                full_image = images_list["hp-full"]

            full_image = full_image.subsurface((0,0,full_image.get_size()[0]*element['hp']['current']/element['hp']['full'], full_image.get_size()[1]))
            
            
            win.blit(full_image, base_coordinates)
            win.blit(empty_image,  base_coordinates)
                

        

    # ui
    positions = [trainer_position[:], (trainer_position[0]*2.2, trainer_position[1])]
    for current_player in range(len(map[1]['players_ids'])):
        image = images_list["trainer_"+map[1]['players_ids'][current_player]]
        image2 = image.copy()
        if map[1]['players_ids'][current_player] != my_trainer_id:
            image2.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)
            
                    
        win.blit(image2, positions[current_player])
    # battle ui
    banner_counter+=0.4
    if _global_zoom>1:
        current_poke = map[map[0]["data"][0]]
        for i in range(0, len(current_poke["atks"])):
            text_co = (screen_size[0]*3/5, screen_size[1]*1/5+136*i +20)
            liste_co = [(screen_size[0]*2/5-70, -170+140*i +20),
                        (screen_size[0]*2/5, -170+140*i +70+20),
                        (screen_size[0]*2/5-78, -170+140*i +20),
                        ]
            img_co = liste_co[i]
            image = images_list[f"Banner_{(int(banner_counter)+3*i)%9+1}"]

            image = pygame.transform.rotozoom(image, 20-20*i, 1)#1-1*(most_zoomed-_global_zoom))

            fill_value = 250-1000*(most_zoomed-_global_zoom)
            if fill_value<0:fill_value=0
            image.fill((255, 255, 255, fill_value), None, pygame.BLEND_RGBA_MULT)

            win.blit(image, img_co)

            if _global_zoom==most_zoomed:
                text = font_atk.render(f'{i+1} : {current_poke["atks"][i].replace("_", " ").replace("dash", "")}', True, (255,255,255))
                text = pygame.transform.rotozoom(text, 20-20*i, 1)
                win.blit(text, text_co)


    """
    if is_multiplayer==1:
        win.blit(images_list['ally_back'], )
    win.blit(images_list['trainer_back'], trainer_position)
    """

    pygame.display.update()
    


waiting_time = 20
animation_duration = 15
zoom_delay = 0

most_zoomed = 2

super_loin_trainer_position = [-200, 400]

def visual_animations(inputs, screen_size, win, map, my_trainer_id, server, clock, has_already_attacked):
    global _global_zoom, _global_zoom_point, trainer_position, zoom_delay
    

    if _global_zoom_point==None:
        _global_zoom_point= [0,-70]
        trainer_position = super_loin_trainer_position[:]
        _global_zoom =0
        return 0 # no selection
    
    if inputs[pygame.K_LSHIFT]:
        return -1

    if zoom_delay>=0:
        zoom_delay -=1

    if _global_zoom!=1 and (has_already_attacked) and zoom_delay<0: # (map[map[0]["data"][0]].get("player") != my_trainer_id or has_already_attacked)
        _old_point = _global_zoom_point[:]
        _old_zoom = _global_zoom
        _old_trainer_position = trainer_position[:]
        zoom_delay = waiting_time

        # first everythiing but trainer
        for i in range(animation_duration):

            #if (i%8==3):
            #    map = multiplayer.load_info(server, [])

            
            position = (100, -30)
            position = (0, 10)

            _global_zoom_point[0]+=(-position[0]-_old_point[0])/animation_duration
            _global_zoom_point[1]+=(-position[1]-_old_point[1])/animation_duration
            
            
            
            _global_zoom += (1-_old_zoom)/animation_duration
            draw(win, screen_size, map, my_trainer_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(80)
        # now character
        for i in range(animation_duration):
            trainer_position[0]+=(screen_size[0]/18-_old_trainer_position[0])/animation_duration
            trainer_position[1]+=(screen_size[1]*5/8-_old_trainer_position[1])/animation_duration
            draw(win, screen_size, map, my_trainer_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(80)

        _global_zoom=1
    
    if _global_zoom==1 and map[map[0]["data"][0]].get("player") == my_trainer_id and (not has_already_attacked)  and zoom_delay<0:

        zoom_delay = waiting_time

        _old_point = _global_zoom_point[:]
        _old_zoom = _global_zoom
        _old_trainer_position = trainer_position[:]
        # first trainer animation
        for i in range(animation_duration):
            trainer_position[0]+=(super_loin_trainer_position[0]-_old_trainer_position[0])/animation_duration
            trainer_position[1]+=(super_loin_trainer_position[1]-_old_trainer_position[1])/animation_duration
            draw(win, screen_size, map, my_trainer_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(80)
        # now other characters
        for i in range(animation_duration):

            #if (i%8==3):
            #    map = multiplayer.load_info(server, [])

            #destination = (100, -30)

            destination =( -all_coordinates[0][0]['x']+screen_size[0]/2,
                -all_coordinates[0][0]['y']+screen_size[1]/2)

            co = map[map[0]["data"][0]]['position']
            destination = (screen_size[0]/2-co['x']+60, screen_size[1]/2-co['y']+100
                           )


            _global_zoom_point[0]+=(destination[0]-_old_point[0])/animation_duration
            _global_zoom_point[1]+=(destination[1]-_old_point[1])/animation_duration
            
            
            
            _global_zoom += (most_zoomed-_old_zoom)/animation_duration
            draw(win, screen_size, map, my_trainer_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            
            clock.tick(80)
        _global_zoom = most_zoomed
        


    





   
