def info_bracket(player:str,game_data: dict)->list:
    """generate info bracket for a player (info on right or left of the display)

    Parameters
    ----------
    player : str name of the player (str)
    game_data : dictionnary of all game data(dict)
    
    Returns
    -------
    player_info : list of all info on a player line by line (list)

    Version
    -------
    specification: De Braekeleer Mickaël (v.1 06/03/25)
    implementation: De Braekeleer Mickaël (v.1 06/03/25)
    """
    print(player)
    print(game_data[player])
    
    #initialisation of the returned list 
    player_info=[]
    
    #Add altar position to the brackets
    player_info.append("-Altar:")
    position=game_data[player]["Altar"]
    player_info.append(f"   >pos : {position[0]} {position[1]}")
    #Add time for next call to the brackets
    Cooldown_Summon=game_data[player]["call"]
    if Cooldown_Summon==0:
        player_info.append("Appel disponnible")
    else:
        player_info.append(f"Appel : {Cooldown_Summon} tours")   
    #Browse each apprentic of a player and add their info to the brackets
    for apprentice in game_data[player]["apprentices"]:
        player_info.append(f"   -{apprentice} :")
        player_info.append(f"   >PV : {game_data[player]["apprentices"][apprentice]["current_health"]}/{game_data[player]["apprentices"][apprentice]["max_health"]}")
        #temporary variable for position of the character 
        position=game_data[player]["apprentices"][apprentice]["pos"]
        player_info.append(f"   >pos : {position[0]} {position[1]} ")
    #Browse each dragon of a player and add their info to the brackets
    for dragon in game_data[player]["dragon"]:
        if dragon==game_data[player]["dragon"][0]:
            player_info.append(f"-Dragon🐉:")
        player_info.append(f"   -{dragon}:")
        player_info.append(f"   >PV : {game_data[player]["dragon"][dragon]["current_health"]}/{game_data[player]["dragon"][dragon]["max_health"]}")
        player_info.append(f"   >Dégats : {game_data[player]["dragon"][dragon]["attack_damage"]}")
        player_info.append(f"   >Portée : {game_data[player]["dragon"][dragon]["attack_range"]}")
        #temporary variable for position of the character 
        position=game_data[player]["dragon"][dragon]["pos"]
        player_info.append(f"   >pos : {position[0]} {position[1]} ")
    return player_info
