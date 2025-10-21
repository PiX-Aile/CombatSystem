import pygame
import os
import time
import random

path_images=os.path.join(os.getcwd(),"Images")

screen_size = (1250,680)
win = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Combat")
pygame.init()
#main_font=pygame.font.Font(None,25)



# load images
def load_images():
    images_list = {}
    for name in os.listdir(path_images):
        if ".png" in name :
            image = pygame.image.load(os.path.join(path_images, name))
            if name == "background.png": 
                image=pygame.transform.rotozoom(image, 0, 0.65)
            elif name == "player_turn.png": 
                image=pygame.transform.rotozoom(image, 0, 0.2)
            elif name == "oponent_turn.png": 
                image=pygame.transform.rotozoom(image, 0, 0.03)
            else:
                if "-b" in name:
                    image = pygame.transform.rotozoom(image, 0, 2)
                if "-f" in name:
                    image = pygame.transform.rotozoom(image, 0, 2)
            images_list[name.split(".")[0]] = image
    return images_list
images_list = load_images()

print(images_list)

class Creature:
    def __init__(self, name, belongs_to_player, position):
        self.name = name
        self.belongs_to_player = belongs_to_player
        print(name + ("-b" if belongs_to_player else "-f") )
        self.image = images_list[ name + ("-b" if belongs_to_player else "-f") ]
        self.image_icon = pygame.transform.rotozoom(images_list[ name +  "-f" ], 0, 0.2)
        self.image_base_size = self.image.get_size()
        print(self.image_base_size)
        self.position = position

        self._random_movement = random.randint(0,5)
    def _get_random_movement(self):
        self._random_movement+=random.randint(-2,2)/10
        return self._random_movement




# creation of pokemon for player 
my_creatures = []
_names = ["Mini-jack", "Minishrum", "Mini-jack"]
_pos=[(screen_size[0]/5+96, screen_size[1]*3/5+96), 
             (screen_size[0]/5+190+96, screen_size[1]*3/5+30-10+96),
             (screen_size[0]/5+130+96, screen_size[1]*3/5+100+96),
             (screen_size[0]/5+60+96, screen_size[1]*3/5+85+96)
             ]
for index in range(len(_names)):
    my_creatures.append(Creature(_names[index], True, _pos[index]))

# creation of pokemon for oponent 
oponent_creatures = []
_names = ["Minishrum", "Mini-jack"]
_pos2=[
            (screen_size[0]*4/5+70, screen_size[1]*2.3/5+96),
            (screen_size[0]*4/5+160, screen_size[1]*2.3/5+96),
        ]
for index in range(len(_names)):
    oponent_creatures.append(Creature(_names[index], False, _pos2[index]))




turn_order = my_creatures[:];turn_order.extend(oponent_creatures)






_global_zoom = 1
_zoom_max = 2
_global_zoom_point = [0,0]
def zoom_towards(Creature):
    global _global_zoom 
    global _global_zoom_point 
    
    _zoom_movement_speed = 40
    _old_global_zoom_point = _global_zoom_point[:]
    _old_global_zoom = _global_zoom
    for a in range(_zoom_movement_speed):
        draw()
        if Creature.belongs_to_player:
            _global_zoom_point[0] += (-Creature.position[0]+screen_size[0]/2-_old_global_zoom_point[0])/_zoom_movement_speed
            _global_zoom_point[1]+=(-Creature.position[1]+screen_size[1]*1/2-_old_global_zoom_point[1])/_zoom_movement_speed # to get the creature centered
            _global_zoom+=_zoom_max/_zoom_movement_speed * (1/_old_global_zoom)
        else:
            _global_zoom_point[0] += (-Creature.position[0]+screen_size[0]/2-_old_global_zoom_point[0])/_zoom_movement_speed
            _global_zoom_point[1] += (-Creature.position[1]+screen_size[1]*1/2-_old_global_zoom_point[1])/_zoom_movement_speed # to get the creature centered
            _global_zoom+=_zoom_max/_zoom_movement_speed* (1/_old_global_zoom)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    
def de_zoom():
    global _global_zoom 
    global _global_zoom_point 
    
    _zoom_movement_speed = 30
    _old_global_zoom_point = _global_zoom_point[:]
    _old_global_zoom = _global_zoom
    for a in range(_zoom_movement_speed):
        draw()
        _global_zoom_point[0] -= _old_global_zoom_point[0]/_zoom_movement_speed
        _global_zoom_point[1]-=_old_global_zoom_point[1]/_zoom_movement_speed
        _global_zoom -= (_old_global_zoom-1)/_zoom_movement_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    _global_zoom = 1




# drawing function
def draw():
    win.fill((0,0,0))

    if _global_zoom!=1: image=pygame.transform.rotozoom(images_list["background"], 0,_global_zoom) 
    else: image=images_list["background"]
    win.blit(image, (_global_zoom_point[0]+(_global_zoom_point[0]-screen_size[0]/2)*(_global_zoom-1), _global_zoom_point[1]+(_global_zoom_point[1]-screen_size[1]/2)*(_global_zoom-1)))


    image_position_randomizer = int(time.time()*10)%5



    for index in range(len(my_creatures)):
        
        if _global_zoom!=1: image=pygame.transform.rotozoom(my_creatures[index].image, 0,_global_zoom) 
        else: image=my_creatures[index].image

        (my_creatures[index].position[0] + (-image.get_size()[0]/2 + _global_zoom_point[0]))*_global_zoom+ _global_zoom_point[0]
        (my_creatures[index].position[1] + (-image.get_size()[1]/2 + _global_zoom_point[1]))*_global_zoom+ _global_zoom_point[1]

        +(_global_zoom_point[0]+my_creatures[index].position[0])*(_global_zoom-1)
        +(_global_zoom_point[1]+my_creatures[index].position[1])*(_global_zoom-1)

        #win.blit(image, (my_creatures[index].position[0]-image.get_size()[0]/2 + _global_zoom_point[0], my_creatures[index].position[1]+my_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]) )
        win.blit(image, (my_creatures[index].position[0]-image.get_size()[0]/2 + _global_zoom_point[0]+(_global_zoom_point[0]+my_creatures[index].position[0]-screen_size[0]/2)*(_global_zoom-1), my_creatures[index].position[1]+my_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]+(_global_zoom_point[1]+my_creatures[index].position[1]-screen_size[1]/2)*(_global_zoom-1)) )


    for index in range(len(oponent_creatures)):
        
        if _global_zoom!=1: image=pygame.transform.rotozoom(oponent_creatures[index].image, 0,_global_zoom) 
        else: image=oponent_creatures[index].image
        win.blit(image, (oponent_creatures[index].position[0]-image.get_size()[0]/2 + _global_zoom_point[0]+(_global_zoom_point[0]+oponent_creatures[index].position[0]-screen_size[0]/2)*(_global_zoom-1), oponent_creatures[index].position[1]+oponent_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]+(_global_zoom_point[1]+oponent_creatures[index].position[1]-screen_size[1]/2)*(_global_zoom-1)) )

        #win.blit(image, (oponent_creatures[index].position[0]-image.get_size()[0]/2+ _global_zoom_point[0], oponent_creatures[index].position[1]+oponent_creatures[index]._get_random_movement()-image.get_size()[1]/2+ _global_zoom_point[1]))

    for index in range(len(turn_order)):
        creature = turn_order[index]
        creature_icon_margin = (70, 13)
        if creature.belongs_to_player:
            win.blit(images_list["player_turn"], (-60 if index>0 else 0,index*60))
            win.blit(creature.image_icon, (creature_icon_margin[0]+(-60 if index>0 else 0), index*60+creature_icon_margin[1]))
        else:
            win.blit(images_list["player_turn"], (-60 if index>0 else 0,index*60))
            win.blit(creature.image_icon, (creature_icon_margin[0]+(-60 if index>0 else 0), index*60+creature_icon_margin[1]))


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
    if keys[pygame.K_f]:
        de_zoom()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           pygame.quit()
