def minimax(game_data:dict, player:str, depth:int, is_maxing:bool)->list:
    """small algorythm that scan every possible move in depth n and choose best move to do each turn to maximize points

    parameters
    ----------
    game_data : dictionnary of dictionnary that contain all game data about player and the map(dict)
    player : name of the player (str)
    depth : depth to scan every move possible (int)
    is maxing
    

    
    returns
    -------
    orders : order with the correct format (list)
    
    Version
    -------
    specification: De Braekeleer Mickaël (v.1 09/04/25)
    implementation: : De Braekeleer Mickaël (v.1 09/04/25)
    """
    if depth == 0 or not check_win(game_data):
        return evaluate(game_data), None

    best_move = None

    if is_maxing:
        max_eval = -9999999
        for move in all_possible_move(game_data):
            eval = minimax(move, depth-1, False)[0]
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = 99999999
        for move in all_possible_move(game_data):
            eval = minimax(move, depth-1, True)[0]
            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move