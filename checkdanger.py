def check_danger(game_data,player):
    """
    Checks wether there is a danger or not near the AI
    parameters:
    ----------
    game_data: The data structure of the game (dict)
    player: The player (string)
    returns:
    -------
    True si il y en a, False si non (bool)
    """
    if player=="player1":
        ennemy_player="player2"
    else:
        ennemy_player="player1"
    
    all_drag=game_data[ennemy_player]["dragons"]
     
        
        
    for entity in all_drag:
            entity_pos=game_data[ennemy_player]["dragons"][entity]["pos"]
            entity_pos_x=entity_pos[0]
            entity_pos_y=entity_pos[1]
            for dragon in game_data[player]["dragons"]:
                drag_pos= game_data[player]["dragons"][dragon]["pos"]
                drag_pos_x=drag_pos[0]
                drag_pos_y=drag_pos[1]
                return  abs(entity_pos_x-drag_pos_x)<= 2 and  abs(entity_pos_y-drag_pos_y)<= 2 
                        
                
            for apprentice in game_data[player]["apprentices"]:
                app_pos= game_data[player]["apprentices"][apprentice]["pos"]
                app_pos_x=app_pos[0]
                app_pos_y=app_pos[1]
                return abs( (entity_pos_x-app_pos_x)<= 2 and (entity_pos_y-app_pos_y)<= 2 )
                        
        
