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
    implementation: De Braekeleer Mickaël (v2 06/03/25)
    """
    #init game data dict with basic info
    game_data={"map":None, "player1":{"Altar":[], "call":10, "apprentices":{}, "dragon":{}}, "player2":{"Altar":[], "call":10, "apprentices":{}, "dragon":{}}, "eggs":{}}
    #open the file of the map
    map=open(map_file_path, "r")
    #get all data lines inside a list (list of lines)
    raw_data=map.readlines()
    #close the map file
    map.close()
    
    #search in all lines for data
    for line in range (len(raw_data)):
        if raw_data[line].split(":")[0] =="altars":
            info=raw_data[line+1].split(" ")
            game_data["player1"]["Altar"]=[int(info[1]), int(info[2])]
            info=raw_data[line+2].split(" ")
            game_data["player2"]["Altar"]=[int(info[1]), int(info[2])]      
        elif raw_data[line].split(":")[0] =="map":
            info=raw_data[line+1].split(" ")
            game_data["map"]=[int(info[0]), int(info[1])]
        elif raw_data[line].split(":")[0] == "apprentices":
            line+=1
            while raw_data[line].split(":")[0] !="eggs":
                info=raw_data[line].split(" ")
                if int(info[0])==1:
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
term = blessed.Terminal()

def info_bracket(player:str,game_data: dict)->list:
    """generate info bracket for a player (info on right or left of the display)

    Parameters
    ----------
    player : str name of the player (str)
    game_data : dictionnary of all game data(dict)
    
    Returns
    -------
    player_info : list of all info on a player line by line (list)

    Version
    -------
    specification: De Braekeleer Mickaël (v.1 06/03/25)
    implementation: De Braekeleer Mickaël (v.1 06/03/25)
    """
    #initialisation of the returned list 
    player_info=[]
    
    #Add altar position to the brackets
    player_info.append("-Altar:")
    position=game_data[player]["Altar"]
    player_info.append(f"   >pos : {position[0]} {position[1]}")
    #Add time for next call to the brackets
    Cooldown_Summon=game_data[player]["call"]
    if Cooldown_Summon==0:
        player_info.append("Appel disponnible")
    else:
        player_info.append(f"Appel : {Cooldown_Summon} tours")
           
    #Browse each apprentic of a player and add their info to the brackets
    have_apprentice=False
    for apprentice in game_data[player]["apprentices"]:
        if not have_apprentice:
            if int(player[-1])==1:
                player_info.append(f"-Apprenti🚹:")
            else:
                player_info.append(f"-Apprenti🚺:")
            have_apprentice=True
        player_info.append(f"   -{apprentice} :")
        player_info.append(f"   >PV  : {game_data[player]["apprentices"][apprentice]["current_health"]}/{game_data[player]["apprentices"][apprentice]["max_health"]}")
        #temporary variable for position of the character 
        position=game_data[player]["apprentices"][apprentice]["pos"]
        player_info.append(f"   >pos : {position[0]} {position[1]} ")
        
    #Browse each dragon of a player and add their info to the brackets
    have_dragon=False
    for dragon in game_data[player]["dragon"]:
        if not have_dragon:
            player_info.append(f"-Dragon🐉:")
            have_dragon=True
        player_info.append(f"   -{dragon}:")
        player_info.append(f"   >PV     : {game_data[player]["dragon"][dragon]["current_health"]}/{game_data[player]["dragon"][dragon]["max_health"]}")
        player_info.append(f"   >Dégats : {game_data[player]["dragon"][dragon]["attack_damage"]}")
        player_info.append(f"   >Portée : {game_data[player]["dragon"][dragon]["attack_range"]}")
        #temporary variable for position of the character 
        position=game_data[player]["dragon"][dragon]["pos"]
        player_info.append(f"   >pos    : {position[0]} {position[1]} ")
    return player_info

def custom_len(word:str)->int:
    """len func but count 2 for any emoji scanned

    Parameters
    ----------
    word

    Returns
    -------
    count
    
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 07/03/25)
    implementation: De Braekeleer Mickaël (v.1 07/03/25)
    """
    count=0
    for char in word:
        if char in "🚹🚺🐉":
            count+=2
        else:
            count+=1
    return count

def display(game_data: dict):
    """Generate the display screen
    
    Parameters
    ----------
    game_data : dictionnary of all game data(dict)
    
    Version
    -------
    specification: Mitta Kylian, De Braekeleer Mickaël (v.1 20/02/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël (v.1.1 06/03/25)
    """
    #initial clear
    print(term.home + term.clear + term.hide_cursor)
    
    #initial map size
    Size_X = game_data["map"][0]
    Size_Y = game_data["map"][1]
    
    #initial info bracket
    player_1=["Player 1 :"]
    player_2=["Player 2 :"]
    player_1.extend(info_bracket("player1", game_data))
    player_2.extend(info_bracket("player2", game_data))
    

    #maximum vertical size of display
    max_size_Y=max(Size_Y*3+1, max(4+len(game_data["player1"]["apprentices"])+len(game_data["player1"]["dragon"]),
                                   4+len(game_data["player2"]["apprentices"])+len(game_data["player2"]["dragon"]),))
    #maximum horiziontal size of display
    max_info_p1=max([len(elem) for elem in player_1])
    max_info_p2=max([len(elem) for elem in player_2])
    max_size_X=int(max_info_p1+max_info_p2+game_data["map"][0]*3+1)
    
    #generate display
    for line in range (max_size_Y):
        #print player 1 info
        if len(player_1)>line:
            print(player_1[line],end="")
            print(" "*(max_info_p1-custom_len(player_1[line])),end="")
        #if no info for player 1, just print a blank space
        else:
            print(" "*max_info_p1,end="")
            
        #generate Array
        #if line=no info case
        if line%3==0:
            for cases in range (game_data["map"][0]*3):
                if cases%3==0:
                    print("+",end="")
                else:
                    print("-",end="")
            print("+",end="")
        #if line=info case  
        else:
            for cases in range (game_data["map"][0]*3):
                if cases%3==0:
                    print("|",end="")
                else:
                    print("d",end="")
            print("|",end="")
        
        #print player 2 info
        if len(player_2)>line:   
            print("  ",end="")
            print(player_2[line])
        #blank space if no info for player 2
        else:
            print("")
        
        
        
  

display(game_data)

input("ordre ->")
