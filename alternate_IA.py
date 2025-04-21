import blessed, math, os, time, random
term = blessed.Terminal()

from remote_play import create_connection, get_remote_orders, notify_remote_orders, close_connection

import copy
#test

def get_AI_orders(game_data:dict, player:str)->list:
    """get advanced AI orders

    parameters
    ----------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    player : name of the player (str)

    
    returns
    -------
    orders : order with the correct format (list)
    
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 27/03/25)
    implementation: : Kylian Mitta, Mickaël De Braekeleer, Aymane El Abbassi, Hamza Sossey-Alaoui (v.1 27/03/25)
 
    """
    in_danger=0
    eggs=False
    orders=[]
    if player == "player1":
        enemy="player2"
    else:
        enemy="player1"
    directly_dangerous_tiles=check_dangerous_tiles(game_data, enemy)
    #apply for every dragon a priority
    for dragon in game_data[player]["dragon"]:
        order=False
        count=int(0)
        #check if in a combat
        dragon_in_combat=[]
        pos=game_data[player]["dragon"][dragon]["pos"]
        attack_damage=game_data[player]["dragon"][dragon]["attack_damage"]
        attacking_dragon=[attacking_dragon for tile, attacking_dragon in directly_dangerous_tiles]
        
        for enemy_dragon in attacking_dragon:
            danger_positions = [tile for tile, dragon in directly_dangerous_tiles]
            if pos == danger_positions[count]:
                if enemy_dragon not in dragon_in_combat:
                    dragon_in_combat.append(enemy_dragon)
            count+=1
                    
        if dragon_in_combat:
            damage_incoming=int(0)
            enemy_health=int(0)
            for dragon_attacking in dragon_in_combat:
                damage_incoming+=game_data[enemy]["dragon"][dragon_attacking]["attack_damage"]
                enemy_health+=game_data[enemy]["dragon"][dragon_attacking]["current_health"]
            turn_to_get_killed=int(game_data[player]["dragon"][dragon]["current_health"]/damage_incoming)
            #last attack
            if turn_to_get_killed<=1:
                in_danger+=1
                exit=attack_nearest(game_data, player, dragon, enemy) 
                order=exit[0]
                tile=exit[1]
                directly_dangerous_tiles.append([tile, dragon])     
            else:
                turn_to_kill=enemy_health//attack_damage
                if damage_incoming<attack_damage or turn_to_kill<(turn_to_get_killed+1) :
                    exit=attack_nearest(game_data, player, dragon, enemy)
                    order=exit[0]
                    tile=exit[1]
                    directly_dangerous_tiles.append([tile, dragon])
                else:
                    in_danger+=1
                    tile=dodge(pos, directly_dangerous_tiles)
                    if tile:
                        order=f"{dragon}:@{tile[0]}-{tile[1]}"
                    else:
                        exit=(attack_nearest(game_data, player, dragon, enemy))
                        order=exit[0]
                        eggs=exit[1]
                        directly_dangerous_tiles.append([tile, dragon])
        if not order:
            exit=attack_nearest(game_data, player, dragon, enemy)
            order=exit[0]
            tile=exit[1]
            directly_dangerous_tiles.append([tile, dragon])
           
        orders.append(order)
        
    #apply for every apprentice a priority
    for apprentice in game_data[player]["apprentices"]:
        tile=False
        positions=[]
        order=False
        pos=game_data[player]["apprentices"][apprentice]["pos"]
        for y in range (-1, 2):
            for x in range (-1, 2):
                positions.append([pos[0]+y, pos[1]+x])
        for near_pos in positions:
            danger_positions = [tile for tile, dragon in directly_dangerous_tiles]
            if near_pos in danger_positions :
                in_danger+=1
                order=move_far(game_data, player, apprentice,enemy)
        if order:
            order=f"{apprentice}:@{pos[0]+order[0]}-{pos[1]+order[1]}"
        elif game_data["eggs"]:
            exit=focus_egg(game_data, player, apprentice, eggs)
            order=exit[0]
            eggs=exit[1]
        else:
            order=move_far(game_data, player, apprentice,enemy)
            order=f"{apprentice}:@{pos[0]+order[0]}-{pos[1]+order[1]}"
                  
        orders.append(order)
        
    if in_danger>=2 and game_data[player]["summon"]==0 and game_data["idle_turn"]<70:
        alt_game_data=copy.deepcopy(game_data)
        alt_game_data[player]["summon"]=10
        alt_game_data=summon(alt_game_data, player)
        orders=get_AI_orders(alt_game_data, player)
        orders.append("summon")
    
    
    return orders

def move_far(game_data, player, apprentice, enemy):
    size=game_data["map"]
    pos=game_data[player]["apprentices"][apprentice]["pos"]
    order=[pos[0], pos[1]]
    nearest_entity = [False, int(10000000)]
    for dragon_enemy in  game_data[enemy]["dragon"]:
        dragon_enemy_pos=game_data[enemy]["dragon"][dragon_enemy]["pos"]
        dif_y=abs(int(dragon_enemy_pos[0])-int(pos[0]))
        dif_x=abs(int(dragon_enemy_pos[1])-int(pos[1]))
        dif=max(dif_y, dif_x)
        if dif < nearest_entity[1]:
            nearest_entity=[dragon_enemy_pos, dif]
    
    if nearest_entity[0]:
        order=[0, 0]
        if pos[0]>nearest_entity[0][0] and pos[0]+1<=size[0]:
            order[0]=+1
        elif pos[0]<nearest_entity[0][0] and pos[0]-1>0:
            order[0]=-1
        if pos[1]>nearest_entity[0][1] and pos[1]+1<=size[1]:
            order[1]=+1
        elif pos[1]<nearest_entity[0][1] and pos[1]-1>0:
            order[1]=-1
            
        if order[0]==0:
            if size[0]-pos[0]<pos[0]:
                order[0]=-1
            else:
                order[0]=1
        elif order[1]==0:
            if size[1]-pos[1]<pos[1]:
                order[1]=-1
            else:
                order[1]=1
            
            
    return order
    
    

def attack_nearest(game_data, player, dragon, enemy):
    lowest_target=[False, False, False, int(100000)]
    tiles=[]
    tiles_in_range=[]
    enemy_in_range=[]
    pos=game_data[player]["dragon"][dragon]["pos"]
    attack_damage=game_data[player]["dragon"][dragon]["attack_damage"]
    attack_range=game_data[player]["dragon"][dragon]["attack_range"]
    for tile in range (1, attack_range+1):
        tiles_in_range.append([pos[0]+tile, pos[1]])
        tiles_in_range.append([pos[0], pos[1]+tile])
        tiles_in_range.append([pos[0]+tile, pos[1]+tile])
        tiles_in_range.append([pos[0]-tile, pos[1]])
        tiles_in_range.append([pos[0], pos[1]-tile])
        tiles_in_range.append([pos[0]-tile, pos[1]-tile])
        tiles_in_range.append([pos[0]-tile, pos[1]+tile])  
        tiles_in_range.append([pos[0]+tile, pos[1]-tile])
     
    
    for enemy_dragon in game_data[enemy]["dragon"]:
        entity_pos=game_data[enemy]["dragon"][enemy_dragon]["pos"]
        entity_hp=game_data[enemy]["dragon"][enemy_dragon]["current_health"]
        if list(entity_pos) in tiles_in_range:
            enemy_in_range.append([enemy_dragon, entity_pos, "dragon", entity_hp])
             
    for apprentice in game_data[enemy]["apprentices"]: 
        entity_pos=game_data[enemy]["apprentices"][apprentice]["pos"]
        entity_hp=game_data[enemy]["apprentices"][apprentice]["current_health"]
        if list(entity_pos) in tiles_in_range:
            enemy_in_range.append([apprentice, entity_pos, "apprentices", entity_hp])
    

    for enemies in enemy_in_range:
        if enemies[1][0]==pos[0]:
            if enemies[1][1]>pos[1]:
                direction="E"
            else:
                direction="W"
        elif enemies[1][0]>pos[0]:
            if enemies[1][1]>pos[1]:
                direction="SE"
            elif enemies[1][1]==pos[1]:
                direction="S"
            else:
                direction="SW"
        else:
            if enemies[1][1]>pos[1]:
                direction="NE"
            elif enemies[1][1]==pos[1]:
                direction="N"
            else:
                direction="NW"
            
        #one shot ?
        if enemies[3]<attack_damage:
            if "N" in direction:
                if "W" in direction:
                    for tile in range(attack_range):
                        tiles.append([pos[0]-(attack_range+1), pos[1]-(attack_range+1)])
                elif "E" in direction:
                    for tile in range(attack_range):
                        tiles.append([pos[0]-(attack_range+1), pos[1]+(attack_range+1)])
                else:
                    for tile in range(attack_range):
                        tiles.append([pos[0]-(attack_range+1), pos[1]])
            elif "S" in direction:
                if "W" in direction:
                    for tile in range(attack_range):
                        tiles.append([pos[0]+(attack_range+1), pos[1]-(attack_range+1)])
                elif "E" in direction:
                    for tile in range(attack_range):
                        tiles.append([pos[0]+(attack_range+1), pos[1]+(attack_range+1)])
                else:
                    for tile in range(attack_range):
                        tiles.append([pos[0]+(attack_range+1), pos[1]])
            else:
                if "W" in direction:
                    for tile in range(attack_range):
                        tiles.append([pos[0], pos[1]-(attack_range+1)])
                else:
                    for tile in range(attack_range):
                        tiles.append([pos[0], pos[1]+(attack_range+1)])
                    
            return f"{dragon}:x{direction}", tiles
        if lowest_target[3]>enemies[3] or (lowest_target[2]!="apprentices" and enemies[2]=="apprentices"):
            lowest_target=enemies
            lowest_target.append(direction)
    
    if lowest_target[0]:
        direction=lowest_target[4]           
        if "N" in direction:
            if "W" in direction:
                for tile in range(attack_range):
                    tiles.append([pos[0]-(attack_range+1), pos[1]-(attack_range+1)])
            elif "E" in direction:
                for tile in range(attack_range):
                    tiles.append([pos[0]-(attack_range+1), pos[1]+(attack_range+1)])
            else:
                for tile in range(attack_range):
                    tiles.append([pos[0]-(attack_range+1), pos[1]])
        elif "S" in direction:
            if "W" in direction:
                for tile in range(attack_range):
                    tiles.append([pos[0]+(attack_range+1), pos[1]-(attack_range+1)])
            elif "E" in direction:
                for tile in range(attack_range):
                    tiles.append([pos[0]+(attack_range+1), pos[1]+(attack_range+1)])
            else:
                for tile in range(attack_range):
                    tiles.append([pos[0]+(attack_range+1), pos[1]])
        else:
            if "W" in direction:
                for tile in range(attack_range):
                    tiles.append([pos[0], pos[1]-(attack_range+1)])
            else:
                for tile in range(attack_range):
                    tiles.append([pos[0], pos[1]+(attack_range+1)])
        return [f"{dragon}:x{direction}", tiles]
    else:
        return search_enemies(game_data, player, dragon, enemy), None
    
    
        

def dodge(pos, directly_dangerous_tiles):
    if not type(pos[0])==type([]):
        for y in range (-1, 2):
            for x in range (-1, 2):
                near_tile=[(pos[0]+y), (pos[1]+x)]
                if near_tile not in directly_dangerous_tiles:
                    return near_tile
                else:
                    return False
    else:
        for pos in pos:
            for y in range (-1, 2):
                for x in range (-1, 2):
                    near_tile=[(pos[0]+y), (pos[1]+x)]
                    if near_tile not in directly_dangerous_tiles:
                        return near_tile
                    else:
                        return False
    
    
def check_dangerous_tiles(game_data: dict, enemy: str):
    tiles_in_range=[]
    for dragon in game_data[enemy]["dragon"]:
        pos=game_data[enemy]["dragon"][dragon]["pos"]
        attack_range=game_data[enemy]["dragon"][dragon]["attack_range"]
        for tile in range (1, attack_range+1):
            tiles_in_range.append([[pos[0]+attack_range, pos[1]], dragon])
            tiles_in_range.append([[pos[0], pos[1]+attack_range], dragon])
            tiles_in_range.append([[pos[0]+attack_range, pos[1]+attack_range], dragon])
            tiles_in_range.append([[pos[0]-attack_range, pos[1]], dragon])
            tiles_in_range.append([[pos[0], pos[1]-attack_range], dragon])
            tiles_in_range.append([[pos[0]-attack_range, pos[1]-attack_range], dragon])
            tiles_in_range.append([[pos[0]+attack_range, pos[1]+attack_range], dragon])  
            tiles_in_range.append([[pos[0]+attack_range, pos[1]-attack_range], dragon])
    return tiles_in_range
        

def search_enemies(game_data: dict, player: str, dragon: str, enemy: str, dragon_in=False) -> list:
    """
    Recherche les ennemis autour d'une entité donnée et renvoie une liste des ennemis à proximité.

    Paramètres :
    - game_data : dict, les données actuelles du jeu, qui contiennent des informations sur les entités, leurs positions, etc.
    - player : str, le nom du joueur pour lequel on fait la recherche ("player1" ou "player2").
    - entity : str, le nom de l'entité à vérifier (un dragon ou un apprenti). C'est l'entité dont on cherche les ennemis autour.

    Retourne :
    - list : une liste contenant les ennemis autour de l'entité donnée (ceux qui sont à une case de distance).
    """
    dragon_pos=game_data[player]["dragon"][dragon]["pos"]
    all_entity_enemy_pos=[]
    nearest_entity=[None, 10000] #pos, dif
  
       
    #recupere la position de toutes les entités enemies
    if dragon_in:
        for dragon_enemy in  game_data[enemy]["dragon"]:
            dragon_enemy_pos=game_data[enemy]["dragon"][dragon_enemy]["pos"]
            all_entity_enemy_pos.append(dragon_enemy_pos)
            dif_y=abs(int(dragon_enemy_pos[0])-int(dragon_pos[0]))
            dif_x=abs(int(dragon_enemy_pos[1])-int(dragon_pos[1]))
            dif=max(dif_y, dif_x)
            if dif < nearest_entity[1]:
                nearest_entity=[dragon_enemy_pos, dif]
    
    for apprentice_enemy in game_data[enemy]["apprentices"]:
        
        apprentice_enemy_pos=game_data[enemy]["apprentices"][apprentice_enemy]["pos"]
        all_entity_enemy_pos.append(apprentice_enemy_pos)
        dif_y=abs(int(apprentice_enemy_pos[0])-int(dragon_pos[0]))
        dif_x=abs(int(apprentice_enemy_pos[1])-int(dragon_pos[1]))
        dif=max(dif_y, dif_x)
        if dif < nearest_entity[1]:
            nearest_entity=[apprentice_enemy_pos, dif]
            
    if nearest_entity:
        order=[0, 0]
        if dragon_pos[0]>nearest_entity[0][0]:
            order[0]=-1
        elif dragon_pos[0]<nearest_entity[0][0]:
            order[0]=1
        if dragon_pos[1]>nearest_entity[0][1]:
            order[1]=-1
        elif dragon_pos[1]<nearest_entity[0][1]:
            order[1]=1
            
        new_pos = [int(dragon_pos[0]) + order[0], int(dragon_pos[1]) + order[1]]
        if new_pos==dragon_pos:
            if new_pos[1]-1>0:
                orders = f'{dragon}:@{new_pos[0]}-{new_pos[1]-1}'
            else:
                orders = f'{dragon}:@{new_pos[0]}-{new_pos[1]+1}'
                
        else:
            if new_pos != nearest_entity[0]:
                orders = f'{dragon}:@{new_pos[0]}-{new_pos[1]}'
            else:
                orders=attack_nearest(game_data, player, dragon, enemy)
        
    return orders
    
                

def focus_egg(game_data:dict, player:str, apprentice:str, eggs=False):
    #init orders variable
    orders=[]
    if game_data["eggs"]:
        if not eggs:
            eggs={}
            #get all egg pos
            for egg in game_data["eggs"]:
                    egg_pos=game_data["eggs"][egg]["pos"]
                    eggs[egg]={}
                    eggs[egg]={"pos": egg_pos, "dif": 0, "focus": False}
                
        #get order for every apprentices
        app_pos=game_data[player]["apprentices"][apprentice]["pos"]
        
        egg_focus=False
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
                
            orders=(f'{apprentice}:@{int(app_pos[0])+order[0]}-{int(app_pos[1])+order[1]}')
        else:
            orders=""
    else:
        orders=""

            
    return orders, eggs
    
    
# other functions //////////////////////////////////////////////////////////////////////////////////////////////////////////////
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
                game_data[player]["apprentices"][info[1]]["regeneration"]=int(info[5][0:2])
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
                game_data["eggs"][info[0]]["regeneration"]=int(info[7][0:2])
                if line == len(raw_data)-1:
                    #return game_data with all map info  
                    return game_data
                
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
    specification: De Braekeleer Mickaël (06/03/25)
    implementation: De Braekeleer Mickaël (06/03/25)
    """
    #initialisation of the returned list 
    player_info=[]
    
    #Add altars position to the brackets
    player_info.append("-Altar🏰:")
    position=game_data[player]["altars"]
    player_info.append(f"   >pos : {position[0]} {position[1]}")
    #Add time for next summon to the brackets
    Cooldown_Summon=game_data[player]["summon"]
    if Cooldown_Summon==0:
        player_info.append("Appel disponible")
    else:
        player_info.append(f"Appel : {Cooldown_Summon} tours")
           
    #Browse each apprentic of a player and add their info to the brackets
    have_apprentice=False
    for apprentice in game_data[player]["apprentices"]:
        if not have_apprentice:
            if int(player[-1])==1:
                player_info.append(f'-Apprenti🚹:')
            else:
                player_info.append(f'-Apprenti🚺:')
            have_apprentice=True
        player_info.append(f'   -{apprentice} :')
        player_info.append(f'   >PV  : {game_data[player]["apprentices"][apprentice]["current_health"]}/{game_data[player]["apprentices"][apprentice]["max_health"]}')
        #add linked_dragon
        if game_data[player]["apprentices"][apprentice]["linked_dragon"]:
            player_info.append(f'   -dragon lié :')
        for dragon in game_data[player]["apprentices"][apprentice]["linked_dragon"]:
            player_info.append(f'      >{dragon}')
        #temporary variable for position of the character 
        position=game_data[player]["apprentices"][apprentice]["pos"]
        player_info.append(f'   >pos : {position[0]} {position[1]} ')
        
    #Browse each dragon of a player and add their info to the brackets
    have_dragon=False
    for dragon in game_data[player]["dragon"]:
        if not have_dragon:
            player_info.append(f"-Dragon🐉:")
            have_dragon=True
        player_info.append(f'   -{dragon}:')
        player_info.append(f'   >PV     : {game_data[player]["dragon"][dragon]["current_health"]}/{game_data[player]["dragon"][dragon]["max_health"]}')
        player_info.append(f'   >Dégats : {game_data[player]["dragon"][dragon]["attack_damage"]}')
        player_info.append(f'   >Portée : {game_data[player]["dragon"][dragon]["attack_range"]}')
        #temporary variable for position of the character 
        position=game_data[player]["dragon"][dragon]["pos"]
        player_info.append(f'   >pos    : {position[0]} {position[1]}')
        
    return player_info

def custom_len(word:str)->int:
    """len func but count 2 for any emoji scanned

    Parameters
    ----------
    word : any string (str)

    Returns
    -------
    count : number of character of the word (int)
    
    Version
    -------
    specification: De Braekeleer Mickaël (07/03/25)
    implementation: De Braekeleer Mickaël (07/03/25)
    """
    #init count
    count=0
    for char in word:
        #custom filter filled emoji maybe used in the program
        if char in "🚹🚺🐉🟨🏰🥚🟩🟥🐲":
            count+=2
        else:
            count+=1
    return count

def generate_map_grid(Size_X:int, Size_Y:int, game_data:dict)->list:
    """Generate map grid

    Parameters
    ----------
    Size_X : size in X of the map (int)
    Size_Y : size in Y of the map (int)
    game_data : dictionnary of all game data(dict)

    Returns
    -------
    map_grid : list of list with emoji for each tiles of the map (list)
    
    Version
    -------
    specification: De Braekeleer Mickaël (10/03/25)
    implementation: De Braekeleer Mickaël (10/03/25)
    """
    
    map_grid=[["🟥"]*(Size_X+2) for i in range(Size_Y+2)]

    #for all player
    for player in ["player1", "player2"]:
        #all position for player team
        pos_altar_p1=game_data[player]["altars"]
        map_grid[pos_altar_p1[1]][pos_altar_p1[0]]="🏰"
        for apprentice in game_data[player]["apprentices"]:
            #get apprentice pos
            pos_X=game_data[player]["apprentices"][apprentice]["pos"][1]
            pos_Y=game_data[player]["apprentices"][apprentice]["pos"][0]
            #place apprentice on the grid with the good emoji
            if player=="player1":
                map_grid[pos_X][pos_Y]="🚹"
            else:
                map_grid[pos_X][pos_Y]="🚺"          
        for dragon in game_data[player]["dragon"]:
            #get dragon pos and place them on the grid
            pos_X=game_data[player]["dragon"][dragon]["pos"][1]
            pos_Y=game_data[player]["dragon"][dragon]["pos"][0]
            if player=="player1":
                map_grid[pos_X][pos_Y]="🐉"
            else:
                map_grid[pos_X][pos_Y]="🐲"  
    for egg in game_data["eggs"]:
        #get egg pos and place them on the grid
        pos_X=game_data["eggs"][egg]["pos"][1]
        pos_Y=game_data["eggs"][egg]["pos"][0]
        map_grid[pos_X][pos_Y]="🥚"
        
    return map_grid

def display(game_data: dict):
    """Generate the display screen
    
    Parameters
    ----------
    game_data : dictionnary of all game data(dict)
    
    Version
    -------
    specification: Mitta Kylian, De Braekeleer Mickaël (20/02/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël (06/03/25)
    """
    #initial clear
    print(term.home + term.clear + term.hide_cursor)
    
    #initial map size
    Size_Y = game_data["map"][0]
    Size_X = game_data["map"][1]
    
    #initial pos
    x=int(1)
    y=float(1)
    
    map_grid=generate_map_grid(Size_X, Size_Y, game_data)
    
    
    
    #initial info bracket
    player_1=["Player 1 :"]
    player_2=["Player 2 :"]
    player_1.extend(info_bracket("player1", game_data))
    player_2.extend(info_bracket("player2", game_data))
    

    #maximum vertical size of display
    max_size=max(Size_X*2+1, max(4+len(game_data["player1"]["apprentices"])+len(game_data["player1"]["dragon"]),
                                   4+len(game_data["player2"]["apprentices"])+len(game_data["player2"]["dragon"]),
                                   len(player_1), 
                                   len(player_2)))
    
    #maximum horiziontal size of left display brackets
    max_info_p1=max([len(elem) for elem in player_1])
    
    #generate display
    for line in range (max_size):
        #print player 1 info brackets
        if len(player_1)>line:
            print(player_1[line],end="")
            print(" "*(max_info_p1-custom_len(player_1[line])),end="")
        #if no info for player 1, just print a blank space
        else:
            print(" "*max_info_p1,end="")
            
        #generate Array
        if line<game_data["map"][0]*2+1:
            #if line=no info case
            if line%2==0:
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
                        if custom_len(map_grid[int(y)][int(x)])==2 and int(y)==float(y):
                            print(f"{map_grid[int(y)][int(x)]}",end="")
                        elif int(y)==float(y):
                            print(f"{map_grid[int(y)][int(x)]}"*2,end="")
                        y+=0.5
                y=float(1)
                x+=1
                print("|",end="")
        else:
            print(" "*(game_data["map"][1]*3+1), end="")
        
        #print player 2 info brackets
        if len(player_2)>line:   
            print("  ",end="")
            print(player_2[line])
        #blank space if no info for player 2
        else:
            print("")
            
def Get_orders(game_data:dict, player:str) -> list:
    """Ask the player what he want to play

    parameters
    ----------
    player : name of the player (str)
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    
    return
    ------
    orders_player : order with the correct format (list)
    
    Version
    -------
    specification: Mitta Kylian, De Braekeleer Mickaël (20/02/25)
    implementation: Mitta Kylian (03/03/25)
    
    """
    #init orders list
    orders_player=[]

    #input orders from player
    orders=input(f"{player}, veuillez entrer votre ordre ->")

    #make a list by splitting by space
    orders=orders.split(" ")
    #check if all orders are valid (only verify good format here and if player have entity) and add them to orders_players if they are
    for order in orders:
        if "summon"==order:
            #add summon to keepen orders
            orders_player.append(order)
                      
        elif ':' in order:
            #split with format / [0] : entity name, [1] : order info like 10-10, xN
            check = order.split(":")

            if len(check) > 1: 
                if check[1]:
                    check_temp = []
                    #if move order format, split and strip info
                    if check[1][0] == "@" and '-' in check[1]: 
                        check[1] = check[1].strip("@")
                        check_temp = check[1].split("-")

                    #check if apprentice belongs to the player
                    if check[0] in game_data[player]["apprentices"]:
                        #move order
                        if len(check_temp) > 1 and check_temp[0].isdigit() and check_temp[1].isdigit():
                                orders_player.append(order)

                    #check if dragon belongs to the player
                    if check[0] in game_data[player]["dragon"]:
                        #move order
                        if len(check_temp) > 1 and check_temp[0].isdigit() and check_temp[1].isdigit():
                            orders_player.append(order)
                        #attack order
                        if check[1] in {"xN", "xNE", "xE", "xSE", "xS", "xSW", "xW", "xNW"}:
                            orders_player.append(order)
    return  orders_player

    
def action(game_data:dict , all_orders:list)->dict :
    """General function which calls the subfunctions to perform the different actions of the game
    
    Parameters
    ----------
    game_data : dictionnary of all game data (dict) 
    orders: orders of the player(list)
        
    Returns
    -------
    game_data: dictionnary of all game data after the player turn (dict)
    
    Version
    -------
    specification: Aymane el abbassi (v.1 20/02/25)
    implementation: Hamza Sossey-Alaoui (v.1 17/03/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël( v.2 22/03/25)
    """
    #init variable for all player
    all_move_orders=[]
    for player in ["player1", "player2"]:
        #init variable player specific
        entity_occupied=[]
        move_orders=[]
        attack_orders=[]
        
        #get player orders list
        if player=="player1":
            orders=all_orders[0]
        else:
            orders=all_orders[1]
            
        #don't do anything if no orders (optimisation)
        if not (len(orders)==1 and orders[0]==""):
            #execute summon order
            if "summon" in orders:
                #delete all summon from the list
                orders=[summon for summon in orders if summon != "summon"]
                if game_data[player]["summon"]==0:
                    game_data[player]["summon"]=int(10)
                    game_data=summon(game_data, player)
            else:
                #sort orders
                for order in orders:
                    if not order=="":             
                        order_split=order.split(":")
                        #if entity not already doing something
                        if not order_split[0] in entity_occupied:
                            if "@" in order:
                                move_orders.append(order)
                            elif "x" in order_split[1]:
                                attack_orders.append(order)
                            entity_occupied.append(order.split(":")[0])
                #execute attack
                for attacks in attack_orders:
                    game_data=attack(game_data, player, attacks)
        all_move_orders.append(move_orders)
        
    # the players move at the same time after attack            
    for player in ["player1", "player2"]:
        
        if player=="player1":
            move_orders=all_move_orders[0]
        else:
            move_orders=all_move_orders[1]
        #execute move
        for movement in move_orders:
            game_data=move(game_data, player, movement)
                    
    #check if some entity are dead
    game_data=check_death(game_data)
                                  
    return game_data

def summon(game_data:dict, player:str)->dict:
    """The function to use the special ability of the player

    Parameters
    ----------
    game_data : Data structure of the game (dict)
    
    Returns
    -------
    game_data : dictionnary of all game data after the summon (dict)
    
    Version
    -------
    specification: Hamza SOSSEY-ALAOUI (20/02/25)
    implementation: Hamza SOSSEY-ALAOUI(v1 15/03/25)
    implementation: Mitta kylian(v2 17/03/25)
    """
    # takes positions of the altar
    position=game_data[player]["altars"]
    pos_altar_y=position[0]
    pos_altar_x=position[1]

    # move apprentices to the altar
    for apprentice in game_data[player]["apprentices"]:
        game_data[player]["apprentices"][apprentice]["pos"] = pos_altar_y,pos_altar_x

    # move dragons to the altar
    for dragon in game_data[player]["dragon"]:
        game_data[player]["dragon"][dragon]["pos"] = pos_altar_y,pos_altar_x
        
    return game_data

def hatch_egg(game_data:dict)->dict:
    """hatch eggs if apprentices are on it 
    
    Parameters :
    ----------
    game_data : dict of all the game(dict)
    
    Returns
    -------
    game_data: dictionnary of all the game_data after a potentially hatching eggs (dic)
    
    Version 
    -------
    specification : Aymane el abbassi(20/02/2025)
    implementation: Aymane el abbassi(v1 15/03/25)
    implementation: Mitta Kylian (v2 19/03/25)
    """
    
    # loop for each player
    for player in ['player1', 'player2']:
        
        egg_to_delete=[]

        # loop for each apprentice of the player
        for apprentice in game_data[player]['apprentices']:
                
            # loop for each egg on the board
            for egg in game_data["eggs"]:

                # check if the positions are identical
                if game_data[player]['apprentices'][apprentice]['pos'] == game_data["eggs"][egg]["pos"]: 
                    game_data["eggs"][egg]['time_to_hatch'] -= 1
                    if game_data["eggs"][egg]['time_to_hatch'] < 1:

                        # hatching
                        game_data[player]["dragon"][egg]={}
                        game_data[player]["dragon"][egg]=game_data["eggs"][egg]
                        game_data[player]["dragon"][egg]["linked_apprentice"]=apprentice
                        game_data[player]["apprentices"][apprentice]["linked_dragon"].append(egg)
                        egg_to_delete.append(egg)
                             
        for egg in egg_to_delete:
            # delete the old egg and time to hatch stats
            if egg in game_data["eggs"]:
                del game_data["eggs"][egg]
                del game_data[player]["dragon"][egg]["time_to_hatch"]
                     
    return game_data

def attack(game_data:dict, player:str, order:str)->dict:
    """The function makes the dragon attack in the 8 directions with 2 boxes limit range
    
        Parameters:
        game_data: dictionnary of all game data (dict)
        
        Returns
        -------
        game_data: dictionnary of all game data after the attack (dict)
        
        Version
        -------
        specification: Hamza SOSSEY-ALAOUI (v.1 20/02/25)
        specification: Hamza SOSSEY-ALAOUI (v.2 17/03/25)
        implementation: Hamza SOSSEY-ALAOUI (v.1 17/03/25)
        implementation: Mitta Kylian, De Braekeleer Mickaël( v.2 22/03/25)
    """
    #split order into the format / [0] : dragon name, [1] : attack direction
    order=order.split(":")
    #check if dragon belongs to the player
    if order[0] in game_data[player]["dragon"]:
        #get all dragon usefull info and init valid_tiles 
        damage=game_data[player]["dragon"][order[0]]['attack_damage']
        attack_range=game_data[player]["dragon"][order[0]]['attack_range']
        position=game_data[player]["dragon"][order[0]]['pos']
        pos_dragon_y=position[0]
        pos_dragon_x=position[1]
        valid_tiles=[]

        for check_attack in range(1,attack_range+1):
            #get tiles coordinate for each direction
            if order[1] == "xN":
                valid_tiles.append([pos_dragon_y-check_attack,pos_dragon_x])
            elif order[1] == "xNE":
                valid_tiles.append([pos_dragon_y-check_attack,pos_dragon_x+check_attack])
            elif order[1] == "xE":
                valid_tiles.append([pos_dragon_y,pos_dragon_x+check_attack])
            elif order[1] == "xSE":
                valid_tiles.append([pos_dragon_y+check_attack,pos_dragon_x+check_attack])
            elif order[1] == "xS":
                valid_tiles.append([pos_dragon_y+check_attack,pos_dragon_x])
            elif order[1] == "xSW":
                valid_tiles.append([pos_dragon_y+check_attack,pos_dragon_x-check_attack])
            elif order[1] == "xW":
                valid_tiles.append([pos_dragon_y,pos_dragon_x-check_attack])
            elif order[1] == "xNW":
                valid_tiles.append([pos_dragon_y-check_attack,pos_dragon_x-check_attack])
                
        print(valid_tiles, order[0])
        
        #check position of each entity that belongs to player1 or player2       
        for player in ["player1", "player2"]:
            for apprentice in game_data[player]["apprentices"]:
                if list(game_data[player]["apprentices"][apprentice]["pos"]) in valid_tiles:
                    game_data[player]["apprentices"][apprentice]['current_health'] -= damage
                    #number of turn without attack:
                    game_data["idle_turn"]=0

            for dragon in game_data[player]["dragon"]:
                if list(game_data[player]["dragon"][dragon]["pos"]) in valid_tiles:
                    game_data[player]["dragon"][dragon]['current_health'] -= damage
                    #number of turn without attack:
                    game_data["idle_turn"]=0
    return game_data

def check_death(game_data:dict)->dict:
    """ check entities death
    
    Parameters:
    game_data: dictionnary of all game data (dict)
    
    Return
    ------
    game_data: dictionnary of all game data (dict)
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 23/02/25)
    implementation: De Braekeleer Mickaël( v.1 23/03/25)
    """
    #check for every entity that belongs to player1 or player2
    for player in ["player1", "player2"]:
        for apprentice in list(game_data[player]["apprentices"]):
            #check if apprentice is dead
            if game_data[player]["apprentices"][apprentice]['current_health'] <1:
                #if apprentice have linked dragon, delete them all aswell
                for linked_dragon in game_data[player]["apprentices"][apprentice]["linked_dragon"]:
                    if linked_dragon in game_data[player]["dragon"]:
                        del game_data[player]["dragon"][linked_dragon]
                del game_data[player]["apprentices"][apprentice]

        for dragon in list(game_data[player]["dragon"]):
            #check if dragon is dead
            if  game_data[player]["dragon"][dragon]['current_health']<1:
                #get dragon master (linked_apprentice) and damage him
                master=game_data[player]["dragon"][dragon]["linked_apprentice"]
                if master in game_data[player]["apprentices"]:
                    game_data[player]["apprentices"][master]["current_health"] -= 10
                    if dragon in game_data[player]["apprentices"][master]["linked_dragon"]:
                        game_data[player]["apprentices"][master]["linked_dragon"].remove(dragon)
                    if game_data[player]["apprentices"][master]["current_health"] < 1:
                        del game_data[player]["apprentices"][master]
                del game_data[player]["dragon"][dragon]        
    return game_data

    
    
def move(game_data:dict, player:str, order:str)->dict:
    """Move an apprentice or a dragon if move is possible 
    
    parameters
    ----------
    orders : list of player orders (list)
    game_data : dictionnary of dictionnary that contain all game data about player and the map (dict)
        
    return
    ------
    game_data : dictionnary of dictionnary that contain all game data about player and the map after move (dict)
    
    Version
    -------
    specification: Aymane el abbassi(20/02/2025)
    implementation: Aymane el abbassi(v.1 20/02/2025)
    implementation: Mitta Kylian, De Braekeleer Mickaël( v.2 22/03/25) 
    """
    
    # Retrieve the number of rows and columns from game_data
    max_rows = game_data['map'][0]  
    max_cols = game_data['map'][1]  
    

    #Split the order into two parts: the element and the position
    order=order.split(':@')
    element = order[0]
    position = order[1]  
    position_list = position.split("-")  # Split the position into two parts: row and column
    if position_list[0].isdigit() and position_list[1].isdigit():
        row = int(position_list[0])  
        col = int(position_list[1])
        pos=[0, 0]
        path=False

        #Check if entity is a dragon or an apprentice and add their pos path
        if element in game_data[player]["apprentices"]:
            path=[player, "apprentices", element, "pos"]
        elif element in game_data[player]["dragon"]:
            path=[player, "dragon", element, "pos"]    
                    
        #check if entity exist (path exist)
        if path!=False:          
            #Check if the position is within the game board limits
            if row >= 0 and row < max_rows and col >= 0 and col < max_cols:            
                pos=game_data[path[0]][path[1]][path[2]][path[3]]
                current_row=pos[0]
                current_col=pos[1] 
                #Check if the movement is only one cell (only on step in every direction)
                if ((current_row+1==row or current_row==row or current_row-1==row) and 
                    (current_col+1==col or current_col==col or current_col-1==col)):
                    #Update the position of the element in game_data
                    game_data[path[0]][path[1]][path[2]][path[3]]  = [row, col]      
    return game_data  

def regeneration(game_data:dict)->dict:
    """The function regenerate health points to the dragons and the apprentices at the end of the turn without exceeding their max health
    Parameters
    ----------
    game_data : Dictionnary of all game data (dict)

    Returns
    -------
    game_data : dictionnary of all game data after characters regeneration (dict)
    
    Version
    -------
    specification: Hamza SOSSEY-ALAOUI ( v.1 20/02/25)
    implementation: Hamza SOSSEY-ALAOUI( v.1 16/03/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël( v.2 22/03/25)
    """
    #check entity for all player
    for player in ["player1", "player2"]:
        #regenerate dragons or apprentices
        for entities in ["dragon", "apprentices"]:
            #regenerate each entity
            for entity in game_data[player][entities]:
                game_data[player][entities][entity]["current_health"]+=game_data[player][entities][entity]["regeneration"]
                #check if current health go above max health
                if game_data[player][entities][entity]["current_health"]>game_data[player][entities][entity]["max_health"]:
                    #then current health is just equals to max health
                    game_data[player][entities][entity]["current_health"]=game_data[player][entities][entity]["max_health"]
        
    return game_data



def end_game(winner):
    """ show the winner of the game 
    
    parameters
    ----------
    winner : name of the winner (str)


    specification: Mitta kylian (02/03/25)
    implementation: Mitta kylian (21/03/25)
    """

    #print blank space
    print("")
    print("")
    print("")
    
    #check winner
    if winner == "player1":
        print("Le Gagnant est Player 1!")
    elif winner == "player2":
        print("Le Gagnant est Player 2!")
    elif winner == "draw":
        print("La partie s'est terminée sur une égalité !")
    else:
        print("La partie est finie à cause de 100 tours sans attaque")
    
    #print blank space
    print("")
    print("")
    print("")
    
def check_win(game_data:dict, silent:bool)->bool:
    """check if one of the two player won
    
    parameters
    ----------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    silent : if silent or not
    
    return
    ------
    game: if the game is running or not (bool)
    
    specification: De Braekeleer Mickael (23/03/25)
    implementation: De Braekeleer Mickael (23/03/25)
    """
    #game end by default
    game=False
    #check who won
    if not game_data["player1"]["apprentices"] and not game_data["player2"]["apprentices"]:
        if not silent:
            end_game("draw")
    elif not game_data["player1"]["apprentices"]:
        if not silent:
            end_game("player2")
    elif not game_data["player2"]["apprentices"]:
        if not silent:
            end_game("player1")
    elif game_data["idle_turn"]==100:
        if not silent:
            end_game("no_winner")
    else:
        #if no winner, game continue
        game=True
        
    return game
    
    

   
# main function
def play_game(map_path, group_1, type_1, group_2, type_2):
    """Play a game.
    
    Parameters
    ----------
    map_path: path of map file (str)
    group_1: group of player 1 (int)
    type_1: type of player 1 (str)
    group_2: group of player 2 (int)
    type_2: type of player 2 (str)
    
    Notes
    -----
    Player type is either 'human', 'AI' or 'remote'.
    
    If there is an external referee, set group id to 0 for remote player.
    
    """
    game=True
    game_data=load_map(map_path)
    
    display(game_data)
    time.sleep(0.5)


    # create connection, if necessary
    if type_1 == 'remote':
        connection = create_connection(group_2, group_1)
    elif type_2 == 'remote':
        connection = create_connection(group_1, group_2)
        
    while game:
        all_orders=[]
        # get orders of player 1 and notify them to player 2, if necessary
        orders=[]
        if type_1 == 'remote':
            orders = get_remote_orders(connection)
        elif type_1 == "human":
            orders = Get_orders(game_data, "player1")
        else:
            orders = get_AI_orders(game_data, "player1")
        if type_2 == 'remote':
            notify_remote_orders(connection, orders) 
        all_orders.append(orders)
        
        # get orders of player 2 and notify them to player 1, if necessary
        orders=[]
        if type_2 == 'remote':
            orders = get_remote_orders(connection)
        elif type_2 == "human":
            orders = Get_orders(game_data, "player2")
        else:
            orders = get_AI_orders(game_data, "player2")
        if type_1 == 'remote':
            notify_remote_orders(connection, orders)
            
        all_orders.append(orders)
            
        #execute players orders
        game_data=action(game_data,  all_orders)  
        
        game_data=regeneration(game_data)
        game_data=hatch_egg(game_data)
        game_data["idle_turn"]+=1
        
        for player in ["player1", "player2"]:
            if game_data[player]["summon"]>0:
                game_data[player]["summon"]-=1
                
        display(game_data)
        time.sleep(0.2)
        
        game=check_win(game_data, False)     

    # close connection, if necessary
    if type_1 == 'remote' or type_2 == 'remote' and not game:
        close_connection(connection)
        
#program
map_path="C:/Users/coram/OneDrive/Desktop/projet/map.drk"       
play_game(map_path, 6, "AI", 6, "AI")