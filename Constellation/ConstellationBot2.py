import math

def find_max(poss_perms, control):
    """

    Parameters
    ----------
    poss_perms : a list of possible permutations of moves, 
    each one having score as the last element - if score is 
    tied for 2 or more, returns all of the tied elements
    control : max number of perms returned - if is greater 
    than length of poss_perms, just returns poss_perms. if is 0, 
    returns empty list

    Returns
    -------
    list of top poss_perms based on control (list of lists)

    """
    if len(poss_perms) <= control:
        return poss_perms
    else:
        vals = []
        maxes = []
        for i in poss_perms:
            vals.append(i[-1])

        for j in range(control):
            try:
                curmax = max(vals)
                for k in poss_perms:
                    if k[-1] == curmax:
                        maxes.append(k)
                        vals.remove(curmax)
            except:
                break
    return maxes
#TESTED and APPROVED


def pyth(p1, p2):
    """
    
    Parameters
    ----------
    p1 : a point with 2 coordinates
    p2 : another point with 2 coordinates

    Returns
    -------
    distance : a float containing the distance between the 2 points

    """
    distance = math.sqrt(abs(p1[0] - p2[0])**2 + abs(p1[1] - p2[1])**2)
    return distance 
#TESTED and APPROVED

def adj_moves(past_moves, availiable_moves, adj_matrix):
    """

    Parameters
    ----------
    past_moves :  list of past moves, with the last element being score
    availiable_moves : list of possible moves
    adjacency_matrix : adjacency matrix of all existing stars

    Returns
    -------
    list of moves adjacent to those provided in past_moves. If none adjacent, 
    returns empty list

    """
    adj_moves = []
    for past_move in past_moves[:-1]: #cycles through past moves
        for indx, conn in enumerate(adj_matrix[past_move[3]]): #cycles through the adjacency list of each past move
            if conn == 1: #if a connection exists
                for star in availiable_moves: 
                    if star[3] == indx: #if this connection connects to an availiable_star:
                        if star not in adj_moves and star not in past_moves:
                            adj_moves.append(star)
    return adj_moves
#TESTED and APPROVED


def best_moves(past_moves, availiable_moves, adj_moves, control, score_multiplier, adj_matrix):
    """
    Parameters
    ----------
    past_moves : list of past moves, with the last element being score
    availiable_moves : a list of availiable (not necessarily adjacent) moves 
    - if equals 0, return []
    control : how many (maximum) move possibilities you can return
    adj_moves : a list of all adjacent_moves given past moves and availiable moves, can be emptyv
    score_multiplier : how much the score is multiplied by
    adj_matrix : adjacency matrix of all existing stars - if equals 0, 
    return best_move_perms based on number of connections

    Returns
    -------
    list of best possible move sequences made by appending one adj_move to past moves 
    (length controled by control) with adjusted score at the end

    """
    poss_move_perms = [] #list of ALL possible moves and their scores
    if adj_moves == []:
        if availiable_moves == []:
            return []
        else:
            for poss_move in availiable_moves:
                move_perm = []
                num_connected = 0
                for indx, conn in enumerate(adj_matrix[poss_move[3]]):
                    if conn == 1:
                        num_connected += 1
                move_perm.extend(past_moves[:-1])
                move_perm.append(poss_move)
                move_perm.append(num_connected)
                poss_move_perms.append(move_perm)
            top_moves = find_max(poss_move_perms, control)
            for move_perm in top_moves:
                move_perm[-1] = past_moves[-1]
            return top_moves
                
    
    else:
        for poss_move in adj_moves: 
            move_perm = []
            score = past_moves[-1]
            for indx, conn in enumerate(adj_matrix[poss_move[3]]):
                if conn == 1:
                    for past_move in past_moves[:-1]:
                        if past_move[3] == indx:
                            score += pyth((poss_move[0], poss_move[1]),(past_move[0], past_move[1])) * score_multiplier
            move_perm.extend(past_moves[:-1])
            move_perm.append(poss_move)
            move_perm.append(score)
            poss_move_perms.append(move_perm)
        
        return find_max(poss_move_perms, control)
#TESTED and APPROVED


def run_bot(past_moves, availiable_moves, control_list, multiplier_list, un_stars, adj_matrix):
    """

    Parameters
    ----------
    past_moves : list of list of past moves, with last index being total score. THEY ALL
    NEED TO BE MARKED AS UNOCCUPIED
    availiable_moves : list of availiable moves (moves that haven't already been claimed)
    control_list : a list of controls for each iteration - length determines number of 
    iterations searched - if list eventually exceeds number of availiable stars, extra
    controls are ignored
    multiplier_list : list of multipliers - same length as control_list, determines how the 
    bot weights current vs future reward. Created so that the bot does the most important 
    moves first
    un_stars : list of stars - ALL MARKED AS UNOCCUPIED
    adj_matrix : matrix that tells you which stars are connected to which other stars
    
    Returns
    -------
    List of best future moves, with total_score at the end

    """
    if past_moves == [[0]]:
        past_moves = [[]]
        poss_move_perms = []
        for star in availiable_moves:
            throwaway = []
            throwaway.append(star)
            throwaway.append(0)
            poss_move_perms.append(throwaway)
    
    else:
        poss_move_perms = past_moves.copy()
    
    for iteration, control in enumerate(control_list):
        if iteration < len(availiable_moves):
            past_moves = poss_move_perms.copy()
            poss_move_perms = []
            
            for past in past_moves:
                availiable_moves_copy = availiable_moves.copy()
                
                for move in past:
                        try:
                            availiable_moves_copy.remove(move)
                        except:
                            pass

                adj = adj_moves(past, availiable_moves_copy, adj_matrix)
                poss_move_perms.extend(best_moves(past, availiable_moves_copy, adj, control_list[iteration], multiplier_list[iteration], adj_matrix))
        else:
            break
    
    return find_max(poss_move_perms, 1)[0]
#TESTED and APPROVED




