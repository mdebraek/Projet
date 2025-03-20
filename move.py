def move(orders, game_data):
    """Déplace un apprenti ou un dragon et vérifie si le mouvement est valide.
    
    Paramètres:
    ----------
    orders : list
        Liste des ordres de mouvement.
    game_data : dict
        Dictionnaire contenant les données du jeu.
        
    Retourne:
    -------
    game_data : dict
        Dictionnaire mis à jour des données du jeu.
    """
    
    # Récupère le nombre de lignes et de colonnes  à partir de game_data
    max_rows = game_data['map'][0]  
    max_cols = game_data['map'][1]  
    
   
    for order in orders:  
        if ':@' in order:  # Vérifie si l'ordre contient le séparateur ':@'
            # Sépare l'ordre en deux parties  l'élément et la position
            element = order.split(':@')
            position = order.split(':@')  
            position_list = position.split('=')  # Sépare la position en deux parties : ligne et colonne
            row = position_list[0]  
            col = position_list[1]  

            # Vérifier si la position est dans les limitesde notre tableaux de jeux
            if row >= 0 and row < max_rows and col >= 0 and col < max_cols:  
                if element in game_data['positions']:  # Vérifie si l'élément existe dans les positions du jeu
                    pos_actuel = game_data['positions'][element] 
                    # la ligne et colonne actuel de notre element 
                    current_row = pos_actuel[0]  
                    current_col = pos_actuel[1]  
                    
                    # Vérifier si le mouvement s'effectue que d'une case (une case vers le bas , vers le haut , une case vers droit , une case vers gauche )
                    if (current_row + 1 == row and current_col == col)  or \
                       (current_row - 1 == row and current_col == col) or \
                       (current_row == row and current_col + 1 == col) or \
                       (current_row == row and current_col - 1 == col):  
                         # Met à jour la position de l'élément dans game_data
                        game_data['positions'][element] = (row, col) 
                    else:
                        print(f"Mouvement not valid.")  
                else:
                    print(f"this move cant be accept because its out of the game_table.")  
                
    return game_data  
