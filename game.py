import blessed, math, os, time, random
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
    specification: Mitta Kylian, De Braekeleer Mickaël (20/02/25)
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
    specification: De Braekeleer Mickaël (06/03/25)
    implementation: De Braekeleer Mickaël (06/03/25)
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
    specification: De Braekeleer Mickaël (07/03/25)
    implementation: De Braekeleer Mickaël (07/03/25)
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
    specification: De Braekeleer Mickaël (10/03/25)
    implementation: De Braekeleer Mickaël (10/03/25)
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
    specification: Mitta Kylian, De Braekeleer Mickaël (20/02/25)
    implementation: Mitta Kylian, De Braekeleer Mickaël (06/03/25)
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
    specification: Mitta Kylian, De Braekeleer Mickaël (20/02/25)
    implementation: Mitta Kylian (03/03/25)
    
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
        
    return  orders

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
    
def action(game_data:dict ,orders:list)->dict :
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
    """

    for order in orders_player:

    #1st action
    call(game_data)
    #2nd action
    hatch_egg(game_data)
    #3rd action
    attack(game_data)
    #4th action
    move(orders,game_data)
    #5th action
    regeneration(game_data)
    return game_data








def hatch_egg(game_data):
    """hatch eggs if apprentice are on it 
        Parametres :
        ----------
        game_data : dic of all the game(dic)
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

        # loop for each egg on the board
        for egg in game_data["eggs"]:

            # loop for each apprentice of the player
            for apprentices in game_data[player]['apprentices']:

                # check if the positions are identical
                if apprentices['pos'] == egg['pos']: 
                    egg['time_to_hatch'] -= 1
                    if egg['time_to_hatch']== 0:

                        # hatching
                        game_data[player]['dragon'].append(egg)
                        game_data[player]['dragon'][egg] = {
                            'pos': egg['pos'],
                            'pv': egg['max_health'],
                            'currenthealth':egg['currenthealth'],
                            'regeneration': egg['regeneration'],
                            'attack_damage': egg['attack_damage'],
                            'attack_range': egg['attack_range'] }
                        
                        

                        # delete the old egg
                        del game_data[player]["eggs"][egg]

                       
    return game_data

def call(player,game_data):
    """The function to use the special ability of the player

    Parameters
    ----------
    game_data : Data structure of the game (dict)
    
    Returns
    -------
    game_data : dictionnary of all game data after the call (dict)
    
    Version
    -------
    specification: Hamza SOSSEY-ALAOUI (20/02/25)
    implementation: Hamza SOSSEY-ALAOUI(v1 15/03/25)
    implementation: Mitta kylian(v2 17/03/25)
    """
    # takes positions of the altar
    pos_altar_y,pos_altar_x=game_data[player]['altars']['pos']

    # move apprentices to the altar
    for apprentice in game_data[player]["apprentices"]:
        apprentice["pos"] = pos_altar_y,pos_altar_x

    # move dragons to the altar
    for dragon in game_data[player]["dragon"]:
        dragon["pos"] = pos_altar_y,pos_altar_x
        
    return game_data


def regeneration(game_data):
    """The function regenerate health points to the dragons and the apprentices at the end of the turn without exceeding their max health
    Parameters
    ----------
    game_data : Dictionnary of all game data (dict)

    Returns
    -------
    game_data : dictionnary of all game data after characters regeneration (dict)
    
    Version
    -------
    specification: Hamza SOSSEY-ALAOUI (20/02/25)
    implementation: Hamza SOSSEY-ALAOUI(16/03/25)
    """
    #combined all apprentices/dragons on the board
    all_app1=game_data['player1']['apprentices'] 
    all_app2=game_data['player2']['apprentices']
    all_apps=[]
    all_apps.append(all_app1)
    all_apps.append(all_app2)
    
    all_drag1=game_data['player1']['dragon'] 
    all_drag2=game_data['player2']['dragon']
    all_drags=[]
    all_drags.append(all_drag1)
    all_drags.append(all_drag2) 


    # regeneration of apprentices
    for apprentice in all_apps:
        reg_app=apprentice['regeneration']
        curr_hea_app=apprentice['current_health']
        pv_app=apprentice['max_health']
        if curr_hea_app >= pv_app :
            curr_hea_app=curr_hea_app
        else:
            hea_diff=pv_app - curr_hea_app
            if hea_diff>=reg_app:
                curr_hea_app+=reg_app
            else:
                curr_hea_app+=hea_diff

    # regeneration of dragons
    for dragon in all_drags:
        reg_drag=dragon['regeneration']
        curr_hea_drag=dragon['current_health']
        pv_drag=dragon['max_health']
        if curr_hea_drag >= pv_drag :
            curr_hea_drag=curr_hea_drag
        else:
            hea_diff=pv_drag - curr_hea_drag
            if hea_diff>=reg_drag:
                curr_hea_drag+=reg_drag
            else:
                curr_hea_drag+=hea_diff


    return game_data

def attack(player,orders,game_data):
    """The function makes the dragon attack in the 8 directions with 2 boxes limit range
        Parameters:
        Game_Data : Data structure of the game (dict)
        Version
        -------
        specification: Hamza SOSSEY-ALAOUI (v.1 20/02/25)
        specification: Hamza SOSSEY-ALAOUI (v.2 17/03/25)
        implementation: Hamza SOSSEY-ALAOUI (17/03/25)
    """
    for order in orders:
        order=order.split(':x')
        damage=game_data[player]["dragon"][order[0]]['attack_damage']
        attack_range=game_data[player]["dragon"][order[0]]['attack_range']


        pos_dragon_y,pos_dragon_x=game_data[player]["dragon"][order[0]]['pos']
        valid_tiles={}


        for check_attack in range(1,attack_range):
        
            if order[1] == "N":
                valid_tiles.append((pos_dragon_y-check_attack,pos_dragon_x))
            elif order[1] == "NE":
                valid_tiles.append((pos_dragon_y-check_attack,pos_dragon_x+check_attack))
            elif order[1] == "E":
                valid_tiles.append((pos_dragon_y,pos_dragon_x+check_attack))
            elif order[1] == "SE":
                valid_tiles.append((pos_dragon_y+check_attack,pos_dragon_x+check_attack))
            elif order[1] == "S":
                valid_tiles.append((pos_dragon_y+check_attack,pos_dragon_x))
            elif order[1] == "SW":
                valid_tiles.append((pos_dragon_y-+check_attack,pos_dragon_x-check_attack))
            elif order[1] == "W":
                valid_tiles.append((pos_dragon_y+check_attack,pos_dragon_x-check_attack))
            elif order[1] == "NW":
                valid_tiles.append((pos_dragon_y-check_attack,pos_dragon_x-check_attack))




        if player=="player1":
            the_other_player="player2"
        else:
            the_other_player="player1"

        for apprentice in game_data[the_other_player]["apprentice"]:

            if game_data[the_other_player]["apprentice"][apprentice]["pos"] in valid_tiles:

                game_data[the_other_player]["apprentice"][apprentice]['current_health'] -= damage

                if game_data[the_other_player]["apprentice"][apprentice]['current_health'] <1:

                    del game_data[the_other_player]["apprentice"][apprentice]



        

        for dragon in game_data[the_other_player]["dragon"]:

            if game_data[the_other_player]["dragon"][dragon]["pos"] in valid_tiles:

                game_data[the_other_player]["dragon"][dragon]['current_health'] -= damage

                if  game_data[the_other_player]["dragon"][dragon]['current_health']<1:

                    del game_data[the_other_player]["dragon"][dragon]

        return game_data



def end_game(winner):
    """ show the winner of the game 
    
    parameters
    ----------
    winner : name of the winner (str)


    specification: Mitta kylian (02/03/25)
    implementation: Mitta kylian (21/03/25)
    """


    if winner=="player1":
        print("the winner is the player 1")
    else:
        print("the winner is the player 2")


def move(orders:list, game_data:dict)->dict:
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
    specification: 
    implementation: 
    """
    
    # Retrieve the number of rows and columns from game_data
    max_rows = game_data['map'][0]  
    max_cols = game_data['map'][1]  
    

    for order in orders:  
        if ':@' in order:  #Check if the order contains the ':@' separator
            #Split the order into two parts: the element and the position
            order.split(':@')
            element = order[0]
            position = order[1]  
            position_list = position.split('-')  # Split the position into two parts: row and column
            row = position_list[0]  
            col = position_list[1]
            pos=[0, 0]
            path=False
            
            #Check if entity is a dragon or an apprentice and add their pos path
            if element in game_data["player1"]["apprentices"] or element in game_data["player2"]["apprentices"]:
                if element in game_data["player1"]["apprentices"]:
                    path=["player1", "apprentices", "pos"]
                else:
                    path=["player2", "apprentices", "pos"]
            elif element in game_data["player1"]["dragon"] or element in game_data["player2"]["dragon"]:
                if element in game_data["player1"]["dragon"]:
                    path=["player1", "dragon", "pos"]
                else:
                    path=["player2", "dragon", "pos"]      
                    
            #check if entity exist (path exist)
            if path!=False:          
                #Check if the position is within the game board limits
                if row >= 0 and row < max_rows and col >= 0 and col < max_cols:            
                    pos=game_data[path[0]][path[1]][path[2]] 
                    current_row=pos[0]
                    current_col=pos[1] 
                    #Check if the movement is only one cell (only on step in every direction)
                    if ((current_row+1==row or current_row==row or current_row-1==row) and 
                        (current_col+1==col or current_col==col or current_col-1==col)):
                        #Update the position of the element in game_data
                        game_data[path[0]][path[1]][path[2]]  = [row, col]      
    return game_data  
   
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
