
def multiplayer(battle_id, opponent): #main.py
    print(opponent)
    opponent = {'name':opponent.name+'-f','player':'opponent','position':_opponent_coordinates, 'hp':{'current': 360, 'full': 400},'atks':opponent.atks}
    url = 'http://pixailesoulweaver.pythonanywhere.com/StartBattle/'+battle_id+opponent
    #url = 'http://127.0.0.1:8000/Send/'+player_name+'/'+str((player.get_pos()[0], player.get_pos()[1], player.direction, int(time.time())))

    try:
        req = requests.get(url, 'html.parser')
    except:

        print("error l")
        return