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
    dict_ofapp1=game_data['player1']['apprentices'] 
    dict_ofapp2=game_data['player2']['apprentices']
    dict_ofapps={**dict_ofapp1,**dict_ofapp2}
    for apprentice in dict_ofapps:
        reg_app=apprentice['regeneration']
        curr_hea_app=apprentice['current_health']
        pv_app=apprentice['max_health']
        if curr_hea_app >= pv_app :
            return game_data
        else:
            hea_diff=pv_app - curr_hea_app
            if hea_diff>=reg_app:
                curr_hea_app+=reg_app
            else:
                curr_hea_app+=hea_diff
        return game_data
    
    dict_ofdrag1=game_data['player1']['dragon'] 
    dict_ofdrag2=game_data['player2']['dragon']
    dict_ofdrags={**dict_ofdrag1,**dict_ofdrag2}
    for dragon in dict_ofdrags:
        reg_drag=dragon['regeneration']
        curr_hea_drag=dragon['current_health']
        pv_drag=dragon['max_health']
        if curr_hea_drag >= pv_drag :
            return game_data
        else:
            hea_diff=pv_drag - curr_hea_drag
            if hea_diff>=reg_drag:
                curr_hea_drag+=reg_drag
            else:
                curr_hea_drag+=hea_diff
        return game_data