import time
import requests
import game_logics


def multiplayer(battle_id, opponent): #main.py

    opponent = {'name':opponent.name+'-f','player':'opponent','position':[],'atks':opponent.atks}
    url = 'http://pixailesoulweaver.pythonanywhere.com/StartBattle/'+battle_id+"/"+str(opponent)
    #url = 'http://127.0.0.1:8000/Send/'+player_name+'/'+str((player.get_pos()[0], player.get_pos()[1], player.direction, int(time.time())))
    #url = 'http://127.0.0.1:8000/StartBattle/'+battle_id+"/"+str(opponent)
    print(url)
    while 1:
        try:
            req = requests.get(url, 'html.parser')
        except:
            print("server down")
            exit()


        
        try:
            my_dict= eval(req.text.replace("&#x27;", "'").replace("&quot;", """ " """))
            break
        except:
            print("errrror : ", req.text)
    server = my_dict["url"]
    print("received url !!!", server)
    return server

#serveur vaut : http://localhost:8000/Battle/UID/

def player_initiation_client(server, my_poke, trainer_id, screen_size, how_many_poke): #client
    print("init")
    local_map = game_logics.player_initiation_client(server, my_poke, trainer_id, screen_size, how_many_poke)
    url = server+"Initialize_player/"+str(local_map)
    try:
        req = requests.get(url, 'html.parser')
    except:

        print("error 2")


def load_info(server, data):
    
    url = server+"ExchangeData/"+str(data)

    
    req = requests.get(url, 'html.parser')
    try:
        my_list = eval(req.text.replace("&#x27;", "'").replace("&quot;", """ " """))
    except SyntaxError:
        print("error !!!", req.text)
        return
        
    
    return my_list



