def attack(game_data):
    """The function makes the dragon attack in the 8 directions with 2 boxes limit range
        Parameters:
        Game_Data : Data structure of the game (dict)
        Version
        -------
        specification: Hamza SOSSEY-ALAOUI (v.1 20/02/25)
        specification: Hamza SOSSEY-ALAOUI (v.2 17/03/25)
        implementation: Hamza SOSSEY-ALAOUI (v.1 17/03/25)
    """
    #get the orders
    for order in get_orders('player1',game_data):
        #remove the :x from the order and putting all of the existing dragons and apprentices in one list
        if ':x' in order:
            order=order.split(':x')
            all_drag1=game_data['player1']['dragon']
            all_drag2=game_data['player2']['dragon'] 
            all_app1=game_data['player1']['apprentices']
            all_app2=game_data['player2']['apprentices'] 
            all_app_drag=[]
            all_app_drag.append(all_drag1)
            all_app_drag.append(all_drag2)
            all_app_drag.append(all_app1)
            all_app_drag.append(all_app2)
            #loop of the dragons for player1 and getting all infos needed
            for dragon in game_data['player1']['dragon']:
                damage=dragon['attack_damage']
                portee=dragon['attack_range']
                posistion=dragon['pos']
                #loop in the list of all of the dragons and apprentices and getting infos needed
                for dragonite in all_app_drag:
                    pos_dragonite=dragonite['pos']
                    health_dragonite=dragonite['current_health']
                    #while the order of attack is in the range attack of the dragon
                    while (pos_dragonite[0] - posistion[0]) < portee and (pos_dragonite[1] - posistion[1]) < portee :
                        #in all the directions, if a random dragon friendly or ennemy exists in the range of the dragon, it is going to be dammaged 
                        if 'N' in order:
                            if (pos_dragonite[1] == posistion[1] +1) or (pos_dragonite[1] == posistion[1] +2):
                                health_dragonite -=damage
                        #in the multiple attack direction, both row and column are going to be browsed through
                        if 'NE' in order:
                            if ((pos_dragonite[0] == posistion[0]) +1 and (pos_dragonite[1] == posistion[1] +1)) or ((pos_dragonite[0] == posistion[0]) +2 and (pos_dragonite[1] == posistion[1] +2)):
                                health_dragonite -=damage
                        
                        if 'E' in order:
                            if (pos_dragonite[0] == posistion[0] +1) or (pos_dragonite[0] == posistion[0] +2):
                                health_dragonite -=damage
                        
                        if 'SE' in order:
                            if ((pos_dragonite[0] == posistion[0]) +1 and (pos_dragonite[1] == posistion[1] -1)) or ((pos_dragonite[0] == posistion[0]) +2 and (pos_dragonite[1] == posistion[1] -2)):
                                health_dragonite -=damage
                        
                        if 'S' in order:
                            if (pos_dragonite[1] == posistion[1] -1) or (pos_dragonite[1] == posistion[1] -2):
                                health_dragonite -=damage
                        
                        if 'SW' in order:
                            if ((pos_dragonite[0] == posistion[0]) -1 and (pos_dragonite[1] == posistion[1] -1)) or ((pos_dragonite[0] == posistion[0]) -2 and (pos_dragonite[1] == posistion[1] -2)):
                                health_dragonite -=damage
                        
                        if 'W' in order:
                            if (pos_dragonite[0] == posistion[0] -1) or (pos_dragonite[0] == posistion[0] -2):
                                health_dragonite -=damage
                        
                        if 'NW' in order:
                            if ((pos_dragonite[0] == posistion[0]) -1 and (pos_dragonite[1] == posistion[1] +1)) or ((pos_dragonite[0] == posistion[0]) -2 and (pos_dragonite[1] == posistion[1] +2)):
                                health_dragonite -=damage

            #loop of the dragons for player2 and getting all infos needed
            for dragon in game_data['player2']['dragon']:
                damage=dragon['attack_damage']
                portee=dragon['attack_range']
                posistion=dragon['pos']
                #loop in the list of all of the dragons and apprentices and getting infos needed
                for dragonite in all_app_drag:
                    pos_dragonite=dragonite['pos']
                    health_dragonite=dragonite['current_health']
                    #while the order of attack is in the range attack of the dragon
                    while (pos_dragonite[0] - posistion[0]) < portee and (pos_dragonite[1] - posistion[1]) < portee :
                        #in all the directions, if a random dragon friendly or ennemy exists in the range of the dragon, it is going to be dammaged 
                        if 'N' in order:
                            if (pos_dragonite[1] == posistion[1] +1) or (pos_dragonite[1] == posistion[1] +2):
                                health_dragonite -=damage
                        #in the multiple attack direction, both row and column are going to be browsed through
                        if 'NE' in order:
                            if ((pos_dragonite[0] == posistion[0]) +1 and (pos_dragonite[1] == posistion[1] +1)) or ((pos_dragonite[0] == posistion[0]) +2 and (pos_dragonite[1] == posistion[1] +2)):
                                health_dragonite -=damage
                        
                        if 'E' in order:
                            if (pos_dragonite[0] == posistion[0] +1) or (pos_dragonite[0] == posistion[0] +2):
                                health_dragonite -=damage
                        
                        if 'SE' in order:
                            if ((pos_dragonite[0] == posistion[0]) +1 and (pos_dragonite[1] == posistion[1] -1)) or ((pos_dragonite[0] == posistion[0]) +2 and (pos_dragonite[1] == posistion[1] -2)):
                                health_dragonite -=damage
                        
                        if 'S' in order:
                            if (pos_dragonite[1] == posistion[1] -1) or (pos_dragonite[1] == posistion[1] -2):
                                health_dragonite -=damage
                        
                        if 'SW' in order:
                            if ((pos_dragonite[0] == posistion[0]) -1 and (pos_dragonite[1] == posistion[1] -1)) or ((pos_dragonite[0] == posistion[0]) -2 and (pos_dragonite[1] == posistion[1] -2)):
                                health_dragonite -=damage
                        
                        if 'W' in order:
                            if (pos_dragonite[0] == posistion[0] -1) or (pos_dragonite[0] == posistion[0] -2):
                                health_dragonite -=damage
                        
                        if 'NW' in order:
                            if ((pos_dragonite[0] == posistion[0]) -1 and (pos_dragonite[1] == posistion[1] +1)) or ((pos_dragonite[0] == posistion[0]) -2 and (pos_dragonite[1] == posistion[1] +2)):
                                health_dragonite -=damage
    return game_data