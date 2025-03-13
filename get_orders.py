def Get_orders(game_data:dict) -> list:
    """Ask the player what he want to play

    parameters
    ----------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    
    return
    ------
    orders ; list of order with the correct format (list)
    Version
    -------
    specification: Mitta Kylian, De Braekeleer Mickaël (v.1 20/02/25)
    implementation: Mitta Kylian (v1 03/03/25)
    
    """
    orders_player_1=[]
    orders_player_2=[]


    list_player=orders_player_1
    player="player1"

    for temp in range(2):

        orders=input("ordres ->")

        order=orders.split(" ")
        for order in orders:
             
                  if f"{player}summon" in order:
                      list_player.append(order)
                      
                  elif ':' in order:
                        check=order.split(":")

                            if check[1][0]=="@" 
                            and check[1][1].isdigit() 
                            and check[1][2]=="-" 
                            and check[1][3].isdigit()
                            and check[0] in game_data[player]["apprentices"]:
                                 list_player.append(order)
                 
                        elif check[0] in game_data[player]["dragon"]:

                            if check[1] in {"xN","xNE","xE","xSE","xS","xSW","xW","xNW"}:
                                 list_player.append(order)
        list_player=orders_player_2
        player="player2"
        

    return  orders_player_1,orders_player_2
                       
