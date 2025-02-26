import os
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
    """
    #init game data dict with basic info
    game_data={"player1": {"call" : 10},
               "player2": {"call" : 10}
               }
    #open the file of the map
    map=open(map_file_path, "r")
    #get all data lines inside a list (list of lines)
    raw_data=map.readlines()
    #close the map file
    map.close()
    
    #search in all lines for data
    for line in range (len(raw_data)):
        if raw_data[line] =="map:":
            game_data["map"]=raw_data[line+1].split(" ")
        elif raw_data[line] == "apprentices:":
            line+=1
            while raw_data[line] !="eggs:":
                info=raw_data[line].split(" ")
                if info[0]==1:
                    game_data["player1"]["apprentices"][info[1]]["pos"]=[info[2], info[3]]
                    game_data["player1"]["apprentices"][info[1]]["max_health"]=info[5]
                    game_data["player1"]["apprentices"][info[1]]["current_health"]=info[5]
                    game_data["player1"]["apprentices"][info[1]]["regeneration"]=info[6]
                else:
                    game_data["player2"]["apprentices"][info[1]]["pos"]=[info[2], info[3]]
                    game_data["player2"]["apprentices"][info[1]]["max_health"]=info[5]
                    game_data["player2"]["apprentices"][info[1]]["current_health"]=info[5]
                    game_data["player2"]["apprentices"][info[1]]["regeneration"]=info[6]          
                line+=1
        elif raw_data[line]=="eggs:":
            for eggs in range (len(raw_data)-line):
                line+=1
                egg=raw_data[line].split(" ")
                game_data["eggs"][egg[0]]["pos"]=[egg[1], egg[2]]
                game_data["eggs"][egg[0]]["time_to_hatch"]=[egg[1], egg[3]]
                game_data["eggs"][egg[0]]["max_health"]=egg[4]
                game_data["eggs"][egg[0]]["current_health"]=egg[4]
                game_data["eggs"][egg[0]]["attack_damage"]=egg[5]
                game_data["eggs"][egg[0]]["attack_range"]=egg[6]
                game_data["eggs"][egg[0]]["regeneration"]=egg[7]
                  
            return game_data
    
map_path="C:/Users/coram/OneDrive/Desktop/projet/map.drk" 
game_data=load_map(map_path)
print(game_data)




