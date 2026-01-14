import time
import random

must_compute_turn_order = False

def init_map(opponent): #server


    map = []

    map.append({'name': '_turn_order', 'data':[], 'y_to_add': 0}) # y to add useless
    map.append({'name': '_game_info', 'players_ids':[]})


    fake_screen_size = (1250*0.8,680*0.8) 
    _opponent_coordinates = {'x': fake_screen_size[0]*10/11+50, 'y': fake_screen_size[1]*5/9, 'y-offset':0}
    map.append({'name':opponent.name+'-f','player':'opponent','position':_opponent_coordinates, 'hp':'130,130'})





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
        if not( "_" in map[index]['name']):
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









def find_coordinates_for_player_initiation_server(nb):
    fake_screen_size = (1250*0.8,680*0.8) 
    if nb==1:
        coordinates = [
            {'x': int(fake_screen_size[0]/4-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8)+30, 'y-offset': 1},
            {'x': fake_screen_size[0]/4+240-10+128*2.4/1.3*0.8, 'y': int(fake_screen_size[1]*3/6-15+128*2.4/1.3*0.8)+30, 'y-offset': -2},
            {'x': int(fake_screen_size[0]/4+320-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+60-15+128*2.4/1.3*0.8)+30, 'y-offset': 1},
        ]
        nb_poke = 3
    else:
        print("ohh ! 2 playwerrs")
        coordinates = [
            {'x': int(fake_screen_size[0]/4-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8)+30, 'y-offset': 1},
            {'x': fake_screen_size[0]/4+180-10+128*2.4/1.3*0.8, 'y': int(fake_screen_size[1]*3/6-15+128*2.4/1.3*0.8)+30, 'y-offset': -2},
            {'x': int(fake_screen_size[0]/4+300+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8)+30, 'y-offset': 1},
            {'x': int(fake_screen_size[0]/4+350-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+60-15+128*2.4/1.3*0.8)+30, 'y-offset': 1},
        ]
        nb_poke = 2
    return coordinates, nb_poke




def player_initiation_client(server, my_poke, trainer_id, screen_size):
    local_map = []
    
    for poke in range(len(my_poke)):
        local_map.append({'name':my_poke[poke].name+'-b','player':trainer_id, 'hp':'130,130'})
    return local_map





def client_attack(current_player_index, data, map, oponent, player_names):
    for a in data:
        
        atk_name, creature_index = a["move_name"], a["creature_index"]
        base_creature_index = creature_index
        #tunr_order
        selected_sould_index_in_map = -1
        for soul in range(len(map)):
            if map[soul].get("player")==player_names[current_player_index]:
                creature_index -=1
                if creature_index == 0: # found selected pokemon
                    selected_sould_index_in_map = soul
                    break
        # check
        
        if map[0]["data"][0] != selected_sould_index_in_map:
            
            return
        
        print(creature_index)
        print("launching attack")
        start_coordinates,_a = find_coordinates_for_player_initiation_server(len(map[1]["players_ids"]))
        start_coordinates = start_coordinates[base_creature_index-1+current_player_index*2]
        start_coordinates = {"x": start_coordinates["x"]-30, "y": start_coordinates["y"]-30}
        fake_screen_size = (1250*0.8,680*0.8) 
        end_coordinates = {'x': fake_screen_size[0]*10/11+50, 'y': fake_screen_size[1]*5/9}
        map.append({'name': atk_name, 'position': start_coordinates, 'destination': end_coordinates, 'arrival_time': 1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.5})

        del map[0]["data"][0]
        
        #_compute_turn_order(map)
                

def ennemy_attack(map, opponent): # called only if ennemy is in first
    print("called")
    fake_screen_size = (1250*0.8,680*0.8) 
    start_coordinates = {'x': fake_screen_size[0]*10/11+50, 'y': fake_screen_size[1]*5/9}
    target = random.randint(0,2)

    end_coordinates,_a = find_coordinates_for_player_initiation_server(len(map[1]["players_ids"]))
    end_coordinates = end_coordinates[target]
    end_coordinates = {"x": end_coordinates["x"]-30, "y": end_coordinates["y"]-30}

    map.append({'name': random.choice(opponent.atks), 'position': start_coordinates, 'destination': end_coordinates, 'arrival_time': 1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.5})

    del map[0]["data"][0]
    



