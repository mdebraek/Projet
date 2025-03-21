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
    implementation: Hamza Sossey-Alaoui (v.1 17/03/25)
    """
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