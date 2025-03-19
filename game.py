import blessed, math, os, time
term = blessed.Terminal()

from remote_play import create_connection, get_remote_orders, notify_remote_orders, close_connection



# other functions
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
    player_info.append("-Altar🏰:")
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
    word : any string (str)

    Returns
    -------
    count : number of character of the word (int)
    
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 07/03/25)
    implementation: De Braekeleer Mickaël (v.1 07/03/25)
    """
    count=0
    for char in word:
        if char in "🚹🚺🐉🟨🏰🥚🟩🟥":
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
    specification: De Braekeleer Mickaël (v.1 10/03/25)
    implementation: De Braekeleer Mickaël (v.1 10/03/25)
    """
    map_grid=[["🟥"]*(Size_Y+1) for i in range(Size_X+1)]

    
    #all position for player 1 team
    pos_altar_p1=game_data["player1"]["Altar"]
    map_grid[pos_altar_p1[0]][pos_altar_p1[1]]="🏰"
    for apprentice in game_data["player1"]["apprentices"]:
        pos_X=game_data["player1"]["apprentices"][apprentice]["pos"][0]
        pos_Y=game_data["player1"]["apprentices"][apprentice]["pos"][1]
        map_grid[pos_X][pos_Y]="🚹"
    for dragon in game_data["player1"]["dragon"]:
        pos_X=game_data["player1"]["dragon"][dragon]["pos"][0]
        pos_Y=game_data["player1"]["dragon"][dragon]["pos"][1]
        map_grid[pos_X][pos_Y]="🐉"  
    #all position for player 2 team
    pos_altar_p2=game_data["player2"]["Altar"]
    map_grid[pos_altar_p2[0]][pos_altar_p2[1]]="🏰"
    for apprentice in game_data["player2"]["apprentices"]:
        pos_X=game_data["player2"]["apprentices"][apprentice]["pos"][0]
        pos_Y=game_data["player2"]["apprentices"][apprentice]["pos"][1]
        map_grid[pos_X][pos_Y]="🚺"
    for dragon in game_data["player2"]["dragon"]:
        pos_X=game_data["player2"]["dragon"][dragon]["pos"][0]
        pos_Y=game_data["player2"]["dragon"][dragon]["pos"][1]
        map_grid[pos_X][pos_Y]="🐉"
    for egg in game_data["eggs"]:
        pos_X=game_data["eggs"][egg]["pos"][0]
        pos_Y=game_data["eggs"][egg]["pos"][1]
        map_grid[pos_X][pos_Y]="🥚"
    return map_grid

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
    
    #initial pos
    x=float(1)
    y=int(1)
    
    map_grid=generate_map_grid(Size_X, Size_Y, game_data)
    
    
    
    #initial info bracket
    player_1=["Player 1 :"]
    player_2=["Player 2 :"]
    player_1.extend(info_bracket("player1", game_data))
    player_2.extend(info_bracket("player2", game_data))
    

    #maximum vertical size of display
    max_size_Y=max(Size_Y*2+1, max(4+len(game_data["player1"]["apprentices"])+len(game_data["player1"]["dragon"]),
                                   4+len(game_data["player2"]["apprentices"])+len(game_data["player2"]["dragon"]),))
    
    #maximum horiziontal size of left display brackets
    max_info_p1=max([len(elem) for elem in player_1])
    
    #generate display
    for line in range (max_size_Y):
        #print player 1 info brackets
        if len(player_1)>line:
            print(player_1[line],end="")
            print(" "*(max_info_p1-custom_len(player_1[line])),end="")
        #if no info for player 1, just print a blank space
        else:
            print(" "*max_info_p1,end="")
            
        #generate Array
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
                    if custom_len(map_grid[int(x)][y])==2 and int(x)==float(x):
                        print(f"{map_grid[int(x)][y]}",end="")
                    elif int(x)==float(x):
                        print(f"{map_grid[int(x)][y]}"*2,end="")
                    x+=0.5
            x=float(1)
            y+=1
            print("|",end="")
        
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
    specification: Mitta Kylian, De Braekeleer Mickaël (v.1 20/02/25)
    implementation: Mitta Kylian (v1 03/03/25)
    
    """
    orders_player=[]

    orders=input(f"{player}, veuillez entrer votre ordre ->")

    orders=orders.split(" ")
    for order in orders:
        if "summon" in order:
            orders_player.append(order)
                      
        elif ':' in order:
            check=order.split(":")
            if check[1][0]=="@" and '-' in check[1]: 
                check[1]=check[1].strip("@")
                check_temp=check[1].split("-")
            if (check_temp[0].isdigit() 
            and check_temp[1].isdigit()
            and check[0] in game_data[player]["apprentices"]):
                orders_player.append(order)
                 
            
            if check[0] in game_data[player]["dragon"]:
                if check[1][0]=="@" and '-' in check[1]: 
                    check[1]=check[1].strip("@")
                    check_temp=check[1].split("-")
                
                if check_temp[0].isdigit() and check_temp[1].isdigit():
                    orders_player.append(order)
                       
                if check[1] in {"xN","xNE","xE","xSE","xS","xSW","xW","xNW"}:
                    orders_player.append(order)
        
    return  orders_player

def get_AI_orders(game_data:dict, player:str)->list:
    """get random AI orders (basic)

    parameters
    ----------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    player : number of the player (int)

    
    returns
    -------
    orders : order with the correct format (list)
    
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 13/03/25)
    implementation:  De Braekeleer Mickaël (v.1 19/03/25)

    """
    #init orders variable
    orders=[]
    
    #random summon
    if random.randint(1, 10)==1:
        orders.append("summon")
    #for all entity of a player, randomize orders
    for apprentice in game_data[player]["apprentices"]:
        #random move
        random_direction=[[0, 0], [0, 1], [1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1], [0, -1], [-1, 0]]
        random_direction=random_direction[random.randint(0, 7)]
        position=game_data[player]["apprentices"][apprentice]["pos"]
        orders.append(f"{apprentice}:@{position[0]+random_direction[0]}-{position[1]+random_direction[1]}")   
    for dragon in game_data[player]["dragon"]:
        #random move or attack
        if random.randint(1, 2)==1:
            #random move
            random_direction=[[0, 0], [0, 1], [1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1], [0, -1], [-1, 0]]
            random_direction=random_direction[random.randint(0, 7)]
            position=game_data[player]["dragon"][dragon]["pos"]
            orders.append(f"{dragon}:@{position[0]+random_direction[0]}-{position[1]+random_direction[1]}")  
        else: 
            #random attack
            random_direction=["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
            random_direction=random_direction[random.randint(0, 7)]
            orders.append(f"{dragon}:x{random_direction}")
            
    return orders               

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


    # create connection, if necessary
    if type_1 == 'remote':
        connection = create_connection(group_2, group_1)
    elif type_2 == 'remote':
        connection = create_connection(group_1, group_2)

    while game:
        display(game_data)
        time.sleep(1.5)


        # get orders of player 1 and notify them to player 2, if necessary
        if type_1 == 'remote':
            orders = get_remote_orders(connection)
        elif type_1 == "human":
            orders = Get_orders(game_data, "player1")
        else:
            orders = get_AI_orders(game_data, 1)
        if type_2 == 'remote':
            notify_remote_orders(connection, orders)
            
        print(orders)
        time.sleep(10)
            
        display(game_data)
        time.sleep(1)
        # get orders of player 2 and notify them to player 1, if necessary
        if type_2 == 'remote':
            orders = get_remote_orders(connection)
        elif type_2 == "human":
            orders = Get_orders(game_data, "player2")
        else:
            orders = get_AI_orders(game_data, 2)
        if type_1 == 'remote':
            notify_remote_orders(connection, orders)
            
        display(game_data)
        time.sleep(1)
        


    # close connection, if necessary
    if type_1 == 'remote' or type_2 == 'remote' and not game:
        close_connection(connection)
        
        
map_path="C:/Users/coram/OneDrive/Desktop/projet/map.drk"       
play_game(map_path, 6, "human", 6, "human")
