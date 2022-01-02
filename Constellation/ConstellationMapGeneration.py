import random

def star_gen(new_star_count, coord_range):
    stars = []
    for star in range(new_star_count):
        new_star = [random.randint(1,coord_range[0]), random.randint(1,coord_range[1]),0, star]
        if new_star in stars:
            pass
        else:
            stars.append(new_star)
    return stars

def matrix_gen(new_star_count, weights):
    matrix = []
    for star in range(new_star_count):
        throwaway = []
        for i in range(new_star_count):
            throwaway.append(0)
        matrix.append(throwaway)
        
    for star in range(new_star_count):
        num_rand = new_star_count - star - 1
        rand_list = [1]
        for conn in range(num_rand):
            rand_list.append((random.choices((0,1), weights))[0])
        
        for i in range(new_star_count - star):
            matrix[star][i+star] = rand_list[i]
            matrix[i+star][star] = rand_list[i]
    return matrix


#stars = star_gen(15, (71,37))
#print(stars)
#adj_matrix = matrix_gen(8, (1,0))
#print(adj_matrix)