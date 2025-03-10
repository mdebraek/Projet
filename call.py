def call(game_data):
    """The function to use the special ability of the player

    Parameters
    ----------
    game_data : Data structure of the game (dict)
    
    Returns
    -------
    game_data : dictionnary of all game data after potential call (dict)
    
    Version
    -------
    specification: Hamza SOSSEY-ALAOUI (v.1 20/02/25)
    """
    altars1=game_data['player1']['altars'] 
    posof_app1=game_data['player1']['apprentices']['pos']
    posof_drag1=game_data['player1']['dragon']['pos']
    posof_AppDrag1={**posof_app1,**posof_drag1}
    for pos in posof_AppDrag1:
        pos[0]=altars1[0] and pos[1]=altars1[1]
        
    
    altars2=game_data['player2']['altars']
    posof_app2=game_data['player2']['apprentices']['pos']
    posof_drag2=game_data['player2']['dragon']['pos']
    posof_AppDrag2={**posof_app2,**posof_drag2}
    for pos in posof_AppDrag2:
        pos[0]=altars2[0] and pos[1]=altars2[1]
        
    display(game_data)
    return game_data    
    
