import time
import random
import _thread

must_compute_turn_order = False

oponent_coordinates = {'x': 940,'y':290, 'y-offset':0}

def init_map(opponent): #server


    map = []

    map.append({'name': '_turn_order', 'data':[], 'y_to_add': 0}) # y to add useless
    map.append({'name': '_game_info', 'players_ids':[]})


    fake_screen_size = (1250*0.8,680*0.8) 
    #_opponent_coordinates = {'x': fake_screen_size[0]*10/11+50, 'y': fake_screen_size[1]*5/9, 'y-offset':0}
    _opponent_coordinates = oponent_coordinates
    map.append({'name':opponent.name+'-f','player':'opponent','position':_opponent_coordinates, 'hp':{'current': 180, 'full': 200},'atks':opponent.atks})

    return map



def _compute_turn_order(map):
    new_order = []
    possible_elements = []
    turn_order_index = -1


    for index in range(len(map)):
        if map[index]['name'] == "_turn_order":
            turn_order_index = index
            continue
        if not map[index].get('player'): # projectile
            continue
        if not( map[index]['name'].startswith("_")):
            possible_elements.append(index)
    
    for i in range(2):
        new_order.extend(possible_elements)
        
            
    map[turn_order_index]['data'] = new_order

def reduce_all_turn_order(map, current_index): # lighter version of turn order
    for a in map[0]["data"]:
        if a>=current_index:
            a-=1



def play(map, inputs): #server
    
    return map






all_coordinates = [


    [
            {'x': 370, 'y':460, 'y-offset': 1},
            {'x': 600, 'y': 440, 'y-offset': -2},
            {'x': 670, 'y': 490, 'y-offset': 1},
    ],
    
    [
            {'x': 370, 'y': 460, 'y-offset': 1},
            {'x': 550,'y': 440, 'y-offset': -2},
            {'x': 650,'y': 460, 'y-offset': 1},
            {'x': 740, 'y': 510, 'y-offset': 1}
    ]


]

def find_coordinates_for_player_initiation_server(nb):
    if nb==1:
        coordinates = all_coordinates[0]
        nb_poke = 3
    else:
        print("ohh ! 2 playwerrs")
        coordinates = all_coordinates[1]
        nb_poke = 2
    return coordinates, nb_poke




def player_initiation_client(server, my_poke, trainer_id, screen_size):
    local_map = []
    
    for poke in range(len(my_poke)):
        local_map.append({'name':my_poke[poke].name+'-b','player':trainer_id, 'hp':{'current': 130, 'full': 130},'atks':my_poke[poke].atks})
    return local_map





def client_attack(current_player_index, data, map, oponent, player_names):
    global current_turn_order_already_attacked
    if current_turn_order_already_attacked:
        return
    current_turn_order_already_attacked = 1
    for a in data:
        atk_name = map[map[0]['data'][0]]["atks"][a["selected_move"] - 1]
        
        #I have to find the creature_index of the current selected creature to be able to find the coordinates
        creature_index = 1
        for soul in range(len(map)):
            if map[soul].get("player")==player_names[current_player_index]:
                print(map[0]["data"][0], soul)
                if map[0]["data"][0] == soul:
                    break
                creature_index+=1
                
        
        print("launching attack")
        start_coordinates,_a = find_coordinates_for_player_initiation_server(len(map[1]["players_ids"]))
        start_coordinates = start_coordinates[creature_index-1+current_player_index*2]


        end_coordinates = oponent_coordinates

        if atk_name.startswith("dash_"):
            start_coordinates = {"x": start_coordinates["x"], "y": start_coordinates["y"]}
            _thread.start_new_thread(dash_attack_animation, (map, map[map[0]["data"][0]], end_coordinates, start_coordinates, atk_name, map[2]))
            

            
        else:
            start_coordinates = {"x": start_coordinates["x"]-30, "y": start_coordinates["y"]-30}

            _thread.start_new_thread(attack_animation, (map, atk_name, start_coordinates, end_coordinates, map[2]))
        
        #_compute_turn_order(map)
                

def dash_attack_animation(map, attacker, end_coordinates, start_coordinates, atk_name, target):
    time.sleep(1)
    global current_turn_order_already_attacked
    # dash
    print("starting attack animation")
    print(attacker)

    true_destination = {"x": end_coordinates["x"]-10, "y": end_coordinates["y"]+20} 

    
    attacker['arrival_time'] = 0.8
    print("starting at", time.time())
    attacker['starting_time'] = int(time.time()*10)/10
    attacker['destination']= true_destination

    if start_coordinates["y"] > end_coordinates["y"] :
        attacker['zoom'] = 0.8
    else:
        attacker['zoom'] = 1.2

    time.sleep(1)
    # explosion
    map_index = len(map)
    map.append({'name': atk_name, 'position': start_coordinates, 'destination': {"x": end_coordinates["x"]+40, "y": end_coordinates["y"]+10}, 'arrival_time': 0.1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.7})

    time.sleep(0.2)
    # going back
    attacker['position'] = true_destination
    attacker['destination']= start_coordinates
    attacker['arrival_time'] = 0.6
    del attacker['zoom']
    attacker['starting_time'] = int(time.time()*10)/10


    deal_damage(target, map[map_index])
    time.sleep(1)
    
    current_turn_order_already_attacked = 0
    
    del map[0]["data"][0]
    attacker['position'] = start_coordinates
    
    del map[map_index] # index of projectile

def attack_animation(map, atk_name, start_coordinates, end_coordinates, target):
    time.sleep(1)
    time.sleep(1)
    global current_turn_order_already_attacked
    map_index = len(map)
    map.append({'name': atk_name, 'position': start_coordinates, 'destination': end_coordinates, 'arrival_time': 1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.5})
    
    if atk_name.startswith("Multi_"):
        for i in range(10):
            map.append({'name': atk_name, 'position': {'x':start_coordinates['x'] -50*random.randint(-4,4), 'y':start_coordinates['y'] -50*random.randint(-4,4)}, 'destination': end_coordinates, 'arrival_time': 1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.5})

    #map.append({'name': atk_name, 'position': end_coordinates, 'destination': end_coordinates, 'arrival_time': 0.2, 'starting_time': int(time.time()*10)/10, 'explosion_time': 5})
    
    time.sleep(1)
    deal_damage(target, map[map_index])
    time.sleep(1)
   
    current_turn_order_already_attacked = 0
    
    del map[0]["data"][0] # turn order
    
    del map[map_index] # index of projectile
    if atk_name.startswith("Multi_"):
        for i in range(10):
            del map[map_index]



current_turn_order_already_attacked = 0
def ennemy_attack(map, opponent_index): # called only if ennemy is in first
    global current_turn_order_already_attacked
    if current_turn_order_already_attacked:
        return
    current_turn_order_already_attacked = 1
    print("called")
    start_coordinates = oponent_coordinates

    target = random.randint(0,2)

    

    end_coordinates,_a = find_coordinates_for_player_initiation_server(len(map[1]["players_ids"]))
    end_coordinates = end_coordinates[target]

    target_element = None
    for i in map:

        if (i.get("destination") and i.get("destination").get("x") == end_coordinates.get("x") and i.get("destination").get("y") == end_coordinates.get("y")) or (i.get("position") and i.get("position").get("x") == end_coordinates.get("x") and i.get("position").get("y") == end_coordinates.get("y")):
            target_element = i
    

    end_coordinates = {"x": end_coordinates["x"]-10, "y": end_coordinates["y"]-30}

    atk_name = random.choice(map[opponent_index]["atks"])
    
    if atk_name.startswith("dash_"):
        #map.append({'name': atk_name, 'position': start_coordinates, 'destination': {"x": end_coordinates["x"]+40, "y": end_coordinates["y"]+10}, 'arrival_time': 0.1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.5})
        _thread.start_new_thread(dash_attack_animation, (map, map[opponent_index], end_coordinates, start_coordinates, atk_name, target_element))
 
    else:
        
        
        _thread.start_new_thread(attack_animation, (map, atk_name, start_coordinates, end_coordinates, target_element))
        
    




def deal_damage(target, projectile): 
    target['hp']['current']-=30
    if target['hp']['current']<0:
        target['hp']['current'] = 0

    
        
