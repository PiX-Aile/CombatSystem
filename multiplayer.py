import pickle
import socket
import time
import random
from _thread import *

import game_logics

max_player_nb = 2

socket.timeout(4000)

def multiplayer(battle_id, opponent): #main.py
    #server_addr, server_port = "2.tcp.ngrok.io", 19757
    server_addr, server_port = "localhost", 8000

    with open("server_list.txt", "r") as f:
        empty_port_found = 0
        current_index = 0
        empty_port_port = 8000;
        empty_addr_global, empty_port_global = None, None 
        for server in f.readlines():
            server_addr, server_port = server.split(", ")
            
            try:
                a = connect(server_addr, int(server_port), battle_id) 
                # has found server
                if a==0: # different battle_id
                    print("Found server but different id")
                else: # same battle_id
                    print("Found perfect server")
                    return a # has found right server

            except (ConnectionRefusedError, EOFError, socket.gaierror) as f: # no server at that ip

                print("no server at that ip, error message:", str(f))
                if empty_port_found==0:
                    empty_port_port += current_index
                    empty_port_found = 1
                    empty_addr_global = server_addr
                    empty_port_global = server_port

            current_index+=1
            
        return launch_server(battle_id, empty_addr_global, int(empty_port_global), empty_port_port, opponent)


def connect(server_addr, server_port, battle_id):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print("Client trying to connect to :", server_addr, server_port)
                
    time.sleep(0.1)
    s.connect((server_addr, server_port))

    # client 
    if (pickle.loads(s.recv(10000))==battle_id):
        print("Client successfully connected at server and port: ", server_addr, server_port)
        s.send(pickle.dumps(1))
        return s

    else:
        print("Server found but not same battle, trying with port+1")
        s.send(pickle.dumps(0))
        
        return 0


liste_connected = []
player_names = []

map = []

def server(oponent):#server
    global map
    inputs = []
    map = game_logics.init_map(oponent)

    timea = 0

    while 1:
        timea += 1
        #if (timea)%20==0:
        #    map.append({'name': random.choice(['SAlec', 'SElec', 'SFire']), 'position': {'x': 630, 'y': 380}, 'destination': {'x': 630, 'y': 380}, 'arrival_time': 0.1, 'starting_time': int(time.time()*10)/10, 'explosion_time': 0.7})
        if (timea)%20==0:#time for cleanup
            current_index = 0
            for el in map:
                if not el.get("player") and not "_" in el['name']:# is projectile
                    if el['starting_time']+el['arrival_time']+el['explosion_time']<time.time():
                        del map[current_index]
                        # reduce all turn_order
                        game_logics.reduce_all_turn_order(map, current_index)
                        
                        #game_logics._compute_turn_order(map)
                        current_index -=1
                if el.get("destination") and int(el['position']['x']) == int(el['destination']['x']) and int(el['position']['y']) == int(el['destination']['y']):
                    if el.get("player"): # not a projectile:
                        print("destination no longer needed for :", el['name'])
                        del el['destination']
                        

                        
                current_index +=1
            
            
            # ennemy attack ?
            if map[map[0]["data"][0]]["player"] == "opponent":
                game_logics.ennemy_attack(map, oponent)
            

            
        map = game_logics.play(map, inputs)
        current_player_index = 0
        for conn in liste_connected:
            time.sleep(0.02)
            try:
                data = pickle.loads(conn.recv(10000))
                if data!=[]:
                    player_names = map[1]["players_ids"]
                    game_logics.client_attack(current_player_index, data, map, oponent, player_names)
                conn.send(pickle.dumps(map))
            except BrokenPipeError:
                print("Second player disconnected")
                map[1]['players_ids'].pop(1)
                liste_connected.pop(1)
                game_logics._compute_turn_order(map)
            current_player_index += 1 
        time.sleep(0.05)


def search_for_clients(s, battle_id): #server
    global map
    nb = 0
    while nb<max_player_nb:
        conn, addr = s.accept() # waits for and accepts the new client
        print()
        print("Connected to:",addr,"        ",time.localtime().tm_hour,"h ",time.localtime().tm_min,"min ",time.localtime().tm_sec,"s")
        conn.send(pickle.dumps(battle_id))
        if pickle.loads(conn.recv(1000))==1:
            print("Client accepted, same battle")
            liste_connected.append(conn)
            player_initiation_server(conn)
            
            
            nb+=1
            
        else:
            print("Client refused, wrong battle")
            
    print("Stopping search")

def launch_server(battle_id, server_addr, server_port, local_port, opponent):#server
    print("Trying to create server ", local_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while 1:
        try:
            s.bind(("localhost", local_port))
            break
        except(OSError):
            pass
    print("Created server ! at port: ", local_port)
    print("\n")
    
    s.listen(10) # 10 = max number of clients

    start_new_thread(server, (opponent, ))
    start_new_thread(search_for_clients,(s,battle_id))
    
    #return multiplayer(battle_id, opponent)
    return connect("localhost", local_port, battle_id)










#client bloqué là
def load_info(server, data_to_send): # client
    try:
        server.send(pickle.dumps(data_to_send))
        return pickle.loads(server.recv(5000))
    except pickle.UnpicklingError:
        print("Error caught in servor")




def player_initiation_server(conn): #server
    print("initialising new plaer")
    data = pickle.loads(conn.recv(2000)) # serveur bloqué là

    map[1]['players_ids'].append(data[0]['player'])
    
    coordinates, nb_poke = game_logics.find_coordinates_for_player_initiation_server(len(liste_connected))
    if len(liste_connected)!=1:
        # finding last pokemon
        index = -1
        while not map[index].get("player"):
            index-=1
        map.pop(index)

    for a in range(nb_poke):
        map.append(data[a])
    nb = 0
    for el in map:
        if (not "_" in el['name'] and el.get('player') and el['player']!='opponent'):
            if el.get("position"): # on déplace les 2 premiers poke
                el['destination'] = coordinates[nb]
                el['arrival_time'] = 0.5
                el['starting_time'] = int(time.time()*10)/10
            else:
                el['position'] = coordinates[nb]

            nb+=1
    
    #map[1]["players_ids"].append(player_id)
    game_logics._compute_turn_order(map)
    


def player_initiation_client(server, my_poke, trainer_id, screen_size): #client
    player_names.append(trainer_id)
    local_map = game_logics.player_initiation_client(server, my_poke, trainer_id, screen_size)
    server.send(pickle.dumps(local_map))

