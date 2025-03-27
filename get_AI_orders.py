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
    specification: Mitta Kylian, De Braekeleer Mickaël (20/02/25)
    implementation: De Braekeleer Mickaël (v1 26/02/25)
    implementation: De Braekeleer Mickaël (v2 06/03/25)
    """
    #init game data dict with basic info
    game_data={"map":None, "player1":{"altars":[], "summon":0, "apprentices":{}, "dragon":{}}, "player2":{"altars":[], "summon":0, "apprentices":{}, "dragon":{}}, "eggs":{}, "idle_turn":0}
    #open the file of the map
    map=open(map_file_path, "r")
    #get all data lines inside a list (list of lines)
    raw_data=map.readlines()
    #close the map file
    map.close()
    
    #search in all lines for data
    for line in range (len(raw_data)):
        if raw_data[line].split(":")[0] =="altars":
            #get all altar info
            info=raw_data[line+1].split(" ")
            game_data["player1"]["altars"]=[int(info[1]), int(info[2])]
            info=raw_data[line+2].split(" ")
            game_data["player2"]["altars"]=[int(info[1]), int(info[2])]      
        elif raw_data[line].split(":")[0] =="map":
            #get map size
            info=raw_data[line+1].split(" ")
            game_data["map"]=[int(info[0]), int(info[1])]
        elif raw_data[line].split(":")[0] == "apprentices":
            line+=1
            while raw_data[line].split(":")[0] !="eggs":
                info=raw_data[line].split(" ")
                #check if apprentice belongs to player 1 or player2
                if int(info[0])==1:
                    player="player1"
                else:
                    player="player2"
                #get apprentices info
                game_data[player]["apprentices"][info[1]]={}
                game_data[player]["apprentices"][info[1]]["pos"]=[int(info[2]), int(info[3])]
                game_data[player]["apprentices"][info[1]]["max_health"]=int(info[4])
                game_data[player]["apprentices"][info[1]]["current_health"]=int(info[4])
                game_data[player]["apprentices"][info[1]]["regeneration"]=int(info[5][0:1])
                game_data[player]["apprentices"][info[1]]["linked_dragon"]=[]   
                line+=1
        elif raw_data[line].split(":")[0]=="eggs":
            for eggs in range (len(raw_data)-line):
                #get all egg info
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
                    #return game_data with all map info  
                    return game_data
                
def get_AI_orders(game_data:dict, player:str)->list:
    """get advanced AI orders

    parameters
    ----------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    player : number of the player (int)

    
    returns
    -------
    orders : order with the correct format (list)
    
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 27/03/25)
    implementation:  

    """
    #init orders variable
    orders=[]
    eggs={}
    
    #get all egg pos
    for egg in game_data["eggs"]:
            egg_pos=game_data["eggs"][egg]["pos"]
            eggs[egg]={}
            eggs[egg]={"pos": egg_pos, "dif": 0, "focus": False}
            
    #get order for every apprentices
    for apprentice in game_data[player]["apprentices"]:
        priority="egg"
        app_pos=game_data[player]["apprentices"][apprentice]["pos"]
        
        if priority=="egg":
            egg_focus=False
            dif=[]
            #check for nearby eggs to hatch them
            for egg in eggs:
                dif_y=abs(int(eggs[egg]["pos"][0])-int(app_pos[0]))
                dif_x=abs(int(eggs[egg]["pos"][1])-int(app_pos[1]))
                eggs[egg]["dif"]=max(dif_y, dif_x)
            #check for nearest egg to hatch it
            nearest_egg=10000
            for egg in eggs:
                if eggs[egg]["focus"]==False and eggs[egg]["dif"]<=nearest_egg:
                    nearest_egg=eggs[egg]["dif"]
                    egg_focus=egg
            if egg_focus:        
                eggs[egg_focus]["focus"]=True
                
                order=[0, 0]
                if app_pos[0]>eggs[egg_focus]["pos"][0]:
                    order[0]=-1
                elif app_pos[0]<eggs[egg_focus]["pos"][0]:
                    order[0]=1
                if app_pos[1]>eggs[egg_focus]["pos"][1]:
                    order[1]=-1
                elif app_pos[1]<eggs[egg_focus]["pos"][1]:
                    order[1]=1
                    
                orders.append(f'{apprentice}:@{int(app_pos[0])+order[0]}-{int(app_pos[1])+order[1]}')
                           
    return orders 

map_path="C:/Users/coram/OneDrive/Desktop/projet/map.drk"
game_data=load_map(map_path)

get_AI_orders(game_data, "player1")