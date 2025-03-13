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
    for order in get_orders('player1',game_data):
        if 'summon' in order:
            #get position of where dragons and apprentices should go when the call
            altars1=game_data['player1']['altars']
            #get all the dragons and apprentices  
            all_app1=game_data['player1']['apprentices']
            all_drag1=game_data['player1']['dragon']
            posof_AppDrag1=[]
            for apprentice in all_app1:
                posof_app=apprentice['pos']
                posof_AppDrag1.append(posof_app)
            for dragon in all_drag1:
                posof_drag=dragon['pos']
                posof_AppDrag1.append(posof_drag)
            for pos in posof_AppDrag1:
                pos[0]=altars1[0] and pos[1]=altars1[1]
        
    for order in get_orders('player2',game_data):
        if 'summon' in order:
            altars2=game_data['player2']['altars']
            #get all the dragons and apprentices  
            all_app2=game_data['player2']['apprentices']
            all_drag2=game_data['player2']['dragon']
            posof_AppDrag2=[]
            for apprentice in all_app2:
                posof_app=apprentice['pos']
                posof_AppDrag2.append(posof_app)
            for dragon in all_drag2:
                posof_drag=dragon['pos']
                posof_AppDrag2.append(posof_drag)
            for pos in posof_AppDrag2:
                pos[0]=altars2[0] and pos[1]=altars2[1]

    display(game_data)
    return game_data    
    

