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
