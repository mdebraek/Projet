import blessed, time
def load_map(map_file_path:str)->dict:
    """Load the map files and return their data in the form of a dictionnary
    
    Parameters
    ----------
    map_file_path : absolute path of the file (str)
    
    Returns
    -------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    
    Version
    -------
    specification: Mitta Kylian, De Braekeleer Mickaël (v.1 20/02/25)
    implementation: De Braekeleer Mickaël (v1 26/02/25)
    """
    #init game data dict with basic info
    game_data={"map":None, "player1":{"call":10, "apprentices":{}, "dragon":{}}, "player2":{"call":10, "apprentices":{}, "dragon":{}}, "eggs":{}}
    #open the file of the map
    map=open(map_file_path, "r")
    #get all data lines inside a list (list of lines)
    raw_data=map.readlines()
    #close the map file
    map.close()
    
    #search in all lines for data
    for line in range (len(raw_data)):
        if raw_data[line].split(":")[0] =="map":
            info=raw_data[line+1].split(" ")
            game_data["map"]=[int(info[0]), int(info[1])]
        elif raw_data[line].split(":")[0] == "apprentices":
            line+=1
            while raw_data[line].split(":")[0] !="eggs":
                info=raw_data[line].split(" ")
                if info[0]==1:
                    game_data["player1"]["apprentices"][info[1]]={}
                    game_data["player1"]["apprentices"][info[1]]["pos"]=[int(info[2]), int(info[3])]
                    game_data["player1"]["apprentices"][info[1]]["max_health"]=int(info[4])
                    game_data["player1"]["apprentices"][info[1]]["current_health"]=int(info[4])
                    game_data["player1"]["apprentices"][info[1]]["regeneration"]=int(info[5][0:1])
                else:
                    game_data["player2"]["apprentices"][info[1]]={}
                    game_data["player2"]["apprentices"][info[1]]["pos"]=[int(info[2]), int(info[3])]
                    game_data["player2"]["apprentices"][info[1]]["max_health"]=int(info[4])
                    game_data["player2"]["apprentices"][info[1]]["current_health"]=int(info[4])
                    game_data["player2"]["apprentices"][info[1]]["regeneration"]=int(info[5][0:1])      
                line+=1
        elif raw_data[line].split(":")[0]=="eggs":
            for eggs in range (len(raw_data)-line):
                line+=1
                info=raw_data[line].split(" ")
                game_data["eggs"][info[0]]={}
                game_data["eggs"][info[0]]["pos"]=[int(info[1]), int(info[2])]
                game_data["eggs"][info[0]]["time_to_hatch"]=int(info[3])
                game_data["eggs"][info[0]]["max_health"]=int(info[4])
                game_data["eggs"][info[0]]["current_health"]=int(info[4])
                game_data["eggs"][info[0]]["attack_damage"]=int(info[5])
                game_data["eggs"][info[0]]["attack_range"]=int(info[6])
                game_data["eggs"][info[0]]["regeneration"]=int(info[7][0:1])
                if line == len(raw_data)-1:  
                    return game_data

#example   
map_path="C:/Users/coram/OneDrive/Desktop/projet/map.drk" 
game_data=load_map(map_path)

def info_bracket(player:str,game_data: dict)->list:
    """generate info bracket for a player

    Parameters
    ----------
    player : 
    game_data : 

    Version
    -------
    specification: Mitta Kylian (v.1 20/02/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël (v.1 27/02/25)
    
    """
    player_info=[]
    for apprentice in game_data[player]["apprentices"]:
        player_info.append(f"   -{apprentice} :")
        player_info.append(f"   >PV : {game_data[player]["apprentices"]["apprentice"]["current_health"]}/{game_data[player]["apprentices"]["apprentice"]["max_health"]}")
        position=game_data[player]["apprentices"]["apprentice"]["pos"]
        player_info.append(f"   >pos : {position[0]} {position[1]} ")
    for dragon in game_data[player]["dragon"]:
        if dragon==game_data[player]["dragon"][0]:
            player_info.append(f"-Dragon🐉:")
        player_info.append(f"   -{dragon}:")
        player_info.append(f"   >PV : {game_data[player]["dragon"][dragon]["current_health"]}/{game_data[player]["dragon"][dragon]["max_health"]}")
        player_info.append(f"   >Dégats : {game_data[player]["dragon"][dragon]["attack_damage"]}")
        player_info.append(f"   >Portée : {game_data[player]["dragon"][dragon]["attack_range"]}")
        position=game_data[player]["dragon"][dragon]["pos"]
        player_info.append(f"   >pos : {position[0]} {position[1]} ")
    
    

def display(game_data: dict):
    """Generate the display screen
    
    Parameters
    ----------
    game_data : dictionnary of all game data(dict)
    
    Version
    -------
    specification: Mitta Kylian, De Braekeleer Mickaël (v.1 20/02/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël (v.1 27/02/25)
    """
    #initial clear
    print(term.home + term.clear + term.hide_cursor)
    
    #initial map size
    Size_X = game_data["map"][0]
    Size_Y = game_data["map"][1]
    
    #initial info bracket
    player_1=["Player 1 :", "-Apprenti🚹:"]
    player_2=["Player 2 :", "-Apprenti🚺:"]
    player_1.extend(info_bracket("player1"))
    player_2.extend(info_bracket("player2"))
    
    #maximum vertical size of info 
    max_size_Y=max(Size_Y*2-1, max(4+len(game_data["player1"]["apprentices"])+len(game_data["player1"]["dragon"]),
                                   4+len(game_data["player2"]["apprentices"])+len(game_data["player2"]["dragon"]),))
    for line in range (max_size_Y):
        if line<=Size_Y:
            if line==0:
                print("Player 1 : ",end="")
                for case in range (Size_X):
                    if case+1<10:
                        print(f"+{str(case+1)}{str(case+1)}",end="")
                    else:
                        print(f"+{str(case+1)}",end="")
                print("+ Player 2 : ")
            else:
                print(" "*11,end="")
                for case in range (Size_X):
                    print("+--",end="")
                print("+")
        else:
            print("dragon")
                
        

    
term = blessed.Terminal()  

    
display(game_data)
input("ordre ->")