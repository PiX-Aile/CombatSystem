_global_zoom = 1
_zoomed_creature = None
_alpha = 255
_zoom_max = 2 # before 2.4
_global_zoom_point = [0,0]

def zoom_towards(Creature):
    global _global_zoom 
    global _global_zoom_point 
    global _alpha
    global  _zoomed_creature
    
    _zoom_movement_speed = 20
    _old_global_zoom_point = _global_zoom_point[:]
    _old_global_zoom = _global_zoom

    _offset = (100, -50)

    _zoomed_creature = Creature

    for a in range(_zoom_movement_speed):
        if _alpha>255-150:
            _alpha -= 150/_zoom_movement_speed
        draw()
        if Creature.belongs_to_player:
            _global_zoom_point[0] += (-Creature.position[0]+screen_size[0]/2-_old_global_zoom_point[0]-_offset[0])/_zoom_movement_speed
            _global_zoom_point[1]+=(-Creature.position[1]+screen_size[1]*1/2-_old_global_zoom_point[1]-_offset[1])/_zoom_movement_speed # to get the creature centered
           
        else:
            _global_zoom_point[0] += (-Creature.position[0]+screen_size[0]/2-_old_global_zoom_point[0])/_zoom_movement_speed
            _global_zoom_point[1] += (-Creature.position[1]+screen_size[1]*1/2-_old_global_zoom_point[1])/_zoom_movement_speed # to get the creature centered
        if _global_zoom<_zoom_max:
            _global_zoom+=(_zoom_max-_old_global_zoom)/_zoom_movement_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
# dezooms
def de_zoom():
    global _global_zoom 
    global _global_zoom_point 
    global _alpha
    global  _zoomed_creature

    
    
    _zoom_movement_speed = 20
    _old_global_zoom_point = _global_zoom_point[:]
    _old_global_zoom = _global_zoom
    for a in range(_zoom_movement_speed):
        if _alpha<255:
            _alpha += 150/_zoom_movement_speed
        draw()
        _global_zoom_point[0] -= _old_global_zoom_point[0]/_zoom_movement_speed
        _global_zoom_point[1]-=_old_global_zoom_point[1]/_zoom_movement_speed
        _global_zoom -= (_old_global_zoom-1)/_zoom_movement_speed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    _global_zoom = 1
    _zoomed_creature = None









def show_turn_order(y_offset, _order_first_opacity):
    for index in range(len(turn_order)):
        creature = turn_order[index]
        creature_icon_margin = (70, 13)

        icon_image = creature.image_icon

        if creature.belongs_to_player:
            background_image = images_list["player_turn"].copy()
            #win.blit(creature.image_icon, (creature_icon_margin[0]+(-60 if index>0 else 0), index*60+creature_icon_margin[1]+y_offset))
        else:
            background_image = images_list["oponent_turn"].copy()
            #win.blit(creature.image_icon, (creature_icon_margin[0]+(-60 if index>0 else 0), index*60+creature_icon_margin[1]+y_offset))

        if _order_first_opacity!=255 and index==0:
            background_image.fill((255, 255, 255, _order_first_opacity), None, pygame.BLEND_RGBA_MULT)
            icon_image.fill((255, 255, 255, _order_first_opacity), None, pygame.BLEND_RGBA_MULT)

        win.blit(background_image, (-60 if index>0 else 0,index*60+y_offset))
        win.blit(icon_image, (creature_icon_margin[0]+(-60 if index>0 else 0), index*60+creature_icon_margin[1]+y_offset))


def next_creature_order():
    for a in range(30):
        draw(_order_y_offset = 0, _order_first_opacity = 255-a*4)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    for a in range(60):
        draw(_order_y_offset = -a, _order_first_opacity = 0)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    turn_order.pop(0)


    
    