def action(game_data:dict , orders:list)->dict :
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
    """
    call(game_data)

    attack(game_data)

    regeneration(game_data)
    return game_data