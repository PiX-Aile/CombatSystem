import pygame
import random
import os


_global_zoom = 1
_global_zoom_point = [0,0]
_zoomed_creature = None

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

            #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
            images_list[name.split(".")[0]] = image

    for name in os.listdir(os.path.join(path_images, "Creatures")):
        if ".png" in name :
            image = pygame.image.load(os.path.join(path_images, "Creatures", name)) # loads the image  

            if "-b" in name:
                    image = pygame.transform.rotozoom(image, 0, 2.4/1.3*0.8)
            if "-f" in name:
                image = pygame.transform.rotozoom(image, 0, 1.8/1.3*0.8)
                images_list[name.split(".")[0]+"_icon"] = pygame.transform.rotozoom(image, 0, 0.35)
                

            #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
            images_list[name.split(".")[0]] = image
    


def draw(win, screen_size, map, my_trainer_id):
    global _global_zoom, _global_zoom_point

    

    if _global_zoom_point==[0,0]:
        x,y = int(screen_size[0]/4-10+128*2.4/1.3*0.8/2)-30, int(screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8/2)-30
        _global_zoom_point=[0,0]
    
    win.fill((0,0,0))
    if _global_zoom!=1: image=pygame.transform.rotozoom(images_list["background"], 0,_global_zoom) 
    else: image=images_list["background"]
    win.blit(image, (_global_zoom_point[0]+(_global_zoom_point[0]-screen_size[0]/2)*(_global_zoom-1), _global_zoom_point[1]+(_global_zoom_point[1]-screen_size[1]/2)*(_global_zoom-1)))
    
    for element in map:
        if element['name'].startswith("_"):
            if element['name'] == "_turn_order":
                if element['data']:
                    first_el = element['data'][0]
                for index in element['data']:
                    creature = map[index]
                    

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
                        
                    win.blit(background_image, (-60 if index-first_el>0 else 0,(index-first_el)*60))
                    win.blit(icon_image, (creature_icon_margin[0]+(-60 if index-first_el>0 else 0), (index-first_el)*60+creature_icon_margin[1]))

            continue
       
        

        image = images_list[element['name']]    
            
        element['position']['y-offset']+=random.randint(-2,2)/10
        if _global_zoom !=1:
            image=pygame.transform.rotozoom(image, 0,_global_zoom)
            if element!=_zoomed_creature:
                pass
                #image.fill((255, 255, 255, _alpha), None, pygame.BLEND_RGBA_MULT)

        win.blit(image, (element['position']['x']-image.get_size()[0] + _global_zoom_point[0]+(_global_zoom_point[0]+element['position']['x']-screen_size[0]/2)*(_global_zoom-1),element['position']['y-offset']+ element['position']['y']-image.get_size()[1]+ _global_zoom_point[1]+(_global_zoom_point[1]+element['position']['y']-screen_size[1]/2)*(_global_zoom-1)) )

        
        #win.blit(images_list[element['name']], (element['position']['x'], element['position']['y']))

        

    pygame.display.update()
    

