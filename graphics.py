import pygame
import time
import random
import multiplayer
import os


_global_zoom = 1
_global_zoom_point = None
_zoomed_creature = None
trainer_position = None

font_atk = pygame.font.Font('./Fonts/a.ttf', 18)

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
                image=pygame.transform.rotozoom(image, 0, 0.2)
            elif name == "oponent_turn.png": 
                image = pygame.image.load(os.path.join(path_images, "player_turn.png"))
                image=pygame.transform.rotozoom(image, 0, 0.2)
                image.fill((0, 0, 0, 255), None, pygame.BLEND_RGBA_MULT) # (0, 255, 100, 255)
            elif name == "ally_turn.png": 
                image = pygame.image.load(os.path.join(path_images, "player_turn.png"))
                image=pygame.transform.rotozoom(image, 0, 0.2)
                image.fill((0, 255, 100, 255), None, pygame.BLEND_RGBA_MULT) # (0, 255, 100, 255)
            elif "trainer_" in name : # if trainer
                image=pygame.transform.rotozoom(image, 0, 3)
            
                

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
            image_size = image.get_size()
            for y in range(y_):
                for x in range(x_): 
                    
                    #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
                    
                    coordinates = [int(image_size[0]/x_*x),int(image_size[1]/y_*y),int(image_size[0]/x_),int(image_size[1]/y_)-20]
                    if coordinates[1]>0:
                        coordinates[1]-=20
                    images_list[name.split("-")[0]+"_"+str(counter)] = image.subsurface(coordinates)
                    counter +=1 



def draw(win, screen_size, map, my_trainer_id):

    win.fill((0,0,0))
    if _global_zoom!=1: image=pygame.transform.rotozoom(images_list["background"], 0,_global_zoom) 
    else: image=images_list["background"]
    win.blit(image, (_global_zoom_point[0]+(_global_zoom_point[0]-screen_size[0]/2)*(_global_zoom-1), _global_zoom_point[1]+(_global_zoom_point[1]-screen_size[1]/2)*(_global_zoom-1)))

    
    _current_zoomed_creature = 0
    for element in map:
        if element['name'].startswith("_"):
            if element['name'] == "_turn_order":
                count = 0
            
                for index in element['data']:

                    icon_image = images_list[map[index]['name'].replace('-b', '-f')+"_icon"]    
                    creature_icon_margin = (60,35-icon_image.get_size()[1]/2)

                    if "-b" in map[index]['name']:
                        if (map[index]['player']==my_trainer_id):
                            background_image = images_list["player_turn"].copy()
                        else:
                            background_image = images_list["ally_turn"].copy()
                        
                    else:
                        background_image = images_list["oponent_turn"].copy()
                        #background_image = images_list["oponent_turn"].copy()
                        
                    win.blit(background_image, (-60 if count>0 else 0,(count)*60))
                    win.blit(icon_image, (creature_icon_margin[0]+(-60 if count>0 else 0), (count)*60+creature_icon_margin[1]))                        

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
            
            if (element.get('player')==my_trainer_id):
                _current_zoomed_creature +=1
            if (element.get('player')!=my_trainer_id) or _current_zoomed_creature!=_zoomed_creature:
                image.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)


        offset = element['position'].get('y-offset')
        if offset:
            element['position']['y-offset']+=random.randint(-2,2)/10
        else:
            offset = 0
        win.blit(image, (x_position-image.get_size()[0] + _global_zoom_point[0]+(_global_zoom_point[0]+x_position-screen_size[0]/2)*(_global_zoom-1),offset+ y_position-image.get_size()[1]+ _global_zoom_point[1]+(_global_zoom_point[1]+y_position-screen_size[1]/2)*(_global_zoom-1)) )

        
        #win.blit(images_list[element['name']], (element['position']['x'], element['position']['y']))

        

    # ui
    positions = [trainer_position[:], (trainer_position[0]*2.2, trainer_position[1])]
    for current_player in range(len(map[1]['players_ids'])):
        image = images_list["trainer_"+map[1]['players_ids'][current_player]]
        image2 = image.copy()
        if map[1]['players_ids'][current_player] != my_trainer_id:
            image2.fill((255, 255, 255, 150), None, pygame.BLEND_RGBA_MULT)
            
                    
        win.blit(image2, positions[current_player])

    """
    if is_multiplayer==1:
        win.blit(images_list['ally_back'], )
    win.blit(images_list['trainer_back'], trainer_position)
    """

    pygame.display.update()
    



def visual_animations(inputs, screen_size, win, map, my_trainer_id, server, clock):
    global _global_zoom, _global_zoom_point, trainer_position, _zoomed_creature
    animation_duration = 20

    if _global_zoom_point==None:
        _global_zoom_point= [0,-70]
        trainer_position = [screen_size[0]/18, screen_size[1]*5/8]
        _global_zoom =1
        return 0 # no selection
    
    if inputs[pygame.K_LSHIFT]:
        return -1

    if inputs[pygame.K_a]: # at start or if a pressed, global view
        _old_point = _global_zoom_point[:]
        _old_zoom = _global_zoom
        _old_trainer_position = trainer_position[:]

        for i in range(animation_duration):

            #if (i%8==3):
            #    map = multiplayer.load_info(server, [])

            _global_zoom_point[0]+=(0-_old_point[0])/animation_duration
            _global_zoom_point[1]+=(-70-_old_point[1])/animation_duration
            
            trainer_position[0]+=(screen_size[0]/18-_old_trainer_position[0])/animation_duration
            trainer_position[1]+=(screen_size[1]*5/8-_old_trainer_position[1])/animation_duration
            
            _global_zoom += (1-_old_zoom)/animation_duration
            draw(win, screen_size, map, my_trainer_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(60)
        return 0 # no selection

    elif inputs[pygame.K_1] or inputs[pygame.K_2] or inputs[pygame.K_3]:
        _zoomed_creature =  inputs[pygame.K_1]*( inputs[pygame.K_2]==0)*( inputs[pygame.K_3]==0) +2*  inputs[pygame.K_2]*( inputs[pygame.K_1]==0)*( inputs[pygame.K_3]==0) +3* inputs[pygame.K_3]*( inputs[pygame.K_2]==0)*( inputs[pygame.K_1]==0)
        if _zoomed_creature==0:
            return -1# don't change selected

        _old_point = _global_zoom_point[:]
        _old_zoom = _global_zoom
        _old_trainer_position = trainer_position[:]
        for i in range(animation_duration):

            #if (i%8==3):
            #    map = multiplayer.load_info(server, [])

            _global_zoom_point[0]+=(-100-_old_point[0])/animation_duration
            _global_zoom_point[1]+=(30-_old_point[1])/animation_duration
            
            trainer_position[0]+=(-500-_old_trainer_position[0])/animation_duration
            trainer_position[1]+=(screen_size[1]-_old_trainer_position[1])/animation_duration
            
            _global_zoom += (1.2-_old_zoom)/animation_duration
            draw(win, screen_size, map, my_trainer_id)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            clock.tick(60)
        return _zoomed_creature # change selected 
    return -1 # don't change selected
    





   
