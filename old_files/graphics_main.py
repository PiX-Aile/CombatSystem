import pygame
import os # for file management
import time
import random 


# not a good way to do it but it works
with open("animations.py", "r") as f:
    exec(f.read())

path_images=os.path.join(os.getcwd(),"Images") # gets current directory and adds "Images" to get the image folder

screen_size = (1250,680) # will be changed after
win = pygame.display.set_mode(screen_size) # sets up the display
pygame.display.set_caption("Combat")
pygame.init()
pygame.font.init()
#main_font=pygame.font.Font(None,25)
font_atk = pygame.font.Font('./Fonts/a.ttf', 18)



"""
loads images
example use : load_images() -> {'Minishrum-b': <pygame image loaded>, 'Minishrum-f': <pygame image loaded>}
"""
def load_images():
    images_list = {}
    for name in os.listdir(path_images): # gets all files and folders from the image folder
        if ".png" in name :
            image = pygame.image.load(os.path.join(path_images, name)) # loads the image
            if name == "background.png": 
                image=pygame.transform.rotozoom(image, 0, 0.65) # reduces size by multiplying by 0.65
            elif name == "player_turn.png": 
                image=pygame.transform.rotozoom(image, 0, 0.2)
            elif name == "oponent_turn.png": 
                image = pygame.image.load(os.path.join(path_images, "player_turn.png"))
                image=pygame.transform.rotozoom(image, 0, 0.2)
                image.fill((0, 255, 100, 255), None, pygame.BLEND_RGBA_MULT) # (0, 255, 100, 255)
            elif name=="attack_background.png":
                image=pygame.transform.rotozoom(image, 0, 0.3)
                image.fill((0, 0, 0, 100), None, pygame.BLEND_RGBA_MULT)
            else:
                if "-b" in name:
                    image = pygame.transform.rotozoom(image, 0, 2.4/1.3)
                if "-f" in name:
                    image = pygame.transform.rotozoom(image, 0, 1.8/1.3)
                    #image.fill((255, 255, 255, 170), None, pygame.BLEND_RGBA_MULT) # darken
                
                    
            #image.fill((255, 255, 255, 30), None, pygame.BLEND_RGBA_MULT) # darken
            images_list[name.split(".")[0]] = image
    return images_list
images_list = load_images()


"""
example use : Creature('Minishrum', True, (0,0))
Instantiates a Minishrum at coordinates (0,0) that belongs to the player
"""
class Creature:
    def __init__(self, name, belongs_to_player, position):
        self.name = name
        self.belongs_to_player = belongs_to_player
        print(name + ("-b" if belongs_to_player else "-f") )
        self.image = images_list[ name + ("-b" if belongs_to_player else "-f") ] # gets the image from the loaded images
        self.image_icon = pygame.transform.rotozoom(images_list[ name +  "-f" ], 0, 0.2)
        self.image_base_size = self.image.get_size()
        print(self.image_base_size)
        self.position = position

        self._random_movement = random.randint(0,5)
    
    # will be modified, used to make the creatures 'move' and not stand still
    def _get_random_movement(self):
        self._random_movement+=random.randint(-2,2)/10
        return self._random_movement




# creation of pokemon for player 
my_creatures = []
_names = ["pumpkin", "pumpkin", "pumpkin"]
# below is the list of all positions in order of use for the player's creatures
_pos=[(screen_size[0]/5+96, screen_size[1]*3/5+96), 
             (screen_size[0]/5+190+96, screen_size[1]*3/5+30-10+96),
             (screen_size[0]/5+130+96, screen_size[1]*3/5+100+96),
             (screen_size[0]/5+60+96, screen_size[1]*3/5+85+96)
             ]
for index in range(len(_names)):
    my_creatures.append(Creature(_names[index], True, _pos[index]))

# creation of pokemon for oponent 
oponent_creatures = []
_names = ["pumpkin", "pumpkin"]
# below is the list of all positions in order of use for the oponent's creatures
_pos2=[
            (screen_size[0]*4/5+70, screen_size[1]*2.3/5+100),
            (screen_size[0]*4/5+160, screen_size[1]*2.3/5+96),
        ]
for index in range(len(_names)):
    oponent_creatures.append(Creature(_names[index], False, _pos2[index]))



# the turn order (example: [<Creature()>, <Creature()>])
turn_order = my_creatures[:];turn_order.extend(oponent_creatures)



# drawing function, executed each frame
def draw(_order_y_offset = 0, _order_first_opacity=255):


    win.fill((0,0,0))

    

    if _global_zoom!=1: image=pygame.transform.rotozoom(images_list["background"], 0,_global_zoom) 
    else: image=images_list["background"]
    win.blit(image, (_global_zoom_point[0]+(_global_zoom_point[0]-screen_size[0]/2)*(_global_zoom-1), _global_zoom_point[1]+(_global_zoom_point[1]-screen_size[1]/2)*(_global_zoom-1)))

    

    image_position_randomizer = int(time.time()*10)%5


    if _global_zoom >=_zoom_max:
        min_, max_= (-1, 1)
        names_liste = ['Dance', 'Lightning', 'Earth', 'Waterfall']
        coordinates_liste = [(screen_size[0]*3/5,100), (270,200), (270,300), (290,400)]
        rotations_liste = [-10, -7, 3, 7]
        for a in range(len(names_liste)):
            win.blit(pygame.transform.rotozoom(images_list['attack_background'], rotations_liste[a], 1), coordinates_liste[a])
            #win.blit(pygame.transform.rotozoom(font_atk.render(f'{a+1}: ', True, (255,0,0)), rotations_liste[a], 1), (coordinates_liste[a][0]+35,coordinates_liste[a][1]+30))
            win.blit(pygame.transform.rotozoom(font_atk.render(f'{a+1}: '+names_liste[a], True, (255,255,255)), rotations_liste[a], 1), (coordinates_liste[a][0]+35,coordinates_liste[a][1]+30))
        """
        win.blit(pygame.transform.rotozoom(images_list['attack_background'], -10+a1, 1), (290,100))
        win.blit(pygame.transform.rotozoom(font_atk.render('1: ', True, (255,0,0)), -10+a1, 1), (325,130))
        win.blit(pygame.transform.rotozoom(font_atk.render('    Dance', True, (255,255,255)), -10+a1, 1), (325,130))

        a2 = 0
        win.blit(pygame.transform.rotozoom(images_list['attack_background'], -7+a2, 1), (270,200))
        win.blit(pygame.transform.rotozoom(font_atk.render('2: ', True, (255,0,0)), -7+a2, 1), (305,230))
        win.blit(pygame.transform.rotozoom(font_atk.render('    Lighting', True, (255,255,255)), -7+a2, 1), (305,230))

        a3 = 0
        win.blit(pygame.transform.rotozoom(images_list['attack_background'], 3+a3, 1), (270,300))
        win.blit(pygame.transform.rotozoom(font_atk.render('3: ', True, (255,0,0)), 3+a3, 1), (305,330))
        win.blit(pygame.transform.rotozoom(font_atk.render('    Waterfall', True, (255,255,255)), 3+a3, 1), (305,330))

        a4 = 0
        win.blit(pygame.transform.rotozoom(images_list['attack_background'], 7+a4, 1), (290,400))
        win.blit(pygame.transform.rotozoom(font_atk.render('4: ', True, (255,0,0)), 7+a4, 1), (325,430))
        win.blit(pygame.transform.rotozoom(font_atk.render('    Earth', True, (255,255,255)), 7+a4, 1), (325,430))
    """

    for index in range(len(my_creatures)):
        
        if _global_zoom!=1: 
            image=pygame.transform.rotozoom(my_creatures[index].image, 0,_global_zoom)
            if my_creatures[index]!=_zoomed_creature:
                image.fill((255, 255, 255, _alpha), None, pygame.BLEND_RGBA_MULT)
        else: 
            image=my_creatures[index].image

        (my_creatures[index].position[0] + (-image.get_size()[0]/2 + _global_zoom_point[0]))*_global_zoom+ _global_zoom_point[0]
        (my_creatures[index].position[1] + (-image.get_size()[1]/2 + _global_zoom_point[1]))*_global_zoom+ _global_zoom_point[1]

        +(_global_zoom_point[0]+my_creatures[index].position[0])*(_global_zoom-1)
        +(_global_zoom_point[1]+my_creatures[index].position[1])*(_global_zoom-1)

        #win.blit(image, (my_creatures[index].position[0]-image.get_size()[0]/2 + _global_zoom_point[0], my_creatures[index].position[1]+my_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]) )
        win.blit(image, (my_creatures[index].position[0]-image.get_size()[0]/2 + _global_zoom_point[0]+(_global_zoom_point[0]+my_creatures[index].position[0]-screen_size[0]/2)*(_global_zoom-1), my_creatures[index].position[1]+my_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]+(_global_zoom_point[1]+my_creatures[index].position[1]-screen_size[1]/2)*(_global_zoom-1)) )


    for index in range(len(oponent_creatures)):
        
        #if _global_zoom!=1: image=pygame.transform.rotozoom(oponent_creatures[index].image, 0,_global_zoom) 
        #else: image=oponent_creatures[index].image

        if _global_zoom!=1: 
            image=pygame.transform.rotozoom(oponent_creatures[index].image, 0,_global_zoom)
            if oponent_creatures[index]!=_zoomed_creature:
                image.fill((255, 255, 255, _alpha), None, pygame.BLEND_RGBA_MULT)
        else: 
            image=oponent_creatures[index].image

        win.blit(image, (oponent_creatures[index].position[0]-image.get_size()[0]/2 + _global_zoom_point[0]+(_global_zoom_point[0]+oponent_creatures[index].position[0]-screen_size[0]/2)*(_global_zoom-1), oponent_creatures[index].position[1]+oponent_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]+(_global_zoom_point[1]+oponent_creatures[index].position[1]-screen_size[1]/2)*(_global_zoom-1)) )

        #win.blit(image, (oponent_creatures[index].position[0]-image.get_size()[0]/2+ _global_zoom_point[0], oponent_creatures[index].position[1]+oponent_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]))

    show_turn_order(_order_y_offset, _order_first_opacity)

    pygame.display.update()


# main loop
while 1:
    draw()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        quit()
    if keys[pygame.K_z]:
        zoom_towards(my_creatures[0])
    if keys[pygame.K_e]:
        zoom_towards(my_creatures[1])
    if keys[pygame.K_r]:
        zoom_towards(my_creatures[2])
    if keys[pygame.K_t]:
        zoom_towards(oponent_creatures[1])
    if keys[pygame.K_q]:
        next_creature_order()
    if keys[pygame.K_f]:
        de_zoom()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
