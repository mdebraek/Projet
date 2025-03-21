def hatch_egg(game_data):
    """hatch eggs if apprentice are on it 
        Parametres :
        ----------
        game_data : dic of all the game(dic)
        Returns
        -------
        game_data: dictionnary of all the game_data after a potentially hatching eggs (dic)
        Version 
        -------
        specification : Aymane el abbassi(20/02/2025)
        implementation: Aymane el abbassi(v1 15/03/25)
        implementation: Mitta Kylian (v2 19/03/25)
    """
     # loop for each player
    for player in ['player1', 'player2']:

        # loop for each egg on the board
        for egg in game_data["eggs"]:

            # loop for each apprentice of the player
            for apprentices in game_data[player]['apprentices']:

                # check if the positions are identical
                if apprentices['pos'] == egg['pos']: 
                    egg['time_to_hatch'] -= 1
                    if egg['time_to_hatch']== 0:

                        # hatching
                        game_data[player]['dragon'].append(egg)
                        game_data[player]['dragon'][egg] = {
                            'pos': egg['pos'],
                            'pv': egg['max_health'],
                            'currenthealth':egg['currenthealth'],
                            'regeneration': egg['regeneration'],
                            'attack_damage': egg['attack_damage'],
                            'attack_range': egg['attack_range'] }
                        
                        

                        # delete the old egg
                        del game_data[player]["eggs"][egg]

                       
    return game_data
