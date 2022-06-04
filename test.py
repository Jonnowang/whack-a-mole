import numpy as np

def cast_to_vec(binary_matrix):
    return np.reshape(binary_matrix, 4**2)

adj_field_list = list()
# Generate list of all squares and adjacent squares
for i in range(4):
    for j in range(4):
        cur_field = np.zeros((4, 4), dtype = 'bool')
        adj_index = [[i,j], [i+1,j], [i,j-1], [i-1,j], [i,j+1]]
        for square in adj_index:
            if all(k >= 0 for k in square) and all(k < 4 for k in square):
                cur_field[square[0]][square[1]] = True
            else:
                pass
        adj_field_list.append(cur_field)
adj_field_list = list(map(cast_to_vec, adj_field_list))
A = np.stack(adj_field_list, axis=0)
# print(A[5] ^ A[13] ^ A[15])
b = np.array([[0,1,0,0,1,1,1,0,0,0,0,1,1,1,0,1]], 'bool').T
print(np.matmul(A,b))