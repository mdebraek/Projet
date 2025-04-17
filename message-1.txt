import random
def search_enemies(game_data: dict, player: str,dragon,enemy) -> list:
    """
    Recherche les ennemis autour d'une entité donnée et renvoie une liste des ennemis à proximité.

    Paramètres :
    - game_data : dict, les données actuelles du jeu, qui contiennent des informations sur les entités, leurs positions, etc.
    - player : str, le nom du joueur pour lequel on fait la recherche ("player1" ou "player2").
    - entity : str, le nom de l'entité à vérifier (un dragon ou un apprenti). C'est l'entité dont on cherche les ennemis autour.

    Retourne :
    - list : une liste contenant les ennemis autour de l'entité donnée (ceux qui sont à une case de distance).
    """

    
    for dragon_enemies in  game_data[enemy]["dragon"]:
             
                dragon_pos=game_data[player]["dragon"][dragon]["pos"]
                dragon_enemies_pos=game_data[enemy]["dragon"][dragon_enemies]["pos"]

                

                if abs(dragon_pos[0] - dragon_enemies_pos[0]) > game_data[player]["dragon"][dragon]["attack_range"]+1 and abs(dragon_enemies_pos[1] - dragon_enemies_pos[1]) > game_data[player]["dragon"][dragon]["attack_range"]+1:
                        
                    distance_y = abs(dragon_pos[0] - dragon_enemies_pos[0])
                    distance_x = abs(dragon_pos[1] - dragon_enemies_pos[1])
                    
                    while closer_position==False:      
                        move=random.choice([0, 0], [0, 1], [1, 0], [1, 1], [-1, 1], [1, -1], [-1, -1], [0, -1], [-1, 0])
                        new_position_y=distance_y+move[0]
                        new_position_x=distance_x+move[1]
                        new_distance_y=abs(new_position_y - dragon_enemies_pos[0])
                        new_distance_x=abs(new_position_x - dragon_enemies_pos[1])
                    
                        if new_distance_y<distance_y and new_distance_x<distance_x:
                            closer_position=True

                    order=(f"{dragon}:@{new_position_y}-{new_position_x}")

    return order


                    
                
                    
