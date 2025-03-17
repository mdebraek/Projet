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
    specification: Hamza SOSSEY-ALAOUI (v.1 20/02/25)
    """
    all_app1=game_data['player1']['apprentices'] 
    all_app2=game_data['player2']['apprentices']
    allapps=[]
    allapps.append(all_app1)
    allapps.append(all_app2)
    for apprentice in allapps:
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
    
    all_drag1=game_data['player1']['dragon'] 
    all_drag2=game_data['player2']['dragon']
    alldrags=[]
    alldrags.append(all_drag1)
    alldrags.append(all_drag2) 
    for dragon in alldrags:
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