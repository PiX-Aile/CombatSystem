import pickle
import socket
import time
from _thread import *

import game_logics

max_player_nb = 3

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

            except (ConnectionRefusedError, EOFError) as f: # no server at that ip

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

    while 1:
        map = game_logics.play(map, inputs)
        for conn in liste_connected:
            conn.send(pickle.dumps(map))
        time.sleep(1/30)


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
    return connect(server_addr, server_port, battle_id)










#client bloqué là
def load_info(server): # client
    return pickle.loads(server.recv(5000))




def player_initiation_server(conn): #server
    print("initialising new plaer")
    data = pickle.loads(conn.recv(2000)) # serveur bloqué là

    fake_screen_size = (1250*0.8,680*0.8) 
    
    if len(liste_connected)==1:
        coordinates = [
            {'x': int(fake_screen_size[0]/4-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8), 'y-offset': 1},
            {'x': fake_screen_size[0]/4+240-10+128*2.4/1.3*0.8, 'y': int(fake_screen_size[1]*3/6-15+128*2.4/1.3*0.8), 'y-offset': -2},
            {'x': int(fake_screen_size[0]/4+320-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+60-15+128*2.4/1.3*0.8), 'y-offset': 1},
        ]
        nb_poke = 3
    else:
        print("ohh ! 2 playwerrs")
        coordinates = [
            {'x': int(fake_screen_size[0]/4-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8), 'y-offset': 1},
            {'x': fake_screen_size[0]/4+240-10+128*2.4/1.3*0.8, 'y': int(fake_screen_size[1]*3/6-15+128*2.4/1.3*0.8), 'y-offset': -2},
            {'x': int(fake_screen_size[0]/4+300+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+3-15+20+128*2.4/1.3*0.8), 'y-offset': 1},
            {'x': int(fake_screen_size[0]/4+350-10+128*2.4/1.3*0.8), 'y': int(fake_screen_size[1]*3/6+60-15+128*2.4/1.3*0.8), 'y-offset': 1},
        ]
        nb_poke = 2
        map.pop(-1)

    for a in range(nb_poke):
        map.append(data[a])
    nb = 0
    for el in map:
        if (not "_" in el['name'] and el['player']!='opponent'):
            el['position'] = coordinates[nb]
            nb+=1
    
    #map[1]["players_ids"].append(player_id)
    game_logics._compute_turn_order(map)
    


def player_initiation_client(server, my_poke, trainer_id, screen_size): #client
    player_names.append(trainer_id)
    local_map = game_logics.player_initiation_client(server, my_poke, trainer_id, screen_size)
    server.send(pickle.dumps(local_map))

