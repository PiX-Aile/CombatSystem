import pickle
import socket
import time
from _thread import *

import game_logics

max_player_nb = 2

socket.timeout(4000)

def multiplayer(battle_id, opponent): #main.py
    #server_addr, server_port = "2.tcp.ngrok.io", 19757
    server_addr, server_port = "localhost", 8000
    return try_connect(battle_id, server_addr, server_port, opponent)


def try_connect(battle_id, server_addr, server_port, opponent): # both client and server
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        s.connect((server_addr, server_port))

        # client 
        if (pickle.loads(s.recv(100000))==battle_id):
            print("Client successfully connected at port: ", server_port)
            s.send(pickle.dumps(1))
            return s

        else:
            print("Server found but not same battle, trying with port+1")
            s.send(pickle.dumps(0))
            
            return try_connect(battle_id, server_addr, server_port+1, opponent)
        
    except (ConnectionRefusedError):# il n'y avait pas de serveur ou sinon un effacé
        
        try: # pas de serveur
            return launch_server(battle_id, server_addr, server_port, opponent)
        except: # en fait, c'était un effacé
            print("whaaaa")
            return try_connect(battle_id, server_addr, server_port+1, opponent)

        

        try_connect(battle_id, server_addr, server_port+1, opponent)
        #return try_connect(battle_id, server_addr, server_port+1, opponent)
        


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

    nb = 0
    while nb<max_player_nb:
        conn, addr = s.accept() # waits for and accepts the new client
        print()
        print("Connected to:",addr,"        ",time.localtime().tm_hour,"h ",time.localtime().tm_min,"min ",time.localtime().tm_sec,"s")
        conn.send(pickle.dumps(battle_id))
        if pickle.loads(conn.recv(1000))==1:
            print("Client accepted, same battle")
            player_initiation_server(conn)
            liste_connected.append(conn)
            nb+=1
            
        else:
            print("Client refused, wrong battle")
            
    print("Stopping search")

def launch_server(battle_id, server_addr, server_port, opponent):#server
    print("Trying to create server ", server_port)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server_addr, server_port))
    print("Created server ! at port: ", server_port)
    
    s.listen(10) # 10 = max number of clients

    start_new_thread(search_for_clients,(s,battle_id))
    start_new_thread(server, (opponent, ))
    return try_connect(battle_id, server_addr, server_port, opponent)










#client bloqué là
def load_info(server): # client
    return pickle.loads(server.recv(5000))




def player_initiation_server(conn): #server
    data = pickle.loads(conn.recv(2000)) # serveur bloqué là
    for a in data:
        map.append(a)
    game_logics._compute_turn_order(map)
    


def player_initiation_client(server, my_poke, trainer_id, screen_size): #client
    player_names.append(trainer_id)
    local_map = game_logics.player_initiation_client(server, my_poke, trainer_id, screen_size)
    server.send(pickle.dumps(local_map))

