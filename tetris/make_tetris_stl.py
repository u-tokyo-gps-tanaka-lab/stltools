import numpy as np
from stl import mesh
import sys

tetris_size = 15

'''
input example
[L] -> 00 01 02 12
[T] -> 00 01 02 11
'''

args = sys.argv
input_list = []
for i in range(1,len(args)):
    input_list.append([int(num) for num in args[i]])

input_list = np.array(input_list)
cube_num = input_list.shape[0]

# Define the 8 vertices of the single cube
vertices = np.array([\
    [0, 0, 0],
    [1, 0, 0],
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
    [1, 0, 1],
    [1, 1, 1],
    [0, 1, 1]])
# Define the 12 triangles composing the single cube
faces = np.array([\
    [0,3,1],
    [1,3,2],
    [0,4,7],
    [0,7,3],
    [4,5,6],
    [4,6,7],
    [5,1,2],
    [5,2,6],
    [2,3,6],
    [3,7,6],
    [0,1,5],
    [0,5,4]])

# Define the vertices and triangles of tetris
# Remove the hidden triangles of each cube
ver_tetris = []
faces_tetris = []
for i in range(cube_num):
    ver_i = vertices + [input_list[i][0], input_list[i][1], 0]
    rm_faces_i = []
    for j in range(cube_num):
        if(i == j):
            continue

        ver_j = vertices + [input_list[j][0], input_list[j][1], 0]
        hid_ver = []
        for k in range(len(ver_i)):
            for l in range(len(ver_j)):
                if((ver_i[k] == ver_j[l]).all()):
                    hid_ver.append(k)

        if(len(hid_ver) == 4):
            for k in range(len(faces)):
                if(set(faces[k]) <= set(hid_ver)):
                    rm_faces_i.append(k)
    
    if(i==0):
        ver_tetris = ver_i
        faces_tetris = np.delete(faces, rm_faces_i, axis=0)
    else:
        ver_tetris = np.vstack([ver_tetris, ver_i])
        faces_tetris = np.vstack([faces_tetris, np.delete(faces, rm_faces_i, axis=0) + len(vertices)*i])


# Create the mesh
ver_tetris *= tetris_size

tetris = mesh.Mesh(np.zeros(len(faces_tetris), dtype=mesh.Mesh.dtype))
for j, f in enumerate(faces_tetris):
    for k in range(3):
        tetris.vectors[j][k] = ver_tetris[f[k],:]

# Write the mesh to file "tetris.stl"
tetris.save('tetris.stl')
