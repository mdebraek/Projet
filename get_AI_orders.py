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
