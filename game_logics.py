must_compute_turn_order = False

def init_map(opponent): #server


    map = []

    map.append({'name': '_turn_order', 'data':[]})
    map.append({'name': '_game_info', 'players_ids':[]})


    fake_screen_size = (1250*0.8,680*0.8) 
    _opponent_coordinates = {'x': fake_screen_size[0]*10/11+50, 'y': fake_screen_size[1]*5/9, 'y-offset':0}
    map.append({'name':opponent.name+'-f','player':'opponent','position':_opponent_coordinates, 'hp':'130,130'})





    return map



def _compute_turn_order(map):
    new_order = []
    turn_order_index = -1
    for index in range(len(map)):
        if map[index]['name'] == "_turn_order":
            turn_order_index = index
            continue
        if not( "_" in map[index]['name']):
            new_order.append(index)
    print("new_order:", new_order)
    map[turn_order_index]['data'] = new_order



def play(map, inputs): #server
    
    return map









def player_initiation_client(server, my_poke, trainer_id, screen_size):
    local_map = []
    
    for poke in range(len(my_poke)):
        local_map.append({'name':my_poke[poke].name+'-b','player':trainer_id, 'hp':'130,130'})
    return local_map
